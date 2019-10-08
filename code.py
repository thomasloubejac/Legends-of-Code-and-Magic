import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
draw_phase = True
count = 0
command = ""


def chose_card(choices=[]):
    """
    Chose the card to draw.
    To adapt according to strategy.
    """
    global cartes_choisies
    return random.randint(0,2)


class Card(object):
    def __init__(self, card_number, instance_id, location, card_type, cost,
    attack, defense, abilities):
        self.card_number = card_number
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.abilities = abilities

    def get_card_number(self):
        return self.card_number

    def get_instance_id(self):
        return self.instance_id

    def get_location(self):
        return self.location

    def get_card_type(self):
        return self.card_type

    def get_cost(self):
        return self.cost

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_abilities(self):
        return self.abilities

    def summon_card(self):
        global command
        command += "SUMMON {}; ".format(str(self.instance_id))
        print(command, file=sys.stderr)

    def attack_something(self, target_id=-1):
        global command
        command += "ATTACK {} {}; ".format(str(self.instance_id), str(target_id))
        print(command, file=sys.stderr)


class BoardManager(object):
    """
    Data structure to handle cards in game.
    """

    def __init__(self):
        self.my_hand = []
        self.my_board = []
        self.enemys_board = []
        self.my_deck = []
        self.cards_to_draw = []

    def add(self, card):
        """
        Adds a card to the data structure
        """
        global count

        if count < 30:
            self.cards_to_draw += [card]

        if not (card is Card):
            print(type(card), file=sys.stderr)

        if card.get_location() == 0:
            self.my_hand += [card]

        if card.get_location() == 1:
            self.my_board += [card]

        if card.get_location() == -1:
            self.enemys_board += [card]

    def get_my_hand(self):
        """
        my_hand attribute getter
        """
        return self.my_hand

    def get_my_board(self):
        """
        my_board attribute getter
        """
        return self.my_board

    def get_enemys_board(self):
        """
        enemys_board attribute getter
        """
        return self.enemys_board

    def draw_card(self):
        """
        Draws a card.
        """
        global command
        carte_choisie = chose_card(self.cards_to_draw)
        self.my_deck += [self.cards_to_draw[carte_choisie]]
        command += "PICK {}".format(carte_choisie)


bdmger = BoardManager()


while True:
    bdmger = BoardManager()
    command = ""
    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = \
        [int(j) for j in input().split()]
    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, \
        abilities, my_health_change, opponent_health_change, card_draw \
        = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        my_health_change = int(my_health_change)
        opponent_health_change = int(opponent_health_change)
        card_draw = int(card_draw)

        card = Card(card_number, instance_id, location, card_type, cost,
        attack, defense, abilities)
        bdmger.add(card)

    if (count < 30):
            bdmger.draw_card()
            print(count, file=sys.stderr)

    else:
        for i in bdmger.get_my_hand():
            if (player_mana >= i.get_cost()):
                i.summon_card()
        for i in bdmger.get_my_board():
            for j in bdmger.get_enemys_board():
                if ("G" in j.get_abilities()):
                    i.attack_something(j.get_instance_id())
                else:
                    i.attack_something()

    count += 1

    if command == "":
        print("PASS")
    else :
        print(command, file=sys.stderr)
        print(command)
