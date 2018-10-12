from flask import Response
from http import HTTPStatus
import json


def _message(message):
    return json.dumps({'message': message})


def resource_exists(message=None):
    if message is None:
        message = 'Resource exists.'
    return Response(response=_message(message), status=HTTPStatus.CONFLICT)


def not_found(message=None):
    if message is None:
        message = 'Resource not found.'
    return Response(response=_message(message), status=HTTPStatus.NOT_FOUND)


def invalid_request_parameters(message=None):
    if message is None:
        message = 'Invalid request parameters.'
    return Response(response=_message(message), status=HTTPStatus.BAD_REQUEST)


def delete():
    return HTTPStatus.NO_CONTENT


def create(body):
    return body, HTTPStatus.CREATED


def search(count, entities):
    return {'count': count, 'results': entities}, HTTPStatus.OK


def get(entity):
    return entity, HTTPStatus.OK


def update(entity):
    return entity, HTTPStatus.OK
