import json
import socket
import sys
from threading import Thread
from types import SimpleNamespace

from model import User, UID

UM_HANDLERS = dict()


def um_handler(func):
    UM_HANDLERS[func.__name__] = func
    print(f'Added handler for {func.__name__}')
    return func


class ResReqClient(socket.socket):
    def __int__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def request(self, req: json) -> SimpleNamespace:
        req = f'{json.dumps(req)}\n'
        self.send(req.encode("utf-8"))
        data = self.recv(1024).decode("utf-8")
        return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


class UMClient(ResReqClient, Thread):
    def __init__(self, main_user: str, addr: tuple) -> None:
        ResReqClient.__init__(self)
        Thread.__init__(self)
        self.connect(addr)
        req = {"request-id": "su", "params": {"main-user": f'{main_user}'}}
        print(f"Setting um connection with main user {main_user}")
        res = self.request(req)
        print(res)

    def run(self):
        try:
            while (data := self.recv(1024).decode("utf-8")) is not None:
                msg = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
                print(msg)
                key = getattr(msg, 'update-message')
                print(key)
                if key in UM_HANDLERS:
                    UM_HANDLERS[key](msg)
                else:
                    print(f'No handler for {key}')
        except:
            self.close()
            print("Connection closed")


res_req_conn: ResReqClient
um_conn: UMClient

assoc_user: User


def ping(client: ResReqClient) -> None:
    print(client.request({"request-id": "ping"}))


def register_user(client: ResReqClient, username: str) -> SimpleNamespace:
    return client.request({"request-id": "ru", "params": {"uname": username}})


def send_message(client: ResReqClient) -> SimpleNamespace:
    pass


def get_user_list(client: ResReqClient) -> SimpleNamespace:
    pass


def establish_voxx_connection(user: str, addr: tuple):
    global res_req_conn
    global um_conn
    global assoc_user
    try:
        res_req_conn = ResReqClient()
        res_req_conn.connect(addr)

        res = register_user(res_req_conn, user)
        if getattr(res, 'response-id') == 0:
            print(res.body.message)
            sys.exit(1)
        uid_int = int(res.body.user.uid)
        assoc_user = User(res.body.user.uname, UID.of(uid_int))


    except TimeoutError | InterruptedError:
        print(f'Could not connect to server {addr}')
        sys.exit(1)
