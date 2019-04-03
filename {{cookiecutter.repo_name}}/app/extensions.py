from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate

csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()
