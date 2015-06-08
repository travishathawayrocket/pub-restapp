from flask.ext.restful import Resource, abort
from flask import current_app as app
import sqlite3
from .arguments import things_parser, create_user_parser
import os


class BaseResource(Resource):

    def __init__(self, *args, **kwargs):
        conn = sqlite3.connect(app.config['DB_LOCATION'])
        self.db = conn.cursor()
        self.init_db()
        super(BaseResource, self).__init__(*args, **kwargs)

    def init_db(self):
        """
        Initialize our database by create a couple tables
        """
        res = self.db.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='users'
            """)

        if not res.fetchall():
            self.db.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    email TEXT,
                    favorite_color TEXT
                )""")

        res = self.db.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='things'
            """)

        if not res.fetchall():
            self.db.execute(
                """
                CREATE TABLE things (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    color TEXT,
                    weight TEXT
                )""")

class Index(BaseResource):
    def get(self):
        """
        The index of your restapi
        """
        return {
            'message': 'Welcome to restapp. The sample Flask Restful'
                       ' tutorial app'
        }


class User(BaseResource):
    def get(self, user_id):
        """
        This is the user resource. Given a user ID, this will
        return information about the user.
        """
        res = self.db.execute('SELECT * FROM users WHERE id = {}'.format(user_id))
        row = res.fetchone()

        if row:
            return {
                'data': row.fetchone()
            }
        else:
            return abort(404, message='User not found')


class UserList(BaseResource):
    def get(self):
        """
        This is the user resource. Given a user ID, this will
        return information about the user.
        """
        res = self.db.execute("SELECT * FROM users")
        rows = res.fetchall()

        return {
            'data': rows or []
        }

    def post(self):
        """
        Create a new user
        """
        args = create_user_parser.parse_args()
        username = args.get('username')

        self.db.execute("INSERT INTO users (username) VALUES ('{}')".format(username))

        res = self.db.execute("SELECT * FROM users WHERE username = '{}'".format(username))
        row = res.fetchone()

        return {
            'data': row
        }


class MySingleThing(BaseResource):
    def get(self, thing_id):
        results = None

        if os.path.exists('./database.csv') and os.path.isfile('./database.csv'):
            with open('./database.csv') as f_handle:
                for line in f_handle.readlines():
                    if line[0] == thing_id:
                        resutls = {
                            'data': [x for x in line.split(',')]
                        }

        if results:
            return results
        else:
            raise abort(404)


class MyListOfThings(BaseResource):
    def post(self):
        """
        Create our resource
        """
        args = thing_parser.parse_args()
        stuff = args.get('stuff')

        if stuff:
            with open('./database.csv', 'a') as f_handle:
                f_handle.write('{}\n'.format(args.get('stuff')))
            return {'message': 'resource created'}
        else:
            return {'message': 'nothing created'}
