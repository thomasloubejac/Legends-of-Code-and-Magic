import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
draw_phase = True
carte_a_choisir=[]
count = 0
first_turn = True

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

def creation_cards_lists (card_number, instance_id, location, card_type, cost, attack, defense, abilities):
    card=Card(card_number, instance_id, location, card_type, cost, attack, defense, abilities)
    if card.get_location()==0 :
        carte_en_main.append(card)

    elif card.get_location() == 1:
        carte_player_en_jeu.append(card)

    else:
        carte_enemi_en_jeu.append(card)
        print("1",file=sys.stderr)
    return carte_en_main, carte_player_en_jeu, carte_enemi_en_jeu

while True:
    carte_a_choisir = []
    carte_en_main = []
    carte_player_en_jeu = []
    carte_enemi_en_jeu = []

    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())
    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
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

        if (draw_phase):
            carte_a_choisir.append(Card( card_number, instance_id, location, card_type, cost, attack, defense, abilities))
        else:
            carte_en_main,carte_player_en_jeu,carte_enemi_en_jeu = creation_cards_lists (card_number, instance_id, location, card_type, cost, attack, defense, abilities)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    if (draw_phase):
            print("PICK 1")
            count+=1
            if (count == 30):
                draw_phase = False

    else:

        for i in carte_en_main:
            if (player_mana>=i.get_cost()):
                print ("SUMMON "+str(i.get_instance_id())+";")
        print(carte_en_main, file=sys.stderr)
        for i in carte_player_en_jeu:
            if (len(carte_enemi_en_jeu)!=0):
                print("ATTACK "+str(i.get_instance_id())+" "+str(carte_enemi_en_jeu[0].get_instance_id())+";")
            else:
                print("ATTACK "+str(i.get_instance_id())+" -1"+";")
        print ("PASS")
