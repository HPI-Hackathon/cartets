# All game related code

import json
import random


class Game():
    def __init__(self):
        self.players = {}
        self.turn = None
        self.running = False

    def add_player(self, conn, data):
        player = Player(conn, data)
        self.players[player.get_name()] = player
        conn.send(json.dumps({'action': 'accepted', 'data': ''}))
        return player

    def wait_for_answer(self, player):
        # Initial start of game
        if not self.running() and len(self.players) == 3:
            starter = self.start_game()
            data = {'turn': starter.get_name(), 'cards': []}
            return json.dumps({'action': 'start', 'data': data})

        return self.handle_round(self, player)

    def handle_round(self, player):
        pass

    def start_game(self):
        self.turn = random.choice(self.players)
        return self.turn


class Player():
    def __init__(self, conn, data):
        self.name = data['name']
        self.connection = conn
        self.cards = []

    def get_name(self):
        return self.name


class Card():
    def __init__(self):
        pass
