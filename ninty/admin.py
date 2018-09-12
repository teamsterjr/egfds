import functools
import click
from dateutil.parser import parse
from datetime import *
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
@login_required
def show_user_profile(username):
    # show the user profile for that user
    user = query_db('select * from user where username=?', [username],True)
    comments = query_db('select g.name as game, c.comment, c.up - c.down as vote, c.date from comment c inner join game g on c.gameId = g.id where c.userId=?', [user.get("id")])
    return render_template("admin/user.html", user=user, comments=comments)


@bp.route('/user/add-user', methods=["POST"])
@login_required
def add_user():
    username = request.form.get("newUsername")
    admin = request.form.get("newAdmin", 0)
    returnVal = register(
        username,
        request.form.get("password"),
        admin
    )
    if returnVal.get("code", 200) == 200:
        return jsonify(success=True, username=username, admin=admin)
    else:
        return jsonify(returnVal), returnVal.get("code")

@bp.route('/user/add-comment', methods=["POST"])
@login_required
def add_comment():
    # game / user / comment / vote / date
    gameId = request.form.get("gameId")
    userId = request.form.get("userId")
    comment = request.form.get("comment")
    up = 0
    down = 0
    vote = request.form.get("vote",0)
    if int(vote)> 0:
        up = 1
    if int(vote) < 0:
        down = 1
    date = request.form.get("date")
    date = parse(date) if date else "{}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
    print([gameId, userId, comment, date])
    db = get_db()
    try:
        db.execute(
            'INSERT INTO comment (gameid, userid, comment, date, up, down) VALUES (?, ?, ?, ?, ?, ?)',
            (gameId, userId, comment, date, up, down)
        )
        db.commit()
    except sqlite3.Error as e:
        print(e)
    return jsonify(success=True)

@bp.route('dump')
def dump():
    db = get_db()
    with open('instance/dump.sql', 'w') as f:
        for line in db.iterdump():
            f.write('%s\n' % line)
    return "ok"


def init_app(app):
    app.cli.add_command(register_admin_command)
