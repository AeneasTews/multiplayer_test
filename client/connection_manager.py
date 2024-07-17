import asyncio
import websockets
import requests
from hashlib import sha256
import json


# TODO: make sure everything is either " or ' or check what the convention specifies

class ConnectionManager:
    def __init__(self):
        # setup
        self.websocket = None
        self.uri = 'ws://localhost:8080'
        self.login_data = None
        self.loop = asyncio.new_event_loop()

    def login(self, username, password, car):
        passwd_hash = sha256(password.encode('utf-8')).hexdigest()
        if not self.handle_login_request(username, passwd_hash, car):
            print("Failed to authenticate")

        print('Attempting login...')
        return asyncio.run(self.establish_ws_connection())

    async def establish_ws_connection(self):
        #self.websocket = await websockets.connect(self.uri)
        self.websocket = self.loop.create_connection()
        try:
            message = {'action': 'login', 'data': self.login_data}
            await self.websocket.send(json.dumps(message))

            state = await self.websocket.recv()
            state = json.loads(state)
            print(state)
            if not state['result'] == 'success':
                await self.websocket.close()
                return False

            return True

        except websockets.exceptions.WebSocketException as e:
            print(e)

        return False

    def handle_login_request(self, username, passwd_hash, car):
        self.login_data = {'username': username, 'passwd_hash': passwd_hash, 'car': car}
        api_url = "http://localhost:3000/"

        data = {
            "username": username,
            "passwd_hash": passwd_hash,
        }

        res = requests.post(api_url + "login", json=data, headers={'Content-Type': 'application/json'})
        return True if res.json()["status"] == "success" else False

    async def send_update(self, data):
        if not self.websocket:
            return False

        message = {
            "action": "update_position",
            "data": {
                "x": data["position"].x,
                "y": data["position"].y,
                "angle": data["angle"],
            },
        }

        await self.websocket.send(json.dumps(message))

    async def update_positions(self, data):
        await self.send_update(data)
        state = await self.websocket.recv()
        state = json.loads(state)
        print(state)

    async def test_send(self, data):
        if not self.websocket:
            return False

        message = {
            "action": "update_position",
            "data": data
        }

        await self.websocket.send(json.dumps(message))
        state = await self.websocket.recv()
        state = json.loads(state)
        print(state)
