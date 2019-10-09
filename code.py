import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
count = 0

def chose_card(choices=[],my_deck=[]):
    """
    Chose the card to draw.
    To adapt according to strategy.
    """
    global cartes_choisies
    return random.randint(0,2)

def battle_actions(bdmger):
    """
    Makes decisions during battle turns.
    """
    summon, green_items, red_items, blue_items, attackers = bdmger.availabilities()

    my_hand = bdmger.get_my_hand()
    my_mana = bdmger.me.get_player_mana()
    my_board = bdmger.get_my_board()
    enemys_board = bdmger.get_enemys_board()

    for i in summon:
        bdmger.summon(i)

    if len(attackers)!=0:
        for i in green_items:
            target = attackers[random.randint(0,len(attackers)-1)]
            bdmger.use(i,target)

    if len(enemys_board)!=0:
        for i in red_items:
            target = enemys_board[random.randint(0,len(enemys_board)-1)]
            bdmger.use(i,target)

    for i in blue_items:
        pass

    for i in attackers:
        target = None
        for j in enemys_board:
            if ("G" in j.get_abilities()):
                target = j
        bdmger.attack(i,target)


class Card(object):
    """
    Data structure to handle card information.
    """
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


class Hero(object):
    """
    Handles Hero information.
    """

    def __init__(self, player_health, player_mana, player_deck, player_rune, player_draw):
        """
        player_health, player_mana are self explanatory
        player_deck is the number of cards left in the deck.
        player_rune is how tf would I know.
        player_draw is the number of cards drawn during this turn.
        """
        self.player_health, self.player_mana, self.player_deck, self.player_rune, self.player_draw = \
        player_health, player_mana, player_deck, player_rune, player_draw

    def get_player_health(self):
        return self.player_health

    def get_player_mana(self):
        return self.player_mana

    def get_player_deck(self):
        return self.player_deck

    def get_player_rune(self):
        return self.player_rune

    def get_player_draw(self):
        return self.player_draw

    def pay_mana(self, cost):
        self.player_mana -= cost

def process_opponent_actions(card_numbers_and_actions):
    """
    Process opponent actions.
    """
    return []

