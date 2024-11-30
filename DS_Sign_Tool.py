import os
import hashlib
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox


# Répertoire pour stocker les clés
KEY_DIR = "keys/"
if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)

# Fonction pour récupérer les ressources dynamiquement
def resource_path(relative_path):
    """Obtenir le chemin absolu pour les ressources (icônes, etc.)."""
    try:
        # Si l'application est exécutée depuis un exécutable PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Si l'application est exécutée depuis le script source
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Chemin vers OpenSSL
OPENSSL_PATH = resource_path("openssl/openssl.exe")


# Fonction pour calculer le hachage SHA-256
def calculate_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(4096):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


# Fonction pour signer un fichier avec OpenSSL
def sign_file(file_path, private_key):
    try:
        signed_file = file_path + ".signed"
        subprocess.run([OPENSSL_PATH, "dgst", "-sha256", "-sign", private_key, "-out", signed_file, file_path], check=True)
        return signed_file
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error signing file: {e}")


# Fonction pour vérifier la signature d'un fichier avec OpenSSL
def verify_file(file_path, public_key, signed_file):
    try:
        result = subprocess.run([OPENSSL_PATH, "dgst", "-sha256", "-verify", public_key, "-signature", signed_file, file_path],
                                check=True, text=True, capture_output=True)
        return "Verified OK" in result.stdout
    except subprocess.CalledProcessError:
        return False


# Fonction pour générer les clés
def generate_keys(key_name):
    try:
        pub_key = os.path.join(KEY_DIR, f"{key_name}_public.pem")
        priv_key = os.path.join(KEY_DIR, f"{key_name}_private.pem")
        subprocess.run([OPENSSL_PATH, "ecparam", "-name", "prime256v1", "-genkey", "-out", priv_key])
        subprocess.run([OPENSSL_PATH, "ec", "-in", priv_key, "-pubout", "-out", pub_key])
        return priv_key, pub_key
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error generating keys: {e}")


# Classe principale pour l'interface utilisateur
class DSSignToolApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DS-Sign-Tool")
        self.setWindowIcon(QtGui.QIcon(resource_path("DS-Sign-Tool_Icone.ico")))  # Charger l'icône dynamiquement
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Titre principal
        title = QtWidgets.QLabel("DS-Sign-Tool")
        title.setFont(QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Champs de saisie pour le fichier à signer/vérifier
        self.file_path_input = QtWidgets.QLineEdit(self)
        self.file_path_input.setPlaceholderText("Enter file path or use the browse button")
        browse_button = QtWidgets.QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)

        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(browse_button)
        layout.addLayout(file_layout)

        # Champs pour les clés
        self.private_key_input = QtWidgets.QLineEdit(self)
        self.private_key_input.setPlaceholderText("Enter private key path or use the browse button")
        browse_private_key_button = QtWidgets.QPushButton("Browse", self)
        browse_private_key_button.clicked.connect(self.browse_private_key)

        private_key_layout = QtWidgets.QHBoxLayout()
        private_key_layout.addWidget(self.private_key_input)
        private_key_layout.addWidget(browse_private_key_button)
        layout.addLayout(private_key_layout)

        self.public_key_input = QtWidgets.QLineEdit(self)
        self.public_key_input.setPlaceholderText("Enter public key path or use the browse button")
        browse_public_key_button = QtWidgets.QPushButton("Browse", self)
        browse_public_key_button.clicked.connect(self.browse_public_key)

        public_key_layout = QtWidgets.QHBoxLayout()
        public_key_layout.addWidget(self.public_key_input)
        public_key_layout.addWidget(browse_public_key_button)
        layout.addLayout(public_key_layout)

        # Boutons principaux
        generate_keys_button = QtWidgets.QPushButton("Generate Keys", self)
        generate_keys_button.clicked.connect(self.generate_keys)
        sign_file_button = QtWidgets.QPushButton("Sign File", self)
        sign_file_button.clicked.connect(self.sign_file)
        verify_file_button = QtWidgets.QPushButton("Verify File", self)
        verify_file_button.clicked.connect(self.verify_file)

        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.addWidget(generate_keys_button)
        buttons_layout.addWidget(sign_file_button)
        buttons_layout.addWidget(verify_file_button)
        layout.addLayout(buttons_layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)

    def browse_private_key(self):
        private_key_path, _ = QFileDialog.getOpenFileName(self, "Select Private Key")
        if private_key_path:
            self.private_key_input.setText(private_key_path)

    def browse_public_key(self):
        public_key_path, _ = QFileDialog.getOpenFileName(self, "Select Public Key")
        if public_key_path:
            self.public_key_input.setText(public_key_path)

    def generate_keys(self):
        key_name, ok = QtWidgets.QInputDialog.getText(self, "Key Name", "Enter a name for the key:")
        if ok and key_name:
            try:
                priv_key, pub_key = generate_keys(key_name)
                QMessageBox.information(self, "Success", f"Keys generated!\nPrivate Key: {priv_key}\nPublic Key: {pub_key}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def sign_file(self):
        file_path = self.file_path_input.text()
        private_key = self.private_key_input.text()
        if not file_path or not private_key:
            QMessageBox.warning(self, "Warning", "Please provide both file path and private key path.")
            return
        try:
            signed_file = sign_file(file_path, private_key)
            QMessageBox.information(self, "Success", f"File signed successfully!\nSigned File: {signed_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def verify_file(self):
        file_path = self.file_path_input.text()
        public_key = self.public_key_input.text()
        signed_file = file_path + ".signed"
        if not file_path or not public_key:
            QMessageBox.warning(self, "Warning", "Please provide both file path and public key path.")
            return
        try:
            valid = verify_file(file_path, public_key, signed_file)
            if valid:
                QMessageBox.information(self, "Success", "Signature is valid!")
            else:
                QMessageBox.warning(self, "Invalid", "Signature is invalid.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = DSSignToolApp()
    window.show()
    sys.exit(app.exec_())
