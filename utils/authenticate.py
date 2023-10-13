import re
from datetime import datetime as dt, timedelta, datetime
from functools import wraps

from flask import current_app, Response
from flask_restful import reqparse
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from utils import database

Session = sessionmaker(bind=database)
session = Session()


def authenticate():
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parser = reqparse.RequestParser()
            parser.add_argument('Authorization', type=str, location='headers', required=True)
            args = parser.parse_args()

            match = re.match(r'^Bearer\s(\S+)$', args['Authorization'])
            if not match:
                error = 'Bearer error="invalid_request", error_description="Incorrect token format"'
                return Response(status=400, headers={'WWW-Authenticate': error})

            token = match.group(1)
            current_date = dt.today().date()

            from models import User
            user = User.query.filter(and_(User.token_expired_at > current_date, User.token == token)).first()
            if not user:
                error = 'Bearer error="invalid_token", error_description="Incorrect token"'
                return Response(status=401, headers={'WWW-Authenticate': error})

            kwargs['user'] = user

            token_expires_days = current_app.configuration['token_expired_days']
            if user.token_expired_at.date() - timedelta(days=token_expires_days) != current_date:
                user.token_expired_at = datetime.utcnow() + timedelta(days=token_expires_days)
                session.commit()
            return func(*args, **kwargs)

        return wrapper

    return actual_decorator
