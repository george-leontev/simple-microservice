from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_pssword = pwd_context.hash('abcdef')

print(hashed_pssword)