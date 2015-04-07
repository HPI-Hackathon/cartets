# All game related code

import json
import random

import card_parser


class Game:
    def __init__(self):
        self.players = {}
        self.turn = None
        self.running = False

    def add_player(self, conn, data):
        player = Player(conn, data)
        self.players[player.get_name()] = player
        conn.sendMessage(json.dumps({'action': 'accepted', 'data': ''}))
        return player

    def wait_for_answer(self, player):
        # Initial start of game
        if not self.running() and len(self.players) == 3:
            starter = self.start_game()
            data = {'turn': starter.get_name(), 'cards': []}
            # TODO: hand out cards
            return json.dumps({'action': 'start', 'data': data})

        return self.handle_round(player)

    def handle_round(self, player):
        # TODO: Add actual functionality
        cards = [player.get_card() for player in self.players.values()]
        # Only hand out current card
        data = {'turn': self.turn.get_name(), 'cards': cards}
        return json.dumps({'action': 'next', 'data': data})

    def start_game(self):
        name = random.choice(self.players.keys())
        self.turn = self.players[name]
        return self.turn


class Player:
    def __init__(self, conn, data):
        self.name = data['name']
        self.connection = conn
        self.cards = self.receive_cards(data)
        self.current_card = None

    def get_name(self):
        return self.name

    def get_card(self):
        return self.current_card

    def receive_cards(self, player_data):
        long = player_data['data']['long']
        lat = player_data['data']['lat']
        cards = card_parser.main(lat, long)
        self.cards = [Card(values) for values in cards]


class Card:
    def __init__(self, values):
        self.values = values
        # TODO: Check if comparisons are good
        self.comparisons = {'price': min,
                            'power': max,
                            'mileage': min,
                            'registration': min,
                            'consumption': min}

    def compare(self, attr, cards):
        comp = self.comparisons[attr]
        winner_card = comp(cards)
        return winner_card
