from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend

from config import SECRET_PASSWORDS


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_PASSWORDS, lifetime_seconds=36000000)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)