from passlib.context import CryptContext
import sys

try:
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    print("Context created with pbkdf2_sha256.")
    h = pwd_context.hash("123456")
    print(f"Hash: {h}")
    v = pwd_context.verify("123456", h)
    print(f"Verify: {v}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
