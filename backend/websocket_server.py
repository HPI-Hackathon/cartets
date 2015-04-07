import thread
import json
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from game import Game


def client_thread(game, conn, data):
    player = game.add_player(conn, data)
    print player


class CartetsServer(WebSocket):
    def handleMessage(self):
        try:
            data = json.loads(self.data.decode('utf-8'))
            value = data['action']
        except Exception:
            data = ''
            value = ''

        if type(data) is dict and value == 'init':
            thread.start_new_thread(client_thread, (game, self, data))

        # self.sendMessage(str(self.data))

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

game = Game()
server = SimpleWebSocketServer('', 8080, CartetsServer)
server.serveforever()
