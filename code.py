def chose_card(choices=[], chosen_cards=[]):
    """
    Determines the next card to take.
    Change function according to strategy.
    """
    print("PICK 0")


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
        self.can_attack = False

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
        print("SUMMON {}".format(str(self.instance_id)))

    def is_able_attack(self):
        return self.can_attack

    def attack(self, target_id=-1):
        print("ATTACK {} {}".format(str(self.instance_id), str(target_id)))



draft_phase = True
deck = []

# game loop
while True:
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

    if draft_phase:
        chose_card()

    print("PASS")
