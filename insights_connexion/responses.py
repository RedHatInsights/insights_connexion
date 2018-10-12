from flask import Response
from http import HTTPStatus


def _message(message):
    return {'message': message}


def not_found(message=None):
    if message is None:
        message = 'Resource not found.'
    return Response(response=_message(message), status=HTTPStatus.NOT_FOUND)


def invalid_request_body(message=None):
    if message is None:
        message = 'Invalid request body.'
    return Response(response=_message(message), status=HTTPStatus.BAD_REQUEST)


def delete():
    return Response(status=HTTPStatus.NO_CONTENT)


def create(body):
    return Response(response=body, status=HTTPStatus.CREATED)


def search(count, entities):
    return Response(response={'count': count, 'results': entities}, status=HTTPStatus.OK)


def get(entity):
    return Response(response=entity, status=HTTPStatus.OK)


def update(entity):
    return Response(response=entity, status=HTTPStatus.OK)
