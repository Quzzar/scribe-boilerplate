
from src.utils.slack import send_slack_message, URL_MAP
from app import supabase
import requests
import os

def get_user(user_id: int):
    from app import supabase
    res = supabase.table('users').select("*").eq('id', user_id).execute()
    return res.data[0] if len(res.data) > 0 else None


def get_user_from_auth_id(auth_user_id: int):
    from app import supabase
    res = supabase.table('users').select("*").eq('auth_user_id', auth_user_id).execute()
    return res.data[0] if len(res.data) > 0 else None


def update_user(user_id: int, name: str, role: str, company_name: str, what_you_do: str, buys_your_product: str, why_buy: str, fun_facts: str):
   
    res = supabase.table('users').update({
        "name": name,
        "role": role,
        "company_name": company_name,
        "what_you_do": what_you_do,
        "buys_your_product": buys_your_product,
        "why_buy": why_buy,
        "fun_facts": fun_facts,
    }).eq('id', user_id).execute()

    user = res.data[0] if len(res.data) > 0 else None
    if user:
        
        # Update user's archetype
        response = requests.post(f"{os.environ.get('SELLSCALE_API_URL')}/client/archetype/{user.get('archetype_id')}/update_description_and_fit",
            headers={
              "Authorization": f"Bearer {os.environ.get('SELLSCALE_AUTH_TOKEN')}",
              "Content-Type": "application/json",
            },
            json={
              "updated_persona_fit_reason": user.get('why_buy'),
              "updated_persona_icp_matching_prompt": user.get('buys_your_product'),
              "updated_persona_contact_objective": "",
            }
        )
        if response.status_code != 200:
            print(f"Failed to update archetype for user {user_id} with response: {response.text}")

        send_slack_message(
            message=f"""
🪄 A new user just onboarded to SellScale Scribe. Their email is: {user.get('email')}
Here's some information:
  - Name: {user.get('name')}
  - Role: {user.get('role')}
  - Company Name: {user.get('company_name')}
  - What you do: {user.get('what_you_do')}
  - Who buys your product: {user.get('buys_your_product')}
  - Why buy: {user.get('why_buy')}
  - Fun facts: {user.get('fun_facts')}
""",
            webhook_urls=[URL_MAP["eng-scribe"]],
        )

    return user


def sign_in_user(email: str):

    try:
       res = supabase.auth.sign_out()
    except:
        pass
    
    try:
        data = supabase.auth.sign_in_with_otp({
          "email": email,
          "options": {
            #"email_redirect_to": 'https://example.com/welcome'
          }
        })
    except Exception as e:
        print(e)
        return False

    return True


def auth_user(access_token: str, refresh_token: str):
    res = supabase.auth.set_session(access_token, refresh_token)

    user = get_user_from_auth_id(res.user.id)

    created_user = False
    if not user:
      # Create archetype for user
      response = requests.post(f"{os.environ.get('SELLSCALE_API_URL')}/client/archetype",
          headers={
            "Authorization": f"Bearer {os.environ.get('SELLSCALE_AUTH_TOKEN')}",
            "Content-Type": "application/json",
          },
          json={
            "archetype": f"Archetype for {res.user.email}",
            "disable_ai_after_prospect_engaged": True,
            "description": "",
            "fit_reason": "",
            "icp_matching_prompt": "",
            "contact_objective": "",
          }
      )
      archetype_id = None
      if response.status_code == 200:
          print('Created an archetype in Sellscale')
          archetype_id = response.json().get('client_archetype_id', None)
      else:
          return None, None, None, False

      data, count = (supabase
        .table('users')
        .insert({
            "auth_user_id": res.user.id,
            "email": res.user.email,
            "name": "New User",
            "archetype_id": archetype_id,
        })
        .execute()
      )
      if len(data) > 0:
        created_user = True

        send_slack_message(
            message=f"🎉 A new user ({res.user.email}, archetype #{archetype_id}) just signed up for SellScale Scribe!",
            webhook_urls=[URL_MAP["eng-scribe"]],
        )

    return res.user.id, res.session.access_token, res.session.refresh_token, created_user


def refresh_user_token(refresh_token: str):
    res = supabase.auth.refresh_session(refresh_token)
    return res.session.access_token, res.session.refresh_token
