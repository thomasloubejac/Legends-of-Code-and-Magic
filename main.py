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
    Choose the best decision to make during battle turns.
    """
    summon, green_items, red_items, blue_items, attackers = bdmger.availabilities()

    my_hand = bdmger.get_my_hand()
    my_mana = bdmger.me.get_player_mana()
    my_board = bdmger.get_my_board()
    enemys_board = bdmger.get_enemys_board()
    end_of_turn = False

    # 0=PASS 1=SUMMON 2=USE_GREEN 3=USE_RED 4=USE_BLUE 5=ATTACK
    action_to_make = random.randint(0,5)

    command = ""

    if (action_to_make == 1):
        if (len(summon)!=0):
            monster_to_summon = random.randint(0,len(summon)-1)
            command += "SUMMON {}; ".format(str(summon[monster_to_summon].get_instance_id()))
        else:
            while (action_to_make==1):
                action_to_make = random.randint(1,5)

    if (action_to_make == 2):
        if (len(attackers)!=0):
            if (len(green_items)!=0):
                green_item_to_use = random.randint(0,len(green_items)-1)
                attackers_to_use_on = random.randint(0,len(attackers)-1)
                command += "USE {} {}; ".format(str(green_items[green_item_to_use].get_instance_id()), str(attackers[attackers_to_use_on].get_instance_id()))
            else:
                while (action_to_make==2):
                    action_to_make = random.randint(0,5)
        else:
            while (action_to_make==2):
                action_to_make = random.randint(0,5)

    if (action_to_make == 3):
        if (len(enemys_board)!=0):
            if (len(red_items)!=0):
                red_item_to_use = random.randint(0,len(red_items)-1)
                enemy_to_use_on = random.randint(0,len(enemy_board)-1)
                command += "USE {} {}; ".format(str(red_items[red_item_to_use].get_instance_id()), str(enemys_board[enemy_to_use_on].get_instance_id()))
            else:
                while (action_to_make==3):
                    action_to_make = random.randint(0,5)
        else:
            while (action_to_make==3):
                action_to_make = random.randint(0,5)

    if (action_to_make == 4):
        if (len(blue_items)!=0):
            blue_item_to_use = random.randint(0,len(blue_items)-1)
            command += "USE {} {}; ".format(str(blue_items[blue_item_to_use].get_instance_id()))
        else:
            while (action_to_make==4):
                action_to_make = random.randint(0,5)

    if (action_to_make==5):
        if (len(attackers)!=0):
            attacker_who_attack = random.randint(0,len(attackers)-1)
            if (len(enemys_guard)!=0):
                enemy_to_attack = random.randint(0,len(enemys_guard)-1)
                command += "ATTACK {} {}; ".format(str(attackers[attacker_who_attack].get_instance_id()) ,str(enemys_guard[enemy_to_attack].get_instance_id()))
            else:
                enemy_to_attack = random.randint(-1,len(enemy_bord)-1)
                command += "ATTACK {} {}; ".format(str(attackers[attacker_who_attack].get_instance_id()) ,str(enemys_board[enemy_to_attack].get_instance_id()))
        else:
            while (action_to_make==4):
                action_to_make = random.randint(0,5)

    if (action_to_make==0):
        end_of_turn = True

    return end_of_turn


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

    def summon_card(self):
        """
        A terme : a virer
        """
        command = "SUMMON {}; ".format(str(self.instance_id))
        return command
        # print(command, file=sys.stderr)

    def attack_something(self, target_id=-1):
        """
        A terme : a virer
        """
        command = "ATTACK {} {}; ".format(str(self.instance_id), str(target_id))
        return command
        # print(command, file=sys.stderr)

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

        summon = [card.get_instance_id() for card in self.my_hand
        if
            (card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 0)
        ]

        green_items = [card.get_instance_id() for card in self.my_hand
        if
            card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 1
        ]

        red_items = [card.get_instance_id() for card in self.my_hand
        if
            card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 2
        ]

        blue_items = [card.get_instance_id() for card in self.my_hand
        if
            card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 3
        ]

        attackers = [card.get_instance_id() for card in self.my_board]

        attackers += [card.get_instance_id() for card in self.my_hand
        if
            card.get_cost() <= self.me.get_player_mana()
        and
            card.get_card_type() == 0
        and
            ("C" in card.get_abilities())
        ]
        print(attackers,file=sys.stderr)
        return summon, green_items, red_items, blue_items, attackers


class GameManager(object):
    """
    Controls game actions. Decision making happens here.
    """

    def __init__(self, bdmger):
        # self.command = ""
        self.bdmger = BoardManager(bdmger)

    def manages(self):
        """
        Choses actions to take and returns them in a command string
        """
        global count
        if count < 30:
            command = self.draw_phase()
        else:
            command = self.battle_phase()
        return command

    def draw_phase(self):
        """
        Choses cards to draw.
        """
        carte_choisie = chose_card(self.bdmger.cards_to_draw, self.bdmger.my_deck)
        self.bdmger.my_deck += [self.bdmger.cards_to_draw[carte_choisie]]
        command = "PICK {}".format(carte_choisie)
        return command

    def battle_phase(self):
        """
        Choses battle actions to take and returns them in a command string
        """
        return battle_actions(self.bdmger)


while True:
    bdmger = BoardManager()
    command = ""
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
    command = gMger.manages()

    count += 1

    if command == "":
        print("PASS")
    else :
        print(command, file=sys.stderr)
        print(command)
