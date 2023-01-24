import secrets
from datetime import datetime, timedelta
from jose import jwt
from cryptography.fernet import Fernet



### --------------------- CONFIGURATION --------------------------
# secret key for JWT token
SECRET_KEY = "c558a80a-f319-4c10-95d4-4282ef745b4b"

#Type of algorithm used for password/token hashing
ALGORITHM = "HS256"

# expiration time for token
ACCESS_TOKEN_EXPIRE_MINUTES = 30
### --------------------------------------------------------------

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def EncryptPassword(password_to_encrypt):
    key = Fernet.generate_key()
    pw_encryptor = Fernet(key)
    salt = secrets.token_hex(8)
    hashed_pw = pw_encryptor.encrypt(bytes(password_to_encrypt + salt, 'utf-8'))

    return salt, hashed_pw, key

def EncryptCompare(hashed_pw, user_provided_pw, salt, key):
    fernet_pw = Fernet(key)
    hash_user_provided = fernet_pw.encrypt(bytes(user_provided_pw + salt,  encoding = 'utf-8'))

    print (hash_user_provided)
    print (hashed_pw)

    if hashed_pw == hash_user_provided:
        return True
    return False

def DecryptPassword(password_to_decrypt, key):
    pw_decryptor = Fernet(key)
    decrypted_pw = pw_decryptor.decrypt(password_to_decrypt)
    return decrypted_pw