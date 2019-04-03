from flask import redirect, url_for, request, Blueprint, render_template
from app.extensions import login_manager
from app.libs.models import User
from flask_login import current_user, login_user, logout_user, login_required


core = Blueprint("core", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@core.route("/")
def index():
    """
    Renders index page.
    :return:
    :rtype:
    """
    return render_template("index.html")


@core.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders login page on GET and logs in user on POST.
    :return:
    :rtype:
    """
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # User(username).set_password(password)
        user = User.query.filter_by(username=username).first()
        if (
            User(username).try_login(username, password)
            and user.confirmed
            and not user.archived
        ):
            login_user(user)
            return redirect(url_for("core.index"))
        else:
            return render_template("login.html")
    return render_template("login.html")


@core.route("/logout")
@login_required
def logout():
    """
    Log user out.
    :return:
    :rtype:
    """
    logout_user()
    return redirect(url_for("core.index"))