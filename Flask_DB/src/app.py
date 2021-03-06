import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from src.resources.security import authenticate, identity
from src.resources.user import UserRegister
from src.resources.item import Item_, ItemRegister, GetOneItem

app = Flask(__name__)
app.secret_key = os.urandom(16)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_AUTH_URL_RULE'] = '/login'  # replace path // auth -> login
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'  # email

jwt = JWT(app, authenticate, identity)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token':
            access_token.decode('utf-8'),
        'user_id': identity.id
    })


api = Api(app)

api.add_resource(UserRegister, '/user')
api.add_resource(Item_, '/items')
api.add_resource(ItemRegister, '/item')
api.add_resource(GetOneItem, '/item/<string:name>')

if __name__ == '__main__':
    from src.database.ORM import db  # avoid circular import
    db.init_app(app)
    app.run(debug=True, port=5000)
