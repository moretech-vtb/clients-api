from datetime import datetime, timedelta

from flask import current_app, make_response, jsonify, Response
from flask_restful import Resource, reqparse

from models import User
from utils import bcrypt, database, authenticate


class LoginResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required=True)
        args = parser.parse_args()

        user_login = args['login']
        password = args['password']

        config = current_app.configuration

        user = User.query.filter_by(login=user_login).first()
        if user and bcrypt.check_password_hash(user.password, password):
            user.token_expired_at = datetime.utcnow() + timedelta(days=config['token_expired_days'])
            database.session.commit()
            return make_response(jsonify(dict(token=user.token)), 200)
        elif not user:
            return make_response(jsonify(dict(message='Пользователь не найден')), 400)

        return make_response(jsonify(dict(message='Логин и/или пароль неверны')), 400)


class AuthResource(Resource):

    @authenticate()
    def get(self, *args, **kwargs):
        return Response(status=200)
