import asyncio
import websockets
import requests
from hashlib import sha256


def login(username, password):
    username = username
    passwd_hash = sha256(password.encode('utf-8')).hexdigest()
    if not handle_login_request(username, passwd_hash):
        print("Failed to authenticate")

    establish_ws_connection()
    # TODO: work on establishing a ws connection; also check whether the user actually exists


def establish_ws_connection():
    pass


def handle_login_request(username, passwd_hash):
    api_url = "http://localhost:3000/"

    data = {
        "username": username,
        "passwd_hash": passwd_hash
    }

    res = requests.post(api_url + "login", json=data, headers={'Content-Type': 'application/json'})
    return True if res.json()["status"] == "success" else False


async def hello():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as ws:
        name = input("What's your name?")

        await ws.send(name)
        print(f">>> {name}")

        greeting = await ws.recv()
        print(f"<<< {greeting}")


if __name__ == '__main__':
    asyncio.run(hello())
