from .postgres import Db

db = Db()

def get_cursor():
    cursor = db.connection.cursor()

    return cursor

def commit_db():
    db.connection.commit()

def query_db(query, args=(), one=False):
    cur = get_cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_app(app):
    db.init_app(app)
