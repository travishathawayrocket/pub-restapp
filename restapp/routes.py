from restapp.app import api
import restapi as rs


api.add_resource(rs.Index, '/')
api.add_resource(rs.User, '/user/<user_id>')
api.add_resource(rs.UserList, '/user')
api.add_resource(rs.MyListOfThings, '/thing')
api.add_resource(rs.MySingleThing, '/thing/<thing_id>')
