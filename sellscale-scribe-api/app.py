
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

from supabase import create_client, Client

app = Flask(__name__)
cors = CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    #default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app.config["CORS_HEADERS"] = "Content-Type"

supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/')
def hello():

    return 'Hello, World!'

# Register blueprints
from src.users.controllers import USERS_BLUEPRINT
from src.projects.controllers import PROJECTS_BLUEPRINT
from src.templates.controllers import TEMPLATES_BLUEPRINT

app.register_blueprint(USERS_BLUEPRINT, url_prefix="/user")
app.register_blueprint(PROJECTS_BLUEPRINT, url_prefix="/project")
app.register_blueprint(TEMPLATES_BLUEPRINT, url_prefix="/template")

if __name__ == '__main__':
    app.run()
