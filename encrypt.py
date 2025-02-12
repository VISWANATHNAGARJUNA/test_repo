from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

key = get_random_bytes(32)  
with open("key.bin", "wb") as f:
    f.write(key)  
files_to_encrypt = ["script1.py", "script2.py", "script3.py"]  
output_files = ["script1.enc", "script2.enc", "script3.enc"]

for i in range(len(files_to_encrypt)):
    with open(files_to_encrypt[i], "rb") as f:
        content = f.read()

    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(content, AES.block_size))

    with open(output_files[i], "wb") as f:
        f.write(iv + ciphertext)

    print(f"Encryption complete for {files_to_encrypt[i]} -> {output_files[i]}")

print("Key saved as key.bin")
