import thread
import json
import time
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from game import Game


def to_json(request):
    try:
        data = json.loads(request.decode('utf-8'))
        value = data['action']
    except Exception:
        data = {}
        value = ''
    return data, value


def client_thread(game, conn, data):
    player = game.add_player(conn, data)

    while True:
        answer_data = game.wait_for_answer(player)
        if answer_data:
            conn.sendMessage(answer_data)
        if game.get_turn() is player:
            while True:
                request = conn.wait()
                data, value = to_json(request)
                if value == 'selectedAttribute':
                    break
            game.attribute_selected(data)

    # Thread loop ended
    conn.sendClose()


class CartetsServer(WebSocket):
    def handleMessage(self):
        if not self.data:
            return {}
        data, value = to_json(self.data)

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
