import base64, hashlib, os, sys
password = sys.argv[1] if len(sys.argv) > 1 else input('Password: ')
salt = os.urandom(16)
digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 210_000)
print(base64.b64encode(salt + digest).decode())
