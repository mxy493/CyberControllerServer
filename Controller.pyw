from TcpServer import TcpServer
from KeyboardListener import KeyboardListener
from service import *
from ComputerMonitor import ComputerMonitor
import json
from KeyboardManager import *


def on_message_received(data):
    command_message = json.loads(data)
    script = command_message["script"]
    params = command_message["params"]
    print(f'script: {script}')
    print(f'params: {params}')
    exec(script)  # 执行脚本


def on_screen_locked():
    print("screen locked")
    data = json.dumps({"command": 2, "message": ""})
    print(data)
    tcpServer.send_text(data)


computerMonitor = ComputerMonitor(on_screen_locked)


def on_tcp_connected():
    if not computerMonitor.started:
        computerMonitor.start()


def onTrans():
    print("need trans")
    content = getClipContent()
    text = json.dumps({"command": 1, "message": content})

    tcpServer.send_text(text)


if __name__ == '__main__':
    tcpServer = TcpServer()
    tcpServer.set_receive_listener(on_message_received)  # set listener for received message
    tcpServer.connected_listener = on_tcp_connected  # 当连接成功时调用, 监视屏幕锁定
    tcpServer.start()

    keyboardListener = KeyboardListener(tcpServer)
    keyboardListener.listen_keyboard(onTrans)
