
<div align="center">
  <img width="1318" alt="banner_png" src="icon/banner_png.png">

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

### ✅ **Enhanced Directory Signing**  
- **Improved Structure Validation**: A file named `dir_file` is generated to represent the directory tree.
- **Robust Hash Verification**: A `hash_file` is generated for the directory's structure hash, which is signed to ensure tamper-proof verification.
- **Flexible Tree Representation**: The directory tree includes emojis (`📁` for folders and `📄` for files) for clarity.

### ✅ **Signature Verification**  
- Verify the integrity and authenticity of a signed file using the public key.
- Directory verification now ensures both the structure and hash signature match the expected values.

### ✅ **Improved Graphical Interface**  
- Introduced a banner image in the main application window for a modern and polished appearance.
- Simplified navigation and file selection:
  - File signing.
  - Directory signing.
  - Signature verification.

### ✅ **All-in-One Script**  
- All functionality has been consolidated into a single Python script for easier deployment and management.
 
---

⚠️ Before installing the application, check if your OS can support it (Click here to see [all the versions available](https://github.com/ohymi04/DS_Sign_Tool/releases/tag/Note))

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
   - Click "Sign File/Folder" to select a file you want to sign.
   - Enter the path to your private key and the tool will create a `.signed` file with the signature.

3. **Sign a Directory**:
   - Select the directory you wish to sign directly.
   - The tool generates:
     - `dir_file`: Tree structure of the directory.
     - `hash_file`: SHA-256 hash of the tree structure.
     - `hash_file.signed`: Signed hash file for verification.

4. **Verify a File/Directory**:
   - Click "Verify File/Folder" to select a signed file or directory.
   - Enter the path to the corresponding public key to verify the signature and structure.

![Picture5](https://github.com/user-attachments/assets/e38cbc43-9772-4c3d-af81-5cce15a9aac4)

---

## 📁 Generated File Structure  

| File                  | Description                                             |  
|-----------------------|---------------------------------------------------------|  
| `<file>.signed`       | Contains the hash signed with the private key.          |  
| `dir_file`            | Represents the directory tree structure.               |  
| `hash_file`           | Contains the SHA-256 hash of `dir_file`.                |  
| `hash_file.signed`    | Signed hash of the directory tree for validation.       |  

---

## 🎨 Graphical Interface  

The DS-Sign-Tool interface has been designed for simplicity and ease of use:  
- **Generate Keys**: Create a new key pair with a single click.  
- **Sign File/Directory**: Select the file or directory to sign.  
- **Verify File/Directory**: Validate the integrity using a public key.  

![Picture4](https://github.com/user-attachments/assets/a9ec9175-fea3-4d7d-9ca5-901db1293ebe)

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
- **PyQt5**: Provides the graphical user interface.

To install them manually:  
```bash
pip install cryptography PyQt5
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