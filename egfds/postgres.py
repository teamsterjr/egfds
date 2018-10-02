from flask import _app_ctx_stack, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
class Db(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('DB_HOST', 'localhost')
        app.config.setdefault('DB_USER', None)
        app.config.setdefault('DB_PASSWORD', None)
        app.config.setdefault('DB_DB', None)
        app.config.setdefault('DB_PORT', 5432)
        app.config.setdefault('DB_UNIX_SOCKET', None)
        app.config.setdefault('DB_CONNECT_TIMEOUT', 10)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)

    @property
    def connect(self):
        kwargs = {}

        if current_app.config['DB_HOST']:
            kwargs['host'] = current_app.config['DB_HOST']

        if current_app.config['DB_USER']:
            kwargs['user'] = current_app.config['DB_USER']

        if current_app.config['DB_PASSWORD']:
            kwargs['password'] = current_app.config['DB_PASSWORD']

        if current_app.config['DB_DB']:
            schema = current_app.config['DB_DB']
            kwargs['database'] = schema
            kwargs['options']=f'-c search_path={schema}'

        if current_app.config['DB_PORT']:
            kwargs['port'] = current_app.config['DB_PORT']

        if current_app.config['DB_UNIX_SOCKET']:
            kwargs['unix_socket'] = current_app.config['DB_UNIX_SOCKET']

        if current_app.config['DB_CONNECT_TIMEOUT']:
            kwargs['connect_timeout'] = \
                current_app.config['DB_CONNECT_TIMEOUT']


        kwargs['cursor_factory']=RealDictCursor
        # if current_app.config['DB_CURSORCLASS']:
        #   kwargs['cursorclass'] = getattr(MySQLdb.cursors, current_app.config['DB_CURSORCLASS'])

        return psycopg2.connect(**kwargs)

    @property
    def connection(self):
        """Attempts to connect to the postgres server.

        :return: Bound postgres connection object if successful or ``None`` if
            unsuccessful.
        """

        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'pgsql_db'):
                ctx.pgsql_db = self.connect
            return ctx.pgsql_db

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'pgsql_db'):
            ctx.pgsql_db.close()
