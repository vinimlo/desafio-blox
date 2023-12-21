from apiflask import HTTPError


class AccountNotFound(HTTPError):
    status_code = 200
    message = 'Account does not exist.'


class CPFAlreadyExists(HTTPError):
    status_code = 403
    message = 'CPF already exists.'


class PersonNotFound(HTTPError):
    status_code = 200
    message = 'Person does not exist.'
