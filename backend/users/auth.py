from passlib import context

PWD_CONTEXT = context.CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(raw_password, hashed_password)
