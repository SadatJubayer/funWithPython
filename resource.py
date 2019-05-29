from flask_restful import Resource
from flask import request, jsonify, g
from .model import User
from .schema import UserSchema
from app import api, db, auth, app
from marshmallow import ValidationError


class UserApiPk(Resource):

    def get(self, pk):
        user = User.query.get_or_404(pk, description="user with this id doens't exit")

        user_schema = UserSchema()
        result = user_schema.dump(user)
        return {'user': result}

    """post for signup the user"""

    def post(self):
        print(request.data)
        json_input = request.get_json()
        print('got post')
        if not json_input:
            return {'error ': 'bad request'}, 400

        # handler for UserSchema
        user_schema = UserSchema()

        # first check the format of the request
        try:
            data = user_schema.load(json_input)
            print('data', data)

            """the below line fixed the issue with validation error"""
            # pip install - U marshmallow - -pre

        except ValidationError as err:
            return {'errors': err.messages}, 422

        if User.query.filter_by(username=data['username']).first():
            return {'error': 'username exists'}, 400

        if User.query.filter_by(email=data['email']).first():
            return {'error': 'email exists'}, 400

        new_user = User(data['username'], data['email'], data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "new user added"}, 200

    # the see if the username and email already exists


class UserApiUsername(Resource):

    def get(self, username):
        print("username got the request")
        user = User.query.filter_by(username=username).first_or_404(description="user with this name doesn't exist")

        user_schema = UserSchema()
        result = user_schema.dump(user)
        print(result)
        return {'user': result}


# TODO: it needs to changed with resource

class UserNameCheck(Resource):

    @auth.login_required
    def get(self):
        return {'data': 'hello %s' % g.user.username}


class TokenGenerator(Resource):

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}


# @app.route('/joke/api/resource')
# @auth.login_required
# def get_resource():
#     return jsonify({'data': 'Hello %s' % g.user.username})
#
# @app.route('/joke/api/token')
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify({'token':token.decode('ascii')})


# HELPER
@auth.verify_password
def verify_password(username_or_token, password):
    print("verification happened")
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


api.add_resource(UserNameCheck, '/joke/api/resource', endpoint='testing')
api.add_resource(TokenGenerator, '/joke/api/token', endpoint='token')
api.add_resource(UserApiPk, '/joke/api/user/<int:pk>', endpoint='user')
api.add_resource(UserApiPk, '/joke/api/user/signup/', endpoint='signup')
api.add_resource(UserApiUsername, '/joke/api/user/<string:username>', endpoint='username')
