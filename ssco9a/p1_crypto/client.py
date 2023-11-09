import asyncio
from crypto import encrypt
from diffie_hellman import calcula_pub, calcula_key
from websockets import connect
from json import loads

from hash import calcula_hash

host = "127.0.0.1"
port = 9898
kpr = 516
K = 0
file_name = "image.jpg"
file = open(file_name, "rb")
message = file.read()
file.close()


async def test():
    kpu = calcula_pub(kpr)
    async with connect(f"ws://{host}:{port}/public_key?key={kpu}") as websocket:
        response = loads(await websocket.recv())
        if response["success"]:
            K = calcula_key(response["kpu"], kpr)
            encrypted, tag, nonce = encrypt(K, message)
            await websocket.send(calcula_hash(file_name))
            await websocket.send(file_name)
            await websocket.send(encrypted)
            await websocket.send(tag)
            await websocket.send(nonce)
            recv = await websocket.recv()
            print(recv)


asyncio.run(test())
