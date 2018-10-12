from http import HTTPStatus


def not_found(message=None):
    if message is None:
        message = 'Resource not found.'
    return {'message': message}, HTTPStatus.NOT_FOUND


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
