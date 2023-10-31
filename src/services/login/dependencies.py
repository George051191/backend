from typing import Annotated

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils import JWTAbc


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)  # self.jwt = jwt

    async def __call__(self, request: Request, jwt: Annotated[JWTAbc, Depends()] = None):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if (request.url.path == "/projects/all" or request.url.path == "/users/experts") and not credentials:
            request.state.user = {"email": "test@test.org"}
            return
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail={"message": "Invalid authorization code"})
            self.jwt = jwt
            user = self.verify_jwt(credentials.credentials)
            if not user:
                raise HTTPException(status_code=403, detail={"message": "Invalid authorization code"})
            request.state.user = user
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail={"message": "Invalid authorization code"})

    def verify_jwt(self, token: str) -> dict | None:
        try:
            payload = self.jwt.decode(token)
        except Exception as e:
            payload = None
        return payload
