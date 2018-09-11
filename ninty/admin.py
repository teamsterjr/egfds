import functools
import click
from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash
from flask.cli import with_appcontext

from ninty.db import get_db, query_db
from ninty.games import get_games

bp = Blueprint("admin", __name__, url_prefix="/adm")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("admin.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            query_db("SELECT * FROM user WHERE id = ?", [user_id], True)
        )


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = query_db(
            "SELECT * FROM user WHERE username = ? and password is not null and deleted = 0", [username], True)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("admin.index"))

        flash(error)

    return render_template("admin/login.html")


@click.command('register')
@click.argument('username')
@click.argument('password')
@with_appcontext
def register_admin_command(username, password):
    status = register(username, password, True)
    print(status.get("error")) if not status.get(
        "code") == 200 else print("YAY")


def register(username, password, admin=False):
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    db = get_db()
    error = None

    if not username:
        error = {"error": 'Username is required.', "code": 400}
    elif not password and admin:
        error = {"error": 'Password is required for admin.', "code": 400}
    elif query_db(
            'SELECT id FROM user WHERE username = ?', [username], True) is not None:
        error = {"error": 'User {0} is already registered.'.format(
            username), "code": 409}

    if password is not None:
        password = generate_password_hash(password)

    if error is None:
        # the name is available, store it in the database and go to
        # the login page
        db.execute(
            'INSERT INTO user (username, password, admin) VALUES (?, ?, ?)',
            (username, password, admin)
        )
        db.commit()
        return {"code": 200}
    return error


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route("/")
@login_required
def index():
    db = get_db()
    users = query_db('select * from user')
    return render_template("admin/index.html", users=users)


@bp.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@bp.route('/user/add-user', methods=["POST"])
def add_user():
    returnVal = register(
        request.form.get("newUsername"),
        request.form.get("password"),
        request.form.get("newAdmin", 0)
    )
    if returnVal.get("code", 200) == 200:
        return jsonify(success=True)
    else:
        return jsonify(returnVal), returnVal.get("code")


def init_app(app):
    app.cli.add_command(register_admin_command)
