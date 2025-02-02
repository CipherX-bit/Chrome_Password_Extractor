# Chrome Password Extractor

## Description
Chrome Password Extractor is a Python script designed to retrieve and decrypt saved passwords from Google Chrome. It utilizes the Windows Data Protection API (DPAPI) to decrypt stored credentials securely.

## Features
- Extracts saved login credentials from Google Chrome.
- Decrypts passwords using the system's encryption key.
- Saves the extracted data to a text file.
- Displays a progress bar using `tqdm`.

## Prerequisites
- Windows OS
- Python 3.x
- Google Chrome installed

## Dependencies
Ensure you have the following Python packages installed:
```bash
pip install pycryptodome pypiwin32 tqdm
```

## Installation
1. Clone or download the repository:
```bash
git clone https://github.com/CipherX-bit/Chrome-Password-Extractor.git
cd Chrome-Password-Extractor
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script with administrator privileges:
```bash
python script.py
```
You will be prompted to confirm the execution before extracting any passwords.

## Security Warning
⚠️ **This script accesses sensitive data. Use it only on systems you own or have permission to access. Unauthorized usage is illegal.**

## License
This project is for educational purposes only. The author is not responsible for any misuse of this script.

