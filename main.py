import time

from connection import ResReqClient, UMClient


def socket_test() -> None:
    addr = ("localhost", 8008)

    s = ResReqClient()
    s.connect(addr)
    ping(s)
    response = register_user(s, "test2")
    uname = response.body.user.uname
    # sleep for 2 secs
    time.sleep(1)
    um_client = UMClient(uname, addr)
    um_client.start()

    time.sleep(30)
    s.close()
    um_client.close()


if __name__ == '__main__':
    socket_test()
