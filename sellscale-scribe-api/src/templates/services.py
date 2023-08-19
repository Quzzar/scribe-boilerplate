
from app import supabase


def create_template(name: str, description: str, blocks: list[str]):

    res = (supabase
      .table('templates')
      .insert({"name": name, "description": description, "blocks": blocks})
      .execute()
    )

    return res.data[0] if len(res.data) > 0 else None


def get_template(template_id: int):
    res = supabase.table('templates').select("*").eq('id', template_id).execute()
    return res.data[0] if len(res.data) > 0 else None


def get_templates():
    res = supabase.table('templates').select("*").execute()
    return res.data
