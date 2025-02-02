import os
import sqlite3
import json
import base64
import shutil
from Crypto.Cipher import AES
import win32crypt
from tqdm import tqdm  # Import tqdm for the progress bar

# Program Information
PROGRAM_NAME = "Chrome Password Extractor"
VERSION = "1.0"
MANUFACTURER = "Yassine_Douadi(CipherX)."

print(f"{PROGRAM_NAME} - Version {VERSION} by {MANUFACTURER}")

# Function to decrypt Chrome passwords
def decrypt_password(buff, key):
    try:
        iv = buff[3:15]  # Extract IV correctly
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16]  # Remove authentication tag
        return decrypted_pass.decode()
    except Exception:
        return None  # Return None instead of printing errors to avoid breaking tqdm

# Function to get the encryption key
def get_encryption_key():
    local_state_path = os.path.join(os.environ['LOCALAPPDATA'],
                                    'Google', 'Chrome', 'User Data', 'Local State')
    if not os.path.exists(local_state_path):
        print("Error: Local State file not found.")
        return None

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix

    try:
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return key
    except Exception as e:
        print(f"Failed to decrypt the encryption key: {e}")
        return None

# Function to fetch and decrypt passwords
def fetch_chrome_passwords():
    key = get_encryption_key()
    if not key:
        print("Failed to retrieve encryption key.")
        return

    # Display encryption key in hexadecimal format
    print(f"Encryption key: {key.hex()}")

    db_path = os.path.join(os.environ['LOCALAPPDATA'],
                           'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    
    if not os.path.exists(db_path):
        print("Chrome password database not found.")
        return

    temp_db_path = os.path.join(os.environ['TEMP'], 'chrome_login_data.db')

    try:
        shutil.copy2(db_path, temp_db_path)  # Copy database to avoid lock issues
    except Exception as e:
        print(f"Failed to copy database: {e}")
        return

    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        rows = cursor.fetchall()
    except Exception as e:
        print(f"Failed to fetch data from database: {e}")
        conn.close()
        os.remove(temp_db_path)
        return

    # Open a text file to save the passwords
    with open('chrome_passwords.txt', 'w', encoding='utf-8') as file:
        with tqdm(total=len(rows), desc="Decrypting passwords", ncols=100) as pbar:
            for row in rows:
                origin_url, username, encrypted_password = row
                decrypted_password = decrypt_password(encrypted_password, key)

                if decrypted_password:
                    file.write(f"URL: {origin_url}\n")
                    file.write(f"Username: {username}\n")
                    file.write(f"Password: {decrypted_password}\n")
                    file.write("-" * 50 + "\n")

                pbar.update(1)  # Update progress bar

    conn.close()
    os.remove(temp_db_path)  # Clean up temp file
    print("Passwords saved to chrome_passwords.txt")

if __name__ == "__main__":
    print("WARNING: This script accesses sensitive login data stored by Google Chrome.")
    print("Ensure you have proper authorization before proceeding.")
    confirmation = input("Do you want to continue? (yes/no): ").strip().lower()
    
    if confirmation == "yes":
        print("Fetching Chrome passwords...")
        fetch_chrome_passwords()  # Correct function call
    else:
        print("Operation canceled.")
