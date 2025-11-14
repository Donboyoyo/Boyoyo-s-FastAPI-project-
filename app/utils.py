from passlib.context import CryptContext

# defining the hashing setting 
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

# defining a password we can call
def hash (password: str):
    return pwd_context.hash(password)


def verify (plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)