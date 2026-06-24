from socket import *
from threading import Thread, Lock

isInput = True # 是否输入
lock = Lock()
def send_msg(s, ip, port):
    global isInput
    while True:
        with lock:
            if not isInput:
                continue
        msg = input("请输入发送信息>>:")
        s.sendto(msg.encode("utf-8"), (ip, port))
        with lock:
            isInput = False


def recv_msg(s):
    global isInput
    while True:
        msg, addr = s.recvfrom(1024)
        print(f"从{addr}接受到消息<<:{msg.decode("utf-8")}")
        with lock:
            isInput = True



if __name__ == "__main__":
    # 对方端口和IP
    send_port = 8888
    send_ip = "127.0.0.1"
    # 创建套接字和线程
    s=socket(AF_INET, SOCK_DGRAM)
    s.bind(("127.0.0.1", 9999))
    send_thread = Thread(target=send_msg, args=(s, send_ip, send_port))
    recv_thread = Thread(target=recv_msg, args=(s,))
    # 启动线程
    send_thread.start()
    recv_thread.start()
    # 等待线程结束
    send_thread.join()
    recv_thread.join()
    # 关闭套接字
    s.close()
