import os
import hashlib
import subprocess
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel


# Répertoire pour stocker les clés
KEY_DIR = "keys/"
if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)


# Fonction pour récupérer les ressources dynamiquement
def resource_path(relative_path):
    """Obtenir le chemin relatif pour les ressources (icônes, etc.)."""
    try:
        base_path = sys._MEIPASS  # Si l'application est exécutée depuis un exécutable PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Si l'application est exécutée depuis le script source
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


# Fonction pour signer un fichier
def sign_file(file_path, private_key):
    try:
        signed_file = file_path + ".signed"
        subprocess.run([OPENSSL_PATH, "dgst", "-sha256", "-sign", private_key, "-out", signed_file, file_path], check=True, encoding="utf-8", errors="ignore")
        return signed_file
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error signing file: {e}")


# Fonction pour vérifier un fichier
def verify_file(file_path, public_key, signed_file):
    try:
        result = subprocess.run(
            [OPENSSL_PATH, "dgst", "-sha256", "-verify", public_key, "-signature", signed_file, file_path],
            check=True, text=True, capture_output=True, encoding="utf-8", errors="ignore")
        return "Verified OK" in result.stdout
    except subprocess.CalledProcessError:
        return False


# Fonction pour générer l'arborescence d'un répertoire
def generate_tree(directory, output_file, prefix=""):
    """
    Génère l'arborescence d'un répertoire et écrit dans un fichier.
    """
    entries = sorted(os.listdir(directory))
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        full_path = os.path.join(directory, entry)
        is_last = index == entries_count - 1

        if os.path.isdir(full_path):
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"{prefix}├───📁 {entry}\n")
            new_prefix = f"{prefix}│   " if not is_last else f"{prefix}    "
            generate_tree(full_path, output_file, new_prefix)
        else:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"{prefix}└───📄 {entry}\n")


# Fonction pour signer un répertoire
def sign_directory(directory_path, private_key):
    try:
        dir_file_path = os.path.join(directory_path, "dir_file")
        hash_file_path = os.path.join(directory_path, "hash_file")
        signed_hash_file_path = hash_file_path + ".signed"

        # Générer le fichier d'arborescence
        with open(dir_file_path, "w", encoding="utf-8") as dir_file:
            dir_file.write(f"{directory_path}:\n")
        generate_tree(directory_path, dir_file_path)

        # Calculer le hash du fichier d'arborescence
        with open(hash_file_path, "w", encoding="utf-8") as hash_file:
            hash_value = calculate_hash(dir_file_path)
            hash_file.write(hash_value)

        # Signer le hash
        sign_file(hash_file_path, private_key)
        return dir_file_path, signed_hash_file_path
    except Exception as e:
        raise Exception(f"Error signing directory: {e}")


# Fonction pour vérifier un répertoire
def verify_directory(directory_path, public_key):
    try:
        dir_file_path = os.path.join(directory_path, "dir_file")
        hash_file_path = os.path.join(directory_path, "hash_file")
        signed_hash_file_path = hash_file_path + ".signed"

        # Vérifier si les fichiers nécessaires existent
        if not all(os.path.exists(p) for p in (dir_file_path, hash_file_path, signed_hash_file_path)):
            return False, "Missing signature files in directory."

        # Vérifier le hash de l'arborescence
        recalculated_hash = calculate_hash(dir_file_path)
        with open(hash_file_path, "r", encoding="utf-8") as hash_file:
            original_hash = hash_file.read().strip()

        if recalculated_hash != original_hash:
            return False, "Directory structure hash mismatch."

        # Vérifier la signature du hash
        valid = verify_file(hash_file_path, public_key, signed_hash_file_path)
        if not valid:
            return False, "Signature invalid."

        return True, "Directory verification successful."
    except Exception as e:
        return False, str(e)


class DSSignToolApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DS-Sign-Tool")
        self.setWindowIcon(QtGui.QIcon(resource_path("icon/DS-Sign-Tool_Icone.ico")))
        self.resize(775, 540)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # Ajouter la bannière en .ico
        self.display_banner()

        self.file_path_input = QtWidgets.QLineEdit(self)
        self.file_path_input.setPlaceholderText("Enter file/folder path or use the import button")
        self.file_path_input.setStyleSheet("padding: 5px;")

        import_menu = QtWidgets.QMenu(self)
        import_file_action = QtWidgets.QAction(QtGui.QIcon(resource_path("icon/file_icon.ico")), "Import File", self)
        import_file_action.triggered.connect(self.import_file)
        import_menu.addAction(import_file_action)

        import_folder_action = QtWidgets.QAction(QtGui.QIcon(resource_path("icon/folder_icon.ico")), "Import Folder", self)
        import_folder_action.triggered.connect(self.import_folder)
        import_menu.addAction(import_folder_action)

        import_button = QtWidgets.QPushButton("Import", self)
        import_button.setMenu(import_menu)
        import_button.setStyleSheet("background-color: #264653; color: white; padding: 5px;")

        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(import_button)
        main_layout.addLayout(file_layout)

        self.private_key_input = QtWidgets.QLineEdit(self)
        self.private_key_input.setPlaceholderText("Enter private key path or use the browse button")
        self.private_key_input.setStyleSheet("padding: 5px;")
        browse_private_key_button = QtWidgets.QPushButton("Browse", self)
        browse_private_key_button.setStyleSheet("background-color: #264653; color: white; padding: 5px;")
        browse_private_key_button.clicked.connect(self.browse_private_key)

        private_key_layout = QtWidgets.QHBoxLayout()
        private_key_layout.addWidget(self.private_key_input)
        private_key_layout.addWidget(browse_private_key_button)
        main_layout.addLayout(private_key_layout)

        self.public_key_input = QtWidgets.QLineEdit(self)
        self.public_key_input.setPlaceholderText("Enter public key path or use the browse button")
        self.public_key_input.setStyleSheet("padding: 5px;")
        browse_public_key_button = QtWidgets.QPushButton("Browse", self)
        browse_public_key_button.setStyleSheet("background-color: #264653; color: white; padding: 5px;")
        browse_public_key_button.clicked.connect(self.browse_public_key)

        public_key_layout = QtWidgets.QHBoxLayout()
        public_key_layout.addWidget(self.public_key_input)
        public_key_layout.addWidget(browse_public_key_button)
        main_layout.addLayout(public_key_layout)

        generate_keys_button = QtWidgets.QPushButton("Generate Keys", self)
        generate_keys_button.setStyleSheet("background-color: #2A9D8F; color: white; padding: 10px;")
        generate_keys_button.clicked.connect(self.generate_keys)

        sign_file_button = QtWidgets.QPushButton("Sign File/Folder", self)
        sign_file_button.setStyleSheet("background-color: #2A9D8F; color: white; padding: 10px;")
        sign_file_button.clicked.connect(self.sign_file)

        verify_file_button = QtWidgets.QPushButton("Verify File/Folder", self)
        verify_file_button.setStyleSheet("background-color: #2A9D8F; color: white; padding: 10px;")
        verify_file_button.clicked.connect(self.verify_file)

        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.addWidget(generate_keys_button)
        buttons_layout.addWidget(sign_file_button)
        buttons_layout.addWidget(verify_file_button)
        main_layout.addLayout(buttons_layout)

        copyright_label = QtWidgets.QLabel("© 2024 Dat-Sam NGUYEN Ltd. All rights reserved")
        copyright_label.setAlignment(QtCore.Qt.AlignRight)
        copyright_label.setStyleSheet("color: gray; font-size: 10px; margin-top: 20px;")
        main_layout.addWidget(copyright_label)

        self.setLayout(main_layout)

    def display_banner(self):
        banner_label = QLabel(self)
        banner_path = resource_path("icon/banner_png.png")  # Remplacer par le chemin correct de votre bannière
        banner_pixmap = QtGui.QPixmap(banner_path)

        if not banner_pixmap.isNull():
            banner_pixmap = banner_pixmap.scaled(750, 350, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            banner_label.setPixmap(banner_pixmap)
        else:
            banner_label.setText("Banner not found!")  # Si l'image est introuvable

        banner_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout().addWidget(banner_label)

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)

    def import_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.file_path_input.setText(folder_path)

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
                pub_key = os.path.join(KEY_DIR, f"{key_name}_public.pem")
                priv_key = os.path.join(KEY_DIR, f"{key_name}_private.pem")
                subprocess.run([OPENSSL_PATH, "ecparam", "-name", "prime256v1", "-genkey", "-out", priv_key])
                subprocess.run([OPENSSL_PATH, "ec", "-in", priv_key, "-pubout", "-out", pub_key])
                QMessageBox.information(self, "Success", f"Keys generated!\nPrivate Key: {priv_key}\nPublic Key: {pub_key}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def sign_file(self):
        file_path = self.file_path_input.text()
        private_key = self.private_key_input.text()
        if not file_path or not private_key:
            QMessageBox.warning(self, "Warning", "Please provide both file/folder path and private key path.")
            return
        try:
            if os.path.isfile(file_path):
                signed_file = sign_file(file_path, private_key)
                QMessageBox.information(self, "Success", f"File signed successfully!\nSigned File: {signed_file}")
            elif os.path.isdir(file_path):
                dir_file_path, signed_hash_file = sign_directory(file_path, private_key)
                QMessageBox.information(self, "Success", f"Folder signed successfully!\nDir File: {dir_file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def verify_file(self):
        file_path = self.file_path_input.text()
        public_key = self.public_key_input.text()
        if not file_path or not public_key:
            QMessageBox.warning(self, "Warning", "Please provide both file path and public key path.")
            return
        try:
            if os.path.isfile(file_path):
                signed_file = file_path + ".signed"
                valid = verify_file(file_path, public_key, signed_file)
                if valid:
                    QMessageBox.information(self, "Success", "File signature is valid!")
                else:
                    QMessageBox.warning(self, "Invalid", "File signature is invalid.")
            elif os.path.isdir(file_path):
                valid, message = verify_directory(file_path, public_key)
                if valid:
                    QMessageBox.information(self, "Success", message)
                else:
                    QMessageBox.warning(self, "Invalid", message)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DSSignToolApp()
    window.show()
    sys.exit(app.exec_())
