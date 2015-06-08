import sqlite3
from flask.ext.restful import Resource, abort, fields, marshal_with
from .arguments import create_user_parser, update_user_parser
from .app import get_db


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'favorite_color': fields.String
}


class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        self.db = get_db()
        self.cursor = self.db.cursor()
        super(BaseResource, self).__init__(*args, **kwargs)


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
    @marshal_with(user_fields)
    def get(self, user_id):
        """
        This is the user resource. Given a user ID, this will
        return information about the user.
        """
        res = self.cursor.execute('SELECT * FROM users WHERE id = {}'.format(user_id))
        row = res.fetchone()
        self.cursor.close()

        if row:
            return {
                'data': {
                    'id': row[0],
                    'username': row[1],
                    'email': row[2],
                    'favorite_color': row[3],
                }
            }
        else:
            return abort(404, message='User not found')

    def put(self, user_id):
        """
        Update the user

        :param user_id: Integer
        """
        args = update_user_parser.parse_args()
        res = self.cursor.execute("SELECT * FROM users WHERE id = {}".format(user_id))
        row = res.fetchone()

        if row:
            pass
        else:
            return abort(404, message='User not found')

    def delete(self, user_id):
        """
        Remove the user

        :param user_id: Integer
        """
        self.cursor.execute("DELETE FROM users WHERE id = {}".format(user_id))

        return {
            'message': 'User deleted'
        }


class UserList(BaseResource):
    def get(self):
        """
        This is the user resource. Given a user ID, this will
        return information about the user.
        """
        res = self.cursor.execute("SELECT * FROM users")
        rows = res.fetchall()
        self.cursor.close()

        return {
            'data': rows or []
        }

    def post(self):
        """
        Create a new user
        """
        args = create_user_parser.parse_args()
        username = args.get('username')
        email = args.get('email')
        favorite_color = args.get('favorite_color')

        try:
            self.cursor.execute(
                "INSERT INTO users (username, email, favorite_color) VALUES ('{}', '{}', '{}')".format(
                    username, email, favorite_color)
            )
        except sqlite3.IntegrityError:
            return {
                'message': 'User with provided username already exists'
            }, 400

        res = self.cursor.execute(
            "SELECT id, username, email, favorite_color FROM users WHERE username = '{}'".format(username)
        )
        row = res.fetchone()
        self.cursor.close()

        return {
            'data': {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'favorite_color': row[3]
            }
        }
