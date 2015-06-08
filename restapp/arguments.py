from flask_restful import reqparse
import checkers as ch

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username',
                                type=ch.username_check,
                                required=True)

things_parser = reqparse.RequestParser()
things_parser.add_argument('stuff', type=str, required=True)
