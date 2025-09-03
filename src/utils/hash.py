import bcrypt

# Password

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# String Encoding / Decoding

def encode_string(data: str) -> str:
    return data.encode("utf-8").hex()

def decode_string(data: str) -> str:
    return bytes.fromhex(data).decode("utf-8")
    