import os
from tkinter import Tk, Label, Button, filedialog, messagebox, ttk
from utils import generate_keys, sign_file, verify_file

KEY_DIR = "keys/"

class DSSignTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DS Sign Tool")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Titre principal
        Label(self.root, text="DS Sign Tool", font=("Helvetica", 20, "bold")).pack(pady=20)

        # Boutons principaux
        Button(self.root, text="Générer des clés", command=self.generate_keys, width=30).pack(pady=10)
        Button(self.root, text="Signer un fichier ou dossier", command=self.sign_ui, width=30).pack(pady=10)
        Button(self.root, text="Vérifier un fichier", command=self.verify_ui, width=30).pack(pady=10)

        # Barre de progression
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=20)

    def generate_keys(self):
        """Génère des clés RSA."""
        try:
            public_key_path = generate_keys()
            messagebox.showinfo("Succès", f"Clés générées avec succès.\nClé publique sauvegardée dans : {public_key_path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération des clés : {e}")

    def sign_ui(self):
        """Permet de sélectionner et de signer un fichier ou dossier."""
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier ou dossier à signer")
        if not file_path:
            return

        try:
            self.progress.start(10)
            file_hash, signature = sign_file(file_path)
            self.progress.stop()
            messagebox.showinfo("Succès", f"Fichier signé avec succès.\nHash : {file_hash.hex()}")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Erreur", f"Erreur lors de la signature : {e}")

    def verify_ui(self):
        """Permet de vérifier la signature d'un fichier."""
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier à vérifier")
        if not file_path:
            return

        signature_path = filedialog.askopenfilename(title="Sélectionnez le fichier de signature associé")
        if not signature_path:
            return

        public_key_path = os.path.join(KEY_DIR, "public_key.pem")
        if not os.path.exists(public_key_path):
            messagebox.showerror("Erreur", "Clé publique introuvable. Générer les clés d'abord.")
            return

        try:
            self.progress.start(10)
            is_valid = verify_file(file_path, public_key_path, signature_path)
            self.progress.stop()
            if is_valid:
                messagebox.showinfo("Succès", "Signature valide.")
            else:
                messagebox.showwarning("Invalide", "La signature est invalide.")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Erreur", f"Erreur lors de la vérification : {e}")

if __name__ == "__main__":
    root = Tk()
    app = DSSignTool(root)
    root.mainloop()
