from Crypto.Cipher import AES


def encrypt(key, plaintext):
    cipher = AES.new(key.to_bytes(16, "big"), AES.MODE_EAX)
    return [*cipher.encrypt_and_digest(plaintext), cipher.nonce]


def decrypt(key, ciphertext, tag, nonce):
    cipher = AES.new(key.to_bytes(16, "big"), AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
