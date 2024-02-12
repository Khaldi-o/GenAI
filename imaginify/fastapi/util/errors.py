from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, message):
        self.status_code = 404
        self.detail = message


class NotAuthError(HTTPException):
    def __init__(self, message):
        self.status_code = 401
        self.detail = message


class PostingError(HTTPException):
    def __init__(self, message):
        self.status_code = 500
        self.detail = message


class GeneratingError(HTTPException):
    def __init__(self, message):
        self.status_code = 500
        self.detail = message


class LanguageError(HTTPException):
    def __init__(self, message):
        self.status_code = 500
        self.detail = message
