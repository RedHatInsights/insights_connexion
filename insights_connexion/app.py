from .config import config
import connexion
from connexion.resolver import RestyResolver
from connexion.decorators.response import ResponseValidator
from connexion.exceptions import NonConformingResponseBody, NonConformingResponseHeaders
from .db import base as db
from jsonschema import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from . import util, responses


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
debug = util.string_to_bool(config.debug)
app = connexion.App('tag',
                    specification_dir='swagger/',
                    validator_map=validator_map,
                    debug=debug)
app.add_api('api.spec.yaml', resolver=RestyResolver(
    'api'), validate_responses=True, strict_validation=True)


def exists_handler(exception):
    return responses.resource_exists()


def no_result_handler(exception):
    return responses.not_found()


def validation_error_handler(exception):
    return responses.invalid_request_parameters()


app.add_error_handler(NoResultFound, no_result_handler)
app.add_error_handler(IntegrityError, exists_handler)
app.add_error_handler(ValidationError, validation_error_handler)

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def start():
    app.run(int(config.port))
