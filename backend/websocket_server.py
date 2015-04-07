import thread
import json
import time
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from game import Game


def client_thread(game, conn, data):
    player = game.add_player(conn, data)

    while True:
        answer_data = game.wait_for_answer(player)
        if answer_data:
            conn.sendMessage(answer_data)
        request = conn.wait()
        print request

    # Thread loop ended
    conn.sendClose()


class CartetsServer(WebSocket):
    def handleMessage(self):
        if not self.data:
            return {}
        try:
            data = json.loads(self.data.decode('utf-8'))
            value = data['action']
        except Exception:
            data = {}
            value = ''

        if value == 'init':
            thread.start_new_thread(client_thread, (game, self, data))

        # self.sendMessage(str(self.data))
        return data

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

    def wait(self):
        while True:
            data = self.handleMessage()
            if data:
                break
            else:
                time.sleep(0.5)
        return data


game = Game()
server = SimpleWebSocketServer('', 8080, CartetsServer)
server.serveforever()
