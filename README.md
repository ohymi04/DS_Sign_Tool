---

# 🌟 DS Sign Tool 🌟  
Simplify the digital signing of your files and directories, ensuring their integrity and authenticity.

---

## 🎯 About  
**DS-Sign-Tool** is a user-friendly application for signing and verifying files or directories using RSA cryptography. This tool ensures your files are authentic and unaltered by providing robust digital signatures.  
With an intuitive interface and key features, DS Sign Tool is your trusted ally for safeguarding scripts, executables, and critical projects.

---

## 🚀 Features  
### ✅ **RSA Key Generation**  
- Securely generate a key pair (private and public).  
- The private key is securely stored within the application directory.  

### ✅ **File and Directory Signing**  
- Hash executable files (.exe, .msi) or entire directories.  
- Automatically creates associated files:  
  - `dir_file`: Contains information about the structure of the file/directory.  
  - `hash_file`: Contains the hash of the file/directory.  
  - `hash_signed_file`: Contains the hash signed with the private key.  

### ✅ **Signature Verification**  
- Verify the integrity and authenticity of a signed file or directory using a public key.  

### ✅ **Intuitive Interface**  
- A simple, clear graphical interface for all operations.  

---

## 🖥️ Installation  

### 1. Prerequisites  
- **Windows**: Recommended operating system.  
- **Python 3.8+** (if running the script directly).  
- Necessary Python libraries (see below).  

### 2. Installation Options  
#### **Option 1**: Use the Precompiled Executable  
- Download the `DS-Sign-Tool.exe` file from the **Releases** section on GitHub.  
- Run the executable—no additional setup required.  

#### **Option 2**: Run from Source Code  
1. Clone the project from GitHub:  
   ```bash
   git clone <repository_url>
   cd DS_Sign_Tool
   ```  
2. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Launch the application:  
   ```bash
   python DS_Sign_Tool.py
   ```  

---

## 🛠️ Usage  

### 1. Generate RSA Keys  
- Click "Generate Keys" in the application.  
- A pair of keys (public and private) will be created:  
  - `private_key.pem`: The private key (keep it secure).  
  - `public_key.pem`: The public key (can be shared).  

### 2. Sign a File or Directory  
- Click "Sign File/Directory" and select the item to sign.  
- Associated files will be automatically created in the same directory.  

### 3. Verify a File or Directory  
- Click "Verify File/Directory".  
- Select the file/directory and the corresponding public key.  
- The application will confirm whether the signature is valid.  

---

## 📁 Generated File Structure  

| File                  | Description                                             |  
|-----------------------|---------------------------------------------------------|  
| `<name>.dir_file`     | Contains information about the structure of the file/directory. |  
| `<name>.hash_file`    | Contains the raw SHA-256 hash of the file/directory.    |  
| `<name>.hash_signed_file` | Contains the hash signed with the private key.           |  

---

## 🎨 Graphical Interface  

The DS-Sign-Tool interface has been designed for simplicity and ease of use:  
- **Generate Keys**: Create a new key pair with a single click.  
- **Sign File/Directory**: Select the file or directory to sign.  
- **Verify File/Directory**: Validate the integrity using a public key.  

*(Add a screenshot here if possible)*  

---

## ⚙️ Building the Executable  

If you wish to create a custom executable from the source code:  

1. Install PyInstaller:  
   ```bash
   pip install pyinstaller
   ```  
2. Create an executable with a custom name:  
   ```bash
   pyinstaller --onefile --windowed --name "DS-Sign-Tool" DS_Sign_Tool.py
   ```  
3. The executable will be located in the `dist/` directory:  
   - `DS Sign Tool.exe`  

---

## 📚 Dependencies  

The libraries used in this project are listed in the `requirements.txt` file:  
- **cryptography**: Handles RSA keys and digital signatures.  
- **hashlib**: Computes SHA-256 hashes.  
- **tkinter**: Provides the graphical user interface.  

To install them manually:  
```bash
pip install cryptography
```  

---

## 💡 Security Tips  

1. **Protect Your Private Key**:  
   - Never share it, and keep it in a secure location.  
2. **Distribute Your Public Key Only**:  
   - Users will need this key to verify your signatures.  

---

## 🤝 Contributions  

Contributions, suggestions, and feedback are welcome!  
- Create an issue on the GitHub repository to report bugs or propose improvements.  
- Submit a pull request to add features or fix issues.  

---

## 📝 Licence  

This project is licensed under the **MIT Licence**. You are free to use, modify, and distribute it, provided the original licence is included.  

---

## 🛡️ Contact  

For any questions or support, feel free to get in touch:  
- **GitHub** : [ohymi04](https://github.com/ohymi04)  
- **Discord** : [hy0.___.mi4](https://discordapp.com/users/387302720593461249)

---

✨ **Thank you for using DS Sign Tool to secure your files!** ✨  