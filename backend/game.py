# All game related code

import json
import random

import card_parser


class Game:
    def __init__(self):
        self.players = {}
        self.picked_cards = []

    def add_player(self, conn, data):
        player = Player(conn, data, self.picked_cards)
        self.players[player.get_name()] = player
        conn.sendMessage(json.dumps({'action': 'accepted', 'data': ''}))

    def check_for_start(self):
        if len(self.players) == 3:
            self.start_game()

    def attribute_selected(self, data):
        # Get all cards with players
        player_cards = self.players.items()
        cards = [(player, player.get_card()) for _, player in player_cards]
        all_card_values = [card.get_values() for player, card in cards]

        # Get current card and compare it
        attr = data['data']['attributeToCompare']
        winner, card = Card.compare(attr, cards)
        winner.add_cards([card for _, card in cards])
        data = {'all_cards': all_card_values, 'winner_card': card.get_values()}

        # Check if game has ended
        has_ended, player = self.check_game_end()
        if has_ended:
            data['loser'] = player
            has_next_round = True if len(self.players) > 1 else False
            self.broadcast(data, 'playerLost', next_card=has_next_round)
            if not has_next_round:
                self.end_connections()
            else:
                for p in player:
                    self.players[p].get_connection().sendClose()
                    del self.players[player]

        # Update after comparison
        data['turn'] = winner.get_name()
        data['attribute_compared'] = attr
        self.broadcast(data, 'next')

    def start_game(self):
        # Randomly select player to start
        random.seed(None)
        name, player = random.choice(self.players.items())
        data = {'turn': name}
        self.broadcast(data, 'start')

    def check_game_end(self):
        # Check if all players still have cards left
        has_ended = False
        players = []
        for name, player in self.players.items():
            if not player.has_cards():
                has_ended = True
                players.append(name)
        return has_ended, players

    def broadcast(self, data, action, next_card=True):
        # Send data to all players
        for name, player in self.players.items():
            if next_card:
                data['card'] = player.next_card()
            conn = player.get_connection()
            conn.sendMessage(json.dumps({'action': action, 'data': data}))

    def end_connections(self):
        # Close all connections
        for _, player in self.players.items():
            player.get_connection().sendClose()


class Player:
    def __init__(self, conn, data, picked_cards):
        self.name = data['name']
        self.connection = conn
        self.cards = self.receive_cards(data, picked_cards)
        self.current_card = None

    def get_name(self):
        return self.name

    def get_card(self):
        return self.current_card

    def get_connection(self):
        return self.connection

    def receive_cards(self, player_data, picked_cards):
        # Get card information from mobile.de API based on location
        long = player_data['data']['long']
        lat = player_data['data']['lat']
        cards = card_parser.main(lat, long, picked_cards)
        return [Card(json.loads(values)) for values in cards]

    def next_card(self):
        try:
            self.current_card = self.cards.pop(0)
        except:
            return {}
        return self.current_card.get_values()

    def add_cards(self, cards):
        try:
            self.cards.extend(cards)
        except:
            print "SOMETHING WENT WRONG!"

    def has_cards(self):
        return len(self.cards) > 0


class Card:
    comparisons = {'price': min,
                   'power': max,
                   'registration': max,
                   'mileage': min,
                   'consumption': min}

    def __init__(self, values):
        self.values = values

    @staticmethod
    def compare(attr, player_cards):
        # Select min or max according to selected attribute
        comp = Card.comparisons[attr]
        # Compare card value from (player, card) as float
        return comp(player_cards, key=lambda pair: float(pair[1].get(attr)))

    def get_values(self):
        return self.values

    def get(self, attr):
        return self.values[attr]
