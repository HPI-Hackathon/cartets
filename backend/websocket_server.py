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
            print "It's", player.get_name(), "'s turn."
            while True:
                print "Server is waiting..."
                request = conn.wait()
                data, value = to_json(request)
                print "Data from", player.get_name(), ":", data
                if value == 'selectedAttribute':
                    break
            print "An attribute was selected."
            game.attribute_selected(data)

    # Thread loop ended
    conn.sendClose()


class CartetsServer(WebSocket):
    def handleMessage(self):
        data, value = to_json(self.data)

        print "value", value
        if value == 'init':
            player = game.add_player(self, data)
            answer_data = game.wait_for_answer(player)
            if answer_data:
                self.sendMessage(answer_data)

        if value == 'attributeSelected':
            game.attribute_selected(data)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

    def wait(self):
        while True:
            data = self.handlePacket()
            if data:
                break
            else:
                time.sleep(0.01)
        print "Finished waiting :) for:", data
        return data


game = Game()
server = SimpleWebSocketServer('', 8080, CartetsServer)
server.serveforever()
