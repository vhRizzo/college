import hashlib


def calcula_hash(file_name):
    sha256 = hashlib.sha256()
    with open(file_name, "rb") as arquivo:
        while True:
            bloco = arquivo.read(65536)  # Leitura em blocos de 64 KB
            if not bloco:
                break
            sha256.update(bloco)
    return sha256.hexdigest()
