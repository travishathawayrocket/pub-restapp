from flask import Flask
from flask.ext import restful

from .restapi import (
    Index, UserList, User, MySingleThing,
    MyListOfThings
)


# Create your flask app object
app = Flask(__name__)
# Import your config variables
app.config.from_pyfile('config.py')
# Create your restapi object
api = restful.Api(app)

# Register all the routes in your REST API
api.add_resource(Index, '/')
api.add_resource(User, '/user/<user_id>')
api.add_resource(UserList, '/user')
api.add_resource(MyListOfThings, '/thing')
api.add_resource(MySingleThing, '/thing/<thing_id>')
