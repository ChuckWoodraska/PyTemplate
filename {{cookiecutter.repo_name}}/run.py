from app.app_factory import create_app
from app.libs.utils import create_db, reset_db
import os

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/config.ini")
app = create_app(config_path)


@app.cli.command("create_db")
def create_database():
    create_db()


@app.cli.command("reset_db")
def reset_database():
    reset_db()