import click
import collections
import dateutil

from dateparser import parse
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from flask import (
    Blueprint,
    current_app,
    session,
    request,
    redirect,
    url_for,
    flash,
    render_template,
    g,
    jsonify,
    send_file
)
from flask.cli import with_appcontext

from .db import get_cursor, query_db, commit_db
from .games import get_games, get_votes
from .utils import login_required, populate_nav, londonToUtc

bp = Blueprint("admin", __name__, url_prefix="/adm")


def init_app(app):
    app.cli.add_command(register_admin_command)


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            query_db("SELECT * FROM user_account WHERE id = %s", [user_id], True)
        )


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user_account by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = query_db(
            "SELECT * FROM user_account WHERE username = %s and password is not null and deleted = false", [username], True)

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

    return render_template("admin/login.html", this='/login')


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
    db = get_cursor()
    error = None

    if not username:
        error = {"error": 'Username is required.', "code": 400}
    elif not password and admin:
        error = {"error": 'Password is required for admin.', "code": 400}
    elif query_db(
            'SELECT id FROM user_account WHERE username = %s', [username], True) is not None:
        error = {"error": 'User {0} is already registered.'.format(
            username), "code": 409}

    if password is not None:
        password = generate_password_hash(password)

    if error is None:
        # the name is available, store it in the database and go to
        # the login page
        db.execute(
            'INSERT INTO user_account (username, password, admin) VALUES (%s, %s, %s)',
            (username, password, admin)
        )
        commit_db()
        return {"code": 200}
    return error


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.index'))


@bp.route("/")
@login_required
def index():
    games = get_games()
    users = query_db('select * from user_account order by username')
    return render_template("admin/index.html", users=users, games=games)


@bp.route('/user/<username>')
@login_required
def show_user_profile(username):
    user = query_db('select * from user_account where username=%s', [username], True)
    votes = get_votes(user=user)
    return render_template("admin/user.html", user=user, this='/adm/user', votes=votes)


@bp.route('/game/<instance_id>')
@login_required
def show_game(instance_id):
    game = get_games(instance_id=instance_id, single=True, sort="name")
    votes = get_votes(instance_id=instance_id, require_comment=True)
    genres = query_db('select * from genre')
    return render_template("admin/game.html", game=game, votes=votes, genres=genres)


@bp.route('/user/add-user', methods=["POST"])
@login_required
def add_user():
    username = request.form.get("newUsername")
    admin = request.form.get("newAdmin", False)
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
    instanceId = request.form.get("instanceId")
    if not instanceId:
        return jsonify(error="missing game"), 400
    userId = request.form.get("userId")
    comment = request.form.get("comment", None)
    vote = request.form.get("vote", 0)
    if not vote and not comment:
        return jsonify(error="Either a vote of a comment is required"), 400

    date = request.form.get("date")
    if not date:
        date = datetime.utcnow()
    else:
        date = parse(date, settings={
                     'TIMEZONE': 'Europe/London', 'RETURN_AS_TIMEZONE_AWARE': True})
        date = londonToUtc(date)

    if (query_db("select 1 from vote where user_id=%s and instance_id=%s", [userId, instanceId], True)):
        return jsonify(error="User has already commented on this game"), 409
    db = get_cursor()
    try:
        db.execute(
            'INSERT INTO vote (instance_id, user_id, date, vote) VALUES (%s, %s, %s, %s)',
            (instanceId, userId, date, vote)
        )
        if comment:
            db.execute('INSERT INTO comment (comment, vote_id) VALUES (%s,%s)',
                       (comment, db.lastrowid))
        commit_db()
    except Exception as e:
        current_app.logger.info(e)
        return jsonify(error="something went wrong"), 400

    # comments = query_db('select g.name as game, c.comment, c.up - c.down as vote, c.date from comment c, game_instance gi, game g where c.user_id=%s and c.instance_id = gi.id and g.id=gi.game_id', [user.get("id")])
    return jsonify(success=True, comment=comment, game=request.form.get("game"), vote=vote, date=date)


@bp.route("/todo")
@login_required
def todo():
    return send_file('../TODO', mimetype='text/plain')


@bp.context_processor
def admin_sections():
    sections = [
        {'name': "Admin"}
    ]

    if(g.user):
        sections.append({'name': "Logout", 'url': 'logout'})
    else:
        sections.append(
            {'name': "Login", 'title': 'EGDS - Login', 'url': 'login'})
    return populate_nav(prefix=bp.url_prefix, links=sections, title='EGDS - Admin')
