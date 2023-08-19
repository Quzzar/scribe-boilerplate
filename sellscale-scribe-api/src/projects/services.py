
from src.users.services import get_user
from app import supabase
import requests
import os
from src.templates.services import get_template
from src.utils.slack import send_slack_message, URL_MAP

def create_project(user_id: int, name: str, description: str, template_id: int = None):

    if template_id is not None:
        template = get_template(template_id)
    else:
        template = None

    res = (supabase
      .table('projects')
      .insert({
          "name": name,
          "description": description,
          "user_id": user_id,
          "template_id": template_id if template is not None else None,
          "blocks": template.get('blocks') if template is not None else [],
      })
      .execute()
    )

    return res.data[0] if len(res.data) > 0 else None


def update_project(user_id: int, project_id: int, name: str, description: str):
   
    res = supabase.table('projects').update({
        "name": name,
        "description": description,
    }).eq('id', project_id).eq('user_id', user_id).execute()

    return res.data[0] if len(res.data) > 0 else None


def delete_project(user_id: int, project_id: int):
    res = supabase.table('projects').delete().eq('id', project_id).eq('user_id', user_id).execute()
    return res.data[0] if len(res.data) > 0 else None


def get_project(user_id: int, project_id: int):
    res = supabase.table('projects').select("*").eq('id', project_id).eq('user_id', user_id).execute()
    return res.data[0] if len(res.data) > 0 else None


def get_projects(user_id: int):
    res = supabase.table('projects').select("*").eq('user_id', user_id).execute()
    return res.data


# Message generation
def create_message(user_id: int, project_id: int, li_url: str, blocks: list[str]):
    
    # Verify that the project belongs to the user
    project = get_project(user_id, project_id)
    if project is None:
        return False, "Project not found", None
    
    # Get archetype_id from user
    user = get_user(user_id)
    archetype_id = user.get('archetype_id', None) if user is not None else None
    if archetype_id is None:
        return False, "User archetype not found", None
    
    # Get prospect_id from li_url
    response = requests.get(f"{os.environ.get('SELLSCALE_API_URL')}/personas/prospect_from_li_url?li_url={li_url}",
      headers={
        "Authorization": f"Bearer {os.environ.get('SELLSCALE_AUTH_TOKEN')}",
      },
    )
    prospect_id = response.json().get('data', {}).get('prospect_id', None) if response.status_code == 200 else None

    if prospect_id is None:
        # Create a prospect in Sellscale
        response = requests.post(f"{os.environ.get('SELLSCALE_API_URL')}/prospect/from_link",
          headers={
            "Authorization": f"Bearer {os.environ.get('SELLSCALE_AUTH_TOKEN')}",
            "Content-Type": "application/json",
          },
          json={
            "archetype_id": archetype_id,
            "url": li_url,
            "live": True,
          }
        )
        if response.status_code == 200:
            print('Created a prospect in Sellscale')
            prospect_id = response.json().get('data', {}).get('prospect_id', None)
        else:
            return False, "Failed to create prospect in Sellscale", None
    
    # Create a message in Sellscale
    response = requests.post(f"{os.environ.get('SELLSCALE_API_URL')}/ml/generate_email_automatic",
      headers={
        "Authorization": f"Bearer {os.environ.get('SELLSCALE_AUTH_TOKEN')}",
        "Content-Type": "application/json",
      },
      json={
        "prospect_id": prospect_id,
        "email_blocks": blocks,
      }
    )

    subject = ""
    msg = ""
    if response.status_code == 200:
        subject = response.json().get('data', {}).get('subject', '')
        msg = response.json().get('data', {}).get('body', '')
    else:
        return False, "Failed to generate message", None

    # Create a message record
    res = (supabase
      .table('messages')
      .insert({
          "project_id": project_id,
          "prospect_id": prospect_id,
          "li_url": li_url,
          "original_message": msg,
          "original_blocks": blocks,
          "current_message": msg,
          "current_subject": subject,
          "original_subject": subject,
      })
      .execute()
    )

    message = res.data[0] if len(res.data) > 0 else None
    if message:
        
        slack_blocks = [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": f"*{user.get('name')} ({user.get('email')}, archetype #{archetype_id}) just generated a new message!*\n\n _LinkedIn:_ {li_url}"
                }
              },
              {
                "type": "divider"
              },
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": f"*{message.get('original_subject')}*"
                }
              },
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": message.get('original_message')
                }
              },
              {
                "type": "divider"
              },
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*They used the following blocks:*\n"
                }
              }
        ]
        for block in message.get('original_blocks'):
            slack_blocks.append({
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": block,
                }
            })

        send_slack_message(
            message=f"{user.get('name')} ({user.get('email')}, archetype #{archetype_id}) just generated a new message!",
            blocks=slack_blocks,
            webhook_urls=[URL_MAP["eng-scribe"]],
        )

    return True, "Success", message


def get_message(user_id: int, message_id: int):
    res = supabase.table('messages').select("*").eq('id', message_id).execute()
    message = res.data[0] if len(res.data) > 0 else None
    if message is None: return None
    project = get_project(user_id, message.get('project_id'))
    if project is None: return None
    return message


def get_messages(user_id: int, project_id: int):
    # Verify that the project belongs to the user
    project = get_project(user_id, project_id)
    if project is None: return []
    
    res = supabase.table('messages').select("*").eq('project_id', project_id).execute()
    return res.data


def update_message(user_id: int, message_id: int, subject: str, message: str):
   
    # Verify that the message belongs to the user
    message = get_message(user_id, message_id)
    if message is None: return None

    res = supabase.table('messages').update({
        "current_subject": subject,
        "current_message": message,
    }).eq('id', message_id).execute()

    return res.data[0] if len(res.data) > 0 else None
