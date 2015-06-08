from __future__ import unicode_literals, absolute_import, print_function

from flask import Blueprint
from flask_restful import Api
from .restapi import (
    Index, UserList, User, MySingleThing,
    MyListOfThings
)


restapp_blueprint = Blueprint('restapp', __name__)
api = Api(restapp_blueprint)

# Register all the routes in your REST API
api.add_resource(Index, '/')
api.add_resource(User, '/user/<user_id>')
api.add_resource(UserList, '/user')
api.add_resource(MyListOfThings, '/thing')
api.add_resource(MySingleThing, '/thing/<thing_id>')
