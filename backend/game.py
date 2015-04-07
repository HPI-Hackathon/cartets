# All game related code

import json
import random


class Game():
    def __init__(self):
        self.players = {}
        self.turn = None
        self.running = False
        # TODO: Check if comparisons are good
        self.comparisons = {'price': min,
                            'power': max,
                            'milage': min,
                            'registration': min,
                            'consumption': min}

    def get_comparisons(self):
        return self.comparisons

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

        return self.handle_round(player)

    def handle_round(self, player):
        # TODO: Add actual functionality
        cards = [player.get_card() for player in self.players.values()]
        data = {'turn': self.turn, 'cards': cards}
        return json.dumps({'action': 'next', 'data': data})

    def start_game(self):
        name = random.choice(self.players.keys())
        self.turn = self.players[name]
        return self.turn


class Player():
    def __init__(self, conn, data):
        self.name = data['name']
        self.connection = conn
        self.cards = []
        self.current_card = None

    def get_name(self):
        return self.name

    def get_card(self):
        return self.current_card


class Card():
    def __init__(self, game):
        self.data = {}
        self.game_comp = game.get_comparisons()

    def compare(self, attr, cards):
        comp = self.game_comp[attr]
        winner_card = comp(cards)
        return winner_card
