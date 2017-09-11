import socketIO_client
import websocket
import json
import random
import uuid
import threading

socketIO = socketIO_client.SocketIO('localhost', 8000, socketIO_client.LoggingNamespace)

printer_ip= "192.168.0.19"

class sockJSWebsocket(object):
    '''
    https://pypi.python.org/pypi/websocket-client
    https://wiki.python.org/moin/PyQt/Threading,_Signals_and_Slots
    '''

    def __init__(self):
        websocket.enableTrace(True)
        url = "ws://{}/sockjs/{:0>3d}/{}/websocket".format(
            printer_ip,  # host + port + prefix, but no protocol
            random.randrange(0, stop=999),  # server_id
            uuid.uuid4()  # session_id
        )
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    def run(self):
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def on_message(self, ws, message):

        message_type = message[0]
        if message_type == "h":
            # "heartbeat" message
            return
        elif message_type == "o":
            # "open" message
            return
        elif message_type == "c":
            # "close" message
            return

        message_body = message[1:]
        if not message_body:
            return
        data = json.loads(message_body)[0]

        if message_type == "m":
            data = [data, ]

        if message_type == "a":
            socketIO.emit(data)

    def on_open(self, ws):
        pass

    def on_close(self, ws):
        pass

    def on_error(self, ws, error):
        pass

if __name__ == "__main__":
    sockJSClient = sockJSWebsocket
    sockJSClient.run()



