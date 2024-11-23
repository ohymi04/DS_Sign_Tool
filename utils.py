import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1
from hashlib import sha256

KEY_DIR = "keys/"
os.makedirs(KEY_DIR, exist_ok=True)

PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "public_key.pem")


def generate_keys():
    """Génère une paire de clés RSA et sauvegarde dans le répertoire."""
    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # Sauvegarder la clé privée
        with open(PRIVATE_KEY_PATH, "wb") as priv_file:
            priv_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Sauvegarder la clé publique
        with open(PUBLIC_KEY_PATH, "wb") as pub_file:
            pub_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        return PUBLIC_KEY_PATH
    else:
        return PUBLIC_KEY_PATH


def compute_file_hash(file_path):
    """Calcule le hash SHA-256 d'un fichier."""
    hash_function = sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            hash_function.update(chunk)
    return hash_function.digest()


def sign_file(file_path):
    """Signe le hash du fichier avec la clé privée."""
    if not os.path.exists(PRIVATE_KEY_PATH):
        raise FileNotFoundError("Clé privée introuvable. Veuillez générer les clés.")

    file_hash = compute_file_hash(file_path)

    with open(PRIVATE_KEY_PATH, "rb") as priv_file:
        private_key = serialization.load_pem_private_key(priv_file.read(), password=None)

    signature = private_key.sign(
        file_hash,
        PSS(mgf=MGF1(hashes.SHA256()), salt_length=PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    signature_file = file_path + ".sig"
    with open(signature_file, "wb") as sig_file:
        sig_file.write(signature)

    return file_hash, signature


def verify_file(file_path, public_key_path, signature_path):
    """Vérifie la signature d'un fichier donné."""
    file_hash = compute_file_hash(file_path)

    with open(public_key_path, "rb") as pub_file:
        public_key = serialization.load_pem_public_key(pub_file.read())

    with open(signature_path, "rb") as sig_file:
        signature = sig_file.read()

    try:
        public_key.verify(
            signature,
            file_hash,
            PSS(mgf=MGF1(hashes.SHA256()), salt_length=PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
