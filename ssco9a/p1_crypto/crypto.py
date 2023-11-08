from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64


def encrypt(key, plaintext):
    cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(plaintext.encode("utf8"), 16))).decode(
        "utf8"
    )


def decrypt(key, ciphertext):
    cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(ciphertext)).decode("utf8")


key = "mysecretpassword"
plaintext = "Hello world!"
ciphertext = encrypt(key, plaintext)
decrypted_text = decrypt(key, ciphertext)

print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted text:", decrypted_text)
