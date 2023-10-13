import logging
from datetime import datetime, date

from flask import Flask, request
from flask_restful import Api
from simplejson import JSONEncoder
from werkzeug.exceptions import HTTPException


class FlaskApp(Flask):
    class FlaskJSONEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, (date, datetime)):
                return o.isoformat()
            return super().default(o)

    json_encoder = FlaskJSONEncoder


class FlaskApi(Api):
    logger = logging.getLogger(__name__)

    def handle_error(self, e):
        FlaskApi.logger.exception(e)
        if (getattr(e, 'code', 500) == 500 and not getattr(e, 'data', dict()).get('message')) \
                or not isinstance(e, HTTPException):
            return self.make_response({'message': 'Произошла внутренняя ошибка, попробуйте позже'}, 500)
        return super().handle_error(e)


def get_client_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


