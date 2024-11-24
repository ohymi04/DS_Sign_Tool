import os
import hashlib
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Entry, simpledialog

KEY_DIR = "keys/"  # Répertoire pour stocker les clés

# Crée un répertoire "keys/" s'il n'existe pas
if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)

# Chemin vers OpenSSL
OPENSSL_PATH = "C:\\Users\\nguyen\\Desktop\\DS_Sign_Tool\\openssl\\openssl.exe"  # Remplacez ce chemin si nécessaire

# Fonction pour calculer le hachage d'un fichier avec SHA-256
def calculate_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(4096):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Fonction pour signer un fichier avec OpenSSL (ECDSA)
def sign_file(file_path, private_key):
    try:
        # Calcul du hash du fichier
        file_hash = calculate_hash(file_path)
        
        # Signer le fichier avec OpenSSL (ECDSA)
        signed_file_path = file_path + ".signed"
        subprocess.run([OPENSSL_PATH, "dgst", "-sha256", "-sign", private_key, "-out", signed_file_path, file_path], check=True)
        
        return file_hash, signed_file_path
    except Exception as e:
        raise Exception(f"Erreur lors de la signature du fichier : {e}")

# Fonction pour vérifier la signature d'un fichier avec OpenSSL (ECDSA)
def verify_file(file_path, public_key, signed_file):
    try:
        # Vérifier la signature du fichier avec OpenSSL
        verification = subprocess.run([OPENSSL_PATH, "dgst", "-sha256", "-verify", public_key, "-signature", signed_file, file_path], check=True, text=True, capture_output=True)
        
        if "Verified OK" in verification.stdout:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# Fonction pour signer un fichier
def sign_file_direct(file_path, private_key):
    file_hash, signed_file = sign_file(file_path, private_key)
    return file_hash, signed_file

# Fonction pour vérifier un fichier
def verify_file_direct(file_path, public_key, signed_file):
    return verify_file(file_path, public_key, signed_file)

class DSSignTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DS-Sign-Tool")
        self.root.geometry("900x600")
        self.root.resizable(True, True)  # Rendre la fenêtre redimensionnable
        self.root.iconbitmap("md5.ico")  # Remplacez ce chemin si nécessaire

        # Titre principal
        tk.Label(self.root, text="DS-Sign-Tool", font=("Helvetica", 20, "bold")).pack(pady=20)

        # Cadre pour la saisie et la sélection de fichiers
        self.path_entry_frame = ttk.Frame(self.root)
        self.path_entry_frame.pack(pady=20)

        # Zone de saisie du chemin
        self.path_entry_label = tk.Label(self.path_entry_frame, text="Chemin du fichier :")
        self.path_entry_label.pack(side="top", padx=10)
        self.path_entry = Entry(self.path_entry_frame, width=40)
        self.path_entry.pack(side="top", padx=10)

        # Bouton pour ouvrir l'explorateur de fichiers
        self.browse_button_file = tk.Button(self.path_entry_frame, text="...", command=self.browse_file, width=5)
        self.browse_button_file.pack(side="top", padx=10)

        # Cadre pour la saisie des chemins des clés publique et privée
        self.keys_frame = ttk.Frame(self.root)
        self.keys_frame.pack(pady=10)

        # Zone de saisie pour la clé privée
        self.private_key_label = tk.Label(self.keys_frame, text="Clé Privée :")
        self.private_key_label.pack(side="left", padx=10)
        self.private_key_entry = Entry(self.keys_frame, width=40)
        self.private_key_entry.pack(side="left", padx=10)

        # Bouton pour ouvrir l'explorateur de fichiers pour la clé privée
        self.browse_button_private = tk.Button(self.keys_frame, text="...", command=self.browse_private_key, width=5)
        self.browse_button_private.pack(side="left", padx=10)

        # Zone de saisie pour la clé publique
        self.public_key_label = tk.Label(self.keys_frame, text="Clé Publique :")
        self.public_key_label.pack(side="left", padx=10)
        self.public_key_entry = Entry(self.keys_frame, width=40)
        self.public_key_entry.pack(side="left", padx=10)

        # Bouton pour ouvrir l'explorateur de fichiers pour la clé publique
        self.browse_button_public = tk.Button(self.keys_frame, text="...", command=self.browse_public_key, width=5)
        self.browse_button_public.pack(side="left", padx=10)

        # Boutons principaux
        tk.Button(self.root, text="Générer des clés", command=self.generate_keys, width=30).pack(pady=10)
        tk.Button(self.root, text="Signer un fichier", command=self.sign_ui, width=30).pack(pady=10)
        tk.Button(self.root, text="Vérifier un fichier", command=self.verify_ui, width=30).pack(pady=10)

        # Barre de progression
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=20)

    def generate_keys(self):
        """Génère des clés avec OpenSSL pour ECDSA."""
        try:
            # Demander le nom de la clé
            key_name = simpledialog.askstring("Nom de la clé", "Entrez le nom pour la clé :")
            if not key_name:
                raise ValueError("Nom de clé invalide.")

            # Utilisation d'OpenSSL pour générer une paire de clés ECDSA
            pub_key_file = os.path.join(KEY_DIR, f"{key_name}_public.pem")
            priv_key_file = os.path.join(KEY_DIR, f"{key_name}_private.pem")

            # Générer la clé privée et publique via OpenSSL (ECDSA)
            subprocess.run([OPENSSL_PATH, "ecparam", "-name", "prime256v1", "-genkey", "-out", priv_key_file])
            subprocess.run([OPENSSL_PATH, "ec", "-in", priv_key_file, "-pubout", "-out", pub_key_file])

            messagebox.showinfo("Succès", f"Clés générées avec succès.\nClé publique sauvegardée dans : {pub_key_file}\nClé privée sauvegardée dans : {priv_key_file}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération des clés : {e}")

    def browse_file(self):
        """Ouvre l'explorateur de fichiers pour sélectionner un fichier."""
        selected_path = filedialog.askopenfilename(title="Sélectionner un fichier")
        if selected_path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, selected_path)

    def browse_private_key(self):
        """Ouvre l'explorateur de fichiers pour sélectionner la clé privée."""
        private_key_path = filedialog.askopenfilename(title="Sélectionner la clé privée")
        if private_key_path:
            self.private_key_entry.delete(0, "end")
            self.private_key_entry.insert(0, private_key_path)

    def browse_public_key(self):
        """Ouvre l'explorateur de fichiers pour sélectionner la clé publique."""
        public_key_path = filedialog.askopenfilename(title="Sélectionner la clé publique")
        if public_key_path:
            self.public_key_entry.delete(0, "end")
            self.public_key_entry.insert(0, public_key_path)

    def sign_ui(self):
        """Permet de signer un fichier."""
        file_path = self.path_entry.get()
        private_key = self.private_key_entry.get()

        if not file_path or not private_key:
            messagebox.showerror("Erreur", "Veuillez entrer ou sélectionner un fichier valide et une clé privée valide.")
            return

        try:
            self.progress.start(10)
            # Signer le fichier
            file_hash, signed_file = sign_file_direct(file_path, private_key)
            self.progress.stop()
            messagebox.showinfo("Succès", f"Fichier signé avec succès.\nFichier signé : {signed_file}")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Erreur", f"Erreur lors de la signature : {e}")

    def verify_ui(self):
        """Permet de vérifier la signature d'un fichier."""
        file_path = self.path_entry.get()
        public_key = self.public_key_entry.get()

        if not file_path or not public_key:
            messagebox.showerror("Erreur", "Veuillez entrer ou sélectionner un fichier valide et une clé publique valide.")
            return

        try:
            self.progress.start(10)
            # Vérifier la signature du fichier
            signed_file = file_path + ".signed"
            is_valid = verify_file_direct(file_path, public_key, signed_file)
            self.progress.stop()

            if is_valid:
                messagebox.showinfo("Succès", f"Signature valide pour : {file_path}")
            else:
                messagebox.showwarning("Erreur", f"Signature invalide pour : {file_path}")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Erreur", f"Erreur lors de la vérification : {e}")

# Création de la fenêtre principale
if __name__ == "__main__":
    root = tk.Tk()
    app = DSSignTool(root)
    root.mainloop()

