# All game related code

import json
import random

import card_parser


class Game:
    def __init__(self):
        self.players = {}
        self.turn = None
        self.running = False
        self.is_evaluated = False

    def get_turn(self):
        return self.turn

    def add_player(self, conn, data):
        player = Player(conn, data)
        self.players[player.get_name()] = player
        conn.sendMessage(json.dumps({'action': 'accepted', 'data': ''}))
        print "Added player:", player.get_name()
        return player

    def wait_for_answer(self, player):
        # Initial start of game
        if not self.running:
            if len(self.players) == 3:
                self.start_game()
                self.running = True
                return
            else:
                return
        return

    def attribute_selected(self, data):
        # Get all cards with players
        player_cards = self.players.items()
        cards = [(player, player.get_card()) for name, player in player_cards]
        all_cards = [card.get_values() for player, card in cards]

        # Get current card and compare it
        cur_card = cards[[x for x, _ in cards].index(self.turn)][1]
        attr = data['data']['attributeToCompare']
        winner, card = cur_card.compare(attr, cards)

        # Update after comparison
        self.turn = winner
        winner.add_cards([card for _, card in cards])
        data = {'turn': winner.get_name()}
        data['all_cards'] = all_cards
        data['winner_card'] = card.get_values()
        self.is_evaluated = True
        self.broadcast(data)

    def start_game(self):
        random.seed(None)
        name = random.choice(self.players.keys())
        self.turn = self.players[name]
        data = {'turn': name}
        self.running = True
        self.broadcast(data)

    def broadcast(self, data):
        for name, player in self.players.items():
            data['card'] = player.next_card()
            conn = player.get_connection()
            conn.sendMessage(json.dumps({'action': 'start', 'data': data}))


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

    def get_connection(self):
        return self.connection

    def receive_cards(self, player_data):
        long = player_data['data']['long']
        lat = player_data['data']['lat']
        cards = card_parser.main(lat, long)
        return [Card(json.loads(values)) for values in cards]

    def next_card(self):
        self.current_card = self.cards.pop(0)
        return self.current_card.get_values()

    def add_cards(self, cards):
        self.cards.extend(cards)


class Card:
    def __init__(self, values):
        self.values = values
        # TODO: Check if comparisons are good
        self.comparisons = {'price': min,
                            'power': max,
                            'mileage': min,
                            'registration': max,
                            'consumption': min}

    def compare(self, attr, player_cards):
        comp = self.comparisons[attr]
        for player, card in player_cards:
            print card.get_values()
        res = comp(player_cards, key=lambda pair: float(pair[1].get(attr)))
        print res
        return res

    def get_values(self):
        return self.values

    def get(self, attr):
        return self.values[attr]
