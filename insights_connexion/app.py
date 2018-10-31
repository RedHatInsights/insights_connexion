import asyncio
import json
import uuid
from json import JSONDecodeError

from sqlalchemy.orm.exc import NoResultFound

import connexion
from aiohttp import web
from asyncpg.exceptions import UniqueViolationError
from connexion.decorators.response import ResponseValidator
from connexion.decorators.validation import RequestBodyValidator
from connexion.exceptions import (NonConformingResponseBody,
                                  NonConformingResponseHeaders)
from connexion.resolver import RestyResolver
from jsonschema import ValidationError

from . import responses, util
from .config import config
from .db import gino as db
from .logger import log


# By default validate_response will return the full stack trace to the client.
# This will instead return a simple 500
class CustomResponseValidator(ResponseValidator):
    def validate_response(self, data, status_code, headers, url):
        try:
            super().validate_response(data, status_code, headers, url)
        except(NonConformingResponseBody, NonConformingResponseHeaders):
            raise Exception()


# This enables a custom error message for invalid request bodies to be sent to the client.
class RequestBodyValidator(RequestBodyValidator):
    def validate_schema(self, data, url):
        if self.is_null_value_valid and connexion.utils.is_null(data):
            return None
        self.validator.validate(data)


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except(ValidationError) as e:
        log.error(e)
        response = responses.invalid_request_parameters()
    except(UniqueViolationError) as e:
        log.error(e)
        response = responses.resource_exists()
    except(NoResultFound) as e:
        log.error(e)
        response = responses.not_found()
    except(Exception) as e:
        log.error(e)
        response = responses.internal_server_error()

    return response


@web.middleware
async def log_middleware(request, handler):
    try:
        req_body = await request.json() if request.has_body else None
    except JSONDecodeError as e:
        log.error(e)
        return responses.invalid_request_parameters('Malformed JSON in request body.')

    req_id = str(uuid.uuid4())

    log.info({'message': req_id,
              'type': 'request',
              'req_id': req_id,
              'body': req_body,
              'cookies': dict(request.cookies),
              'content-type': request.content_type,
              'content-length': request.content_length,
              'headers': dict(request.headers),
              'method': request.method,
              'query': dict(request.query),
              'url': str(request.url)})

    response = await handler(request)

    log.info({'message': req_id,
              'type': 'response',
              'req_id': req_id,
              'body': response.text,
              'cookies': dict(response.cookies),
              'content_type': response.content_type,
              'content_length': response.content_length,
              'headers': dict(response.headers),
              'status_code': response.status})

    return response


validator_map = {
    'response': CustomResponseValidator,
    'body': RequestBodyValidator
}
debug = util.string_to_bool(config.debug)

app = connexion.AioHttpApp('__main__',
                           specification_dir='swagger/',
                           validator_map=validator_map,
                           debug=debug,
                           middlewares=[log_middleware, error_middleware])
app.add_api('api.spec.yaml',
            resolver=RestyResolver('api'),
            validate_responses=True,
            strict_validation=True,
            pass_context_arg_name='request')


application = app.app


def _parse_headers(dict_in):
    return json.dumps(
        {k: v for k, v in dict_in})


def _parse_params(params):
    return params.to_dict(flat=False)


@asyncio.coroutine
async def setup_app(app):
    await db.init()
    app['db'] = db
    return app


def start():
    app_copy = app.app
    app.app = setup_app(app_copy)
    app.run(port=int(config.port))
