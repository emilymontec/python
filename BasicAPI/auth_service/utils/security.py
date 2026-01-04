import bcrypt
import hashlib


def hash_password(password: str) -> str:
    # Generar hash con bcrypt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Devolver como string
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    try:
        # Convertir ambos a bytes
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        # Verificar con bcrypt
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        # Si hay algún error (formato incorrecto, etc.), retornar False
        return False


def fingerprint(user_agent: str, ip: str) -> str:
    raw = f"{user_agent}:{ip}".encode()
    return hashlib.sha256(raw).hexdigest()