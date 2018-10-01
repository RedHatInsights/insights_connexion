from .config import config
import connexion
from connexion.resolver import RestyResolver
from connexion.decorators.response import ResponseValidator
from connexion.exceptions import NonConformingResponseBody, NonConformingResponseHeaders
from .db import base as db
from flask import Response
from http import HTTPStatus
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


# By default validate_response will return the full stack trace to the client.
# This will instead return a simple 500
class CustomResponseValidator(ResponseValidator):
    def validate_response(self, data, status_code, headers, url):
        try:
            super().validate_response(data, status_code, headers, url)
        except(NonConformingResponseBody, NonConformingResponseHeaders):
            raise Exception()


session = db.init()
validator_map = {
    'response': CustomResponseValidator
}
app = connexion.App('tag',
                    specification_dir='swagger/',
                    validator_map=validator_map,
                    debug=config.debug)
app.add_api('api.spec.yaml', resolver=RestyResolver(
    'api'), validate_responses=True)


def exists_handler(exception):
    return Response(response=json.dumps({'message': 'Resource exists.'}), status=HTTPStatus.CONFLICT)


def no_result_handler(exception):
    return Response(response=json.dumps({'message': 'Resource not found.'}), status=HTTPStatus.NOT_FOUND)


app.add_error_handler(NoResultFound, no_result_handler)
app.add_error_handler(IntegrityError, exists_handler)

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def start():
    app.run(int(config.port))
