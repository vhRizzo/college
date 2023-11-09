import asyncio
from crypto import decrypt
from diffie_hellman import calcula_pub, calcula_key
from websockets.server import serve
from urllib.parse import urlparse
from urllib.parse import parse_qs
from json import dumps

from hash import calcula_hash

host = "127.0.0.1"
port = 9898
kpr = 732
K = 0


# create handler for each connection
async def handler(websocket, path):
    kpu = calcula_pub(kpr)
    reply = dumps(
        {
            "success": True,
            "kpu": kpu,
        }
    )
    await websocket.send(reply)
    other_kpu = int(parse_qs(urlparse(path).query)["key"][0])
    K = calcula_key(other_kpu, kpr)
    recv_sha = await websocket.recv()
    file_name = await websocket.recv()
    encrypted = await websocket.recv()
    tag = await websocket.recv()
    nonce = await websocket.recv()
    decrypted = decrypt(K, encrypted, tag, nonce)
    output = open(f"out_{file_name}", "wb")
    output.write(decrypted)
    output.close()
    send_sha = calcula_hash(f"out_{file_name}")
    print(f"Hash original:\t\t{recv_sha}")
    print(f"Hash após decriptação:\t{send_sha}")
    message = "Arquivo corrompido ou adulterado!"
    if recv_sha == send_sha:
        message = "Hashs compatíveis!"
    print(message)
    await websocket.send(message)


async def main():
    async with serve(handler, host, port):
        await asyncio.Future()


asyncio.run(main())
