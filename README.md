
<div align="center">
  <img src="https://github.com/user-attachments/assets/814bfa67-7c50-4468-be0c-9180d987a4df" alt="DS-Sign-Tool_Icone">

   ## 🌟 DS-Sign-Tool 🌟
   Simplify the digital signing of your files and directories, ensuring their integrity and authenticity.
</div>

---

## 🎯 About  
**DS-Sign-Tool** is a powerful yet user-friendly application designed for securely signing and verifying all types of files using cryptographic algorithms (via OpenSSL). Whether you’re protecting your documents, scripts, images, videos, or executables, DS-Sign-Tool ensures their authenticity and guards against tampering with robust digital signatures.
---

## 🚀 Features  
### ✅ **Key Pair Generation**  
- Securely generate a key pair (private and public) for signing and verifying files.  
- The private key and public key are securely stored in the `keys/` directory.

### ✅ **File Signing**  
- Sign any type of file (e.g., `.exe`, `.msi`, `.txt`, `.mp4`, `.jpg`, etc.) using the private key.
- After signing, a `.signed` file is created with the signature of the file.

### ✅ **Directory Signing**  
- If you want to sign an entire directory, you must first compress it into a `.ZIP` file.
- After compression, the directory will be treated as a file and can be signed like any other file.
- The `.ZIP` file, along with the corresponding public key and signed file, will be created in the `keys/` directory.

### ✅ **Signature Verification**  
- Verify the integrity and authenticity of a signed file using the public key.
- This works with both individual files and compressed directories (i.e., `.ZIP` files).

### ✅ **Intuitive Interface**  
- A simple, clear graphical interface for all operations:
  - Generate key pairs (public/private).
  - Sign files or directories (after compression).
  - Verify signed files with the public key.
- Flexible window size to accommodate key entry fields and file selection.
 
---

## 🖥️ Installation  

### 1. Prerequisites  
- **Windows**: Recommended operating system.  
- **Python 3.8+** (if running the script directly).  
- Necessary Python libraries (see below).  

### 2. Installation Options  
#### **Option 1**: Use the Precompiled Executable  
- Download the `DS-Sign-Tool.exe` file from the [**Releases**](https://github.com/ohymi04/DS_Sign_Tool/releases) section on GitHub.  
- Run the executable, no additional setup required.  

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

## 🛠️ How to Use

1. **Generate Keys**:
   - Click "Generate Keys" to create a new public/private key pair. Enter the name for the key during generation.
   - The keys are saved in the `keys/` directory.

2. **Sign a File**:
   - Click "Sign a File" to select a file you want to sign.
   - Enter the path to your private key and the tool will create a `.signed` file with the signature.

3. **Sign a Directory**:
   - First, compress the directory you want to sign into a `.ZIP` file.
   - Then, click "Sign a File" and select the `.ZIP` file.
   - The tool will create the `.signed` file for the `.ZIP` file, and the public key will be saved in the `keys/` directory along with the signed file.

4. **Verify a File**:
   - Click "Verify a File" to select a signed file.
   - Enter the path to the corresponding public key to verify the file's signature.

---

## 📁 Generated File Structure  

| File                  | Description                                             |  
|-----------------------|---------------------------------------------------------|  
| `<name>.signed` | Contains the hash signed with the private key.              |  

---

## 🎨 Graphical Interface  

The DS-Sign-Tool interface has been designed for simplicity and ease of use:  
- **Generate Keys**: Create a new key pair with a single click.  
- **Sign File/Directory**: Select the file or directory to sign.  
- **Verify File/Directory**: Validate the integrity using a public key.  

![Capture d'écran 2024-11-25 214533](https://github.com/user-attachments/assets/14a9436c-987d-41a5-86ef-48e9cf009ee5)

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
   - `DS-Sign-Tool.exe`  

---

## 📚 Dependencies  

The libraries used in this project are listed in the `requirements.txt` file:  
- **cryptography**: Handles RSA keys and digital signatures.  
- **tkinterdnd2**: Provides the graphical user interface.  
- **PyQt5**: Provides the graphical user interface.

To install them manually:  
```bash
pip install cryptography tkinterdnd2
```  

---

## 💡 Notes

- Ensure that your keys are securely stored and backed up, as they are necessary for both signing and verification.
- When signing a directory, compress it to a `.ZIP` file before selecting it. You will get a `.signed` file and the public key, which should be stored together with the signed file.

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