class BoardManager(object):
    """
    Data structure to handle game information.
    Don't do any default actions in __init__,
    to avoid draw and battle phases conflicts.
    """

    def __init__(self, bdmger=None):
        self.my_hand = []
        self.my_board = []
        self.enemys_board = []
        self.my_deck = []
        self.cards_to_draw = []
        self.me = None

        self.opponent_hero = None
        self.opponent_actions = []
        self.opponent_hand = 0

        self.command = ""

        if not (bdmger is None):
            self.my_hand = bdmger.my_hand
            self.my_board = bdmger.my_board
            self.enemys_board = bdmger.enemys_board
            self.my_deck = bdmger.my_deck
            self.cards_to_draw = bdmger.cards_to_draw
            self.me = bdmger.me

            self.opponent_hero = bdmger.opponent_hero
            self.opponent_actions = bdmger.opponent_actions
            self.opponent_hand = bdmger.opponent_hand

    def add_card(self, card):
        """
        Adds a card to the correct data structure attribute.
        """
        global count

        if not (card is Card):
            pass #print(type(card), file=sys.stderr)

        if count < 30:
            self.cards_to_draw += [card]

        else:
            if card.get_location() == 0:
                self.my_hand += [card]

            if card.get_location() == 1:
                self.my_board += [card]

            if card.get_location() == -1:
                self.enemys_board += [card]

    def add_hero(self, hero):
        """
        Stores Hero informations.
        """
        if self.me is None:
            self.me = hero
        elif self.opponent_hero is None:
            self.opponent_hero = hero
        else:
            # you're doing something wrong
            print("Adding hero in bdmger while heroes already set", file=sys.stderr)

    def add_opponent_informations(self, opponent_hand, card_numbers_and_actions):
        """
        collects and stores non hero opponent informations
        """
        self.opponent_actions = process_opponent_actions(card_numbers_and_actions)
        self.opponent_hand = opponent_hand


    def get_my_hand(self):
        """
        my_hand attribute getter.
        """
        return self.my_hand

    def get_my_board(self):
        """
        my_board attribute getter.
        """
        return self.my_board

    def get_enemys_board(self):
        """
        enemys_board attribute getter.
        """
        return self.enemys_board

    def summon(self, card):
        """
        Applique une directive d'invocation.
        """
        id = str(card.get_instance_id())
        self.command += "SUMMON {}; ".format(id)
        self.me.pay_mana(card.get_cost())
        # print(command, file=sys.stderr)

    def attack(self, card, target_card=None):
        """
        Applique une directive d'attaque.
        """
        id = str(card.get_instance_id())
        target_id = -1
        if not(target_card is None):
            target_id = target_card.get_instance_id()
        self.command += "ATTACK {} {}; ".format(id, str(target_id))
        # print(command, file=sys.stderr)

    def use(self, item, target):
        """
        Applique une directive d'attaque.
        """
        id = str(item.get_instance_id())
        target_id = str(target.get_instance_id())
        self.command += "USE {} {}; ".format(id, target_id)
        self.me.pay_mana(item.get_cost())

    def availabilities(self):
        """
        Returns a list of command strings giving possible actions to take.
        Ex : ["SUMMON 1;","ATTACK 3 -1;"]

        Est-ce la bonne chose a faire ?
        Ca fait bcp bcp de combinaisons, on devrait peut-être se limiter
        a donner
        [
        qui peut attaquer (rajouter les creatures dans la main avec charge)
        qui peut etre summon
        quel item peut etre use
        ]
        (qui peut etre attaque : bah toutes les creatures du board adverse + leur hero)
        l'IA fera le reste de l'analyse toute seule
        """

        summon = [card for card in self.my_hand
        if
            ((card.get_cost() <= self.me.get_player_mana())
        and
            (card.get_card_type() == 0))
        ]

        green_items = [card for card in self.my_hand
        if
            ((card.get_cost() <= self.me.get_player_mana())
        and
            (card.get_card_type() == 1))
        ]

        red_items = [card for card in self.my_hand
        if
            (card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 2)
        ]

        blue_items = [card for card in self.my_hand
        if
            (card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 3)
        ]

        attackers = [card for card in self.my_board]

        attackers += [card for card in self.my_hand
        if
            (card.get_cost() <= self.me.get_player_mana())
        and
            (card.get_card_type() == 0)
        and
            ("C" in card.get_abilities())
        ]

        return summon, green_items, red_items, blue_items, attackers


class GameManager(object):
    """
    Controls game actions. Decision making happens here.
    """

    def __init__(self, bdmger):
        self.bdmger = BoardManager(bdmger)

    def manages(self):
        """
        Choses actions to take and returns them in a command string
        """
        global count
        if count < 30:
            self.draw_phase()
        else:
            self.battle_phase()

    def draw_phase(self):
        """
        Choses cards to draw.
        """
        carte_choisie = chose_card(self.bdmger.cards_to_draw, self.bdmger.my_deck)
        self.bdmger.my_deck += [self.bdmger.cards_to_draw[carte_choisie]]
        command = "PICK {}".format(carte_choisie)
        self.bdmger.command = command

    def battle_phase(self):
        """
        Choses battle actions to take and returns them in a command string
        """
        battle_actions(self.bdmger)


while True:
    bdmger = BoardManager()
    card_numbers_and_actions = []

    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = \
        [int(j) for j in input().split()]
        hero = Hero(player_health, player_mana, player_deck, player_rune, player_draw)
        bdmger.add_hero(hero)

    opponent_hand, opponent_actions = [int(i) for i in input().split()]

    for i in range(opponent_actions):
        card_numbers_and_actions += [input()]
    bdmger.add_opponent_informations(opponent_hand, card_numbers_and_actions)

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
        bdmger.add_card(card)

    gMger = GameManager(bdmger)
    gMger.manages()

    command = gMger.bdmger.command

    count += 1

    if command == "":
        print("PASS")
    else :
        print(command, file=sys.stderr)
        print(command)
