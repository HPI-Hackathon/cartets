import json
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


class CartetsServer(WebSocket):
    def handleMessage(self):
        data, value = to_json(self.data)

        if value == 'init':
            # New player connected
            game.add_player(self, data)
            game.check_for_start()

        if value == 'attributeSelected':
            # Attribute was selected
            game.attribute_selected(data)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'


if __name__ == '__main__':
    game = Game()
    server = SimpleWebSocketServer('', 8080, CartetsServer)
    server.serveforever()
