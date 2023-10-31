import abc
import string

import jose.jwt


class JWTAbc(abc.ABC):
    @abc.abstractmethod
    def encode(self, payload: dict) -> str:
        pass

    @abc.abstractmethod
    def decode(self, token: str) -> dict:
        pass


class JWT:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode(self, payload: dict) -> str:
        return jose.jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        return jose.jwt.decode(token, self.secret_key, algorithms=[self.algorithm])


def check_password(password: str) -> bool:
    """
    Check if password is longer than 8 characters, shorter than 100 characters, contains at least one digit
    :param password: password to check
    :return:
    """
    if len(password) < 8:
        return False
    if len(password) > 100:
        return False
    if not any(char.isalpha() for char in password):
        return False
    if any(not char.isprintable() for char in password):
        return False
    return True
