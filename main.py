import sys
import math
import random
from copy import deepcopy
import signal
from contextlib import contextmanager


count = 0
hero_letal = False

# Weigths Draw

weight_draw_breakthrought = 1
weight_draw_charge = 1
weight_draw_drain = 1.5
weight_draw_guard = 2
weight_draw_letal = 5
weight_draw_ward = 3
weight_draw_attack = 1
weight_draw_cost = 2
weight_draw_defense = 1
weight_draw_opponent = 0
weight_draw_healthchange = 1/4
weight_draw_drawcard = 2

# Weigths Battle

weight_battle_breakthrought = 1
weight_battle_charge = 1
weight_battle_drain = 1.5
weight_battle_guard = 2
weight_battle_letal = 5
weight_battle_ward = 3
weight_battle_attack = 1
weight_battle_cost = 1
weight_battle_defense = 1
weight_battle_opponent = 1.5
weight_battle_healthchange = 0
weight_battle_drawcard = 2

# Weigths Hero in Battle

weight_health = 1/4
weight_deck = 1/6
weight_mana = 4
weight_rune = 1
weight_hand = 1

# Wheights lists

weights_draw_card = [weight_draw_breakthrought, weight_draw_charge, weight_draw_drain, weight_draw_guard, weight_draw_letal, weight_draw_ward, weight_draw_attack, weight_draw_cost, weight_draw_defense, weight_draw_opponent, weight_draw_healthchange, weight_draw_drawcard]

weights_battle_card = [weight_battle_breakthrought,weight_battle_charge,weight_battle_drain,weight_battle_guard,weight_battle_letal,weight_battle_ward,weight_battle_attack,weight_battle_cost,weight_battle_defense,weight_battle_opponent,weight_battle_healthchange,weight_battle_drawcard]

weights_hero = [weight_health, weight_deck, weight_mana, weight_rune, weight_hand]

#Simulation parameters

number_of_boards_at_start = 10
number_of_person_to_mutate = 5


@contextmanager
def timeout(time):
    """
    TimeOut definition to end the simulation in time
    """

    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.setitimer(signal.ITIMER_REAL,time,0)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    """
    Not needed here
    """
    raise TimeoutError


def simulation (board):
    """
    Simulate the best action list possible thanks to a genetical algorithm
    """
    sim_count = 0
    final_boards = []
    with timeout(0.099):

        # Creation of boards to start the evolution

        for i in range (number_of_boards_at_start):
            simulated_board = deepcopy(board)
            simulated_board.generate_a_combo()
            if (hero_letal):
                return simulated_board
            final_boards.append(simulated_board)
        # final_boards.sort(reverse = True ,key=BoardManager.evaluate)

        # Mutation et croisement

        while (True):

            #Conservation du meilleur board
            boards_to_mutate = []
            board_to_mutate = max(final_boards,key=BoardManager.evaluate)
            boards_to_mutate.append(board_to_mutate)
            mutate_from = random.randint(0,len(board_to_mutate.command)-1)
            new_board = deepcopy(board)
            prefixcommand = []

            for j in range(mutate_from):
                prefixcommand += [board_to_mutate.command[j]]

            # print("prefix "+ str(sim_count)+ ": " + str(prefixcommand),file=sys.stderr)
            new_board.play_commands(prefixcommand)
            new_board.generate_a_combo()
            if (hero_letal):
                return new_board
            # print("combo "+ str(sim_count)+ ": " + str(new_board.command) ,file=sys.stderr)
            sim_count += 1
            boards_to_mutate.append(new_board)

            for i in range (number_of_person_to_mutate - 1):
                board_to_mutate = select_board_to_mutate(final_boards,2)
                boards_to_mutate.append(board_to_mutate)
                new_board = deepcopy(board)


                mutate_from = random.randint(0,len(board_to_mutate.command)-1)
                prefixcommand = []

                for j in range(mutate_from):
                    prefixcommand += [board_to_mutate.command[j]]
                # print("prefix "+ str(sim_count)+ ": " + str(prefixcommand),file=sys.stderr)
                new_board.play_commands(prefixcommand)

                # Une chance sur deux de muter:

                if (random.randint(0,1) == 0) :
                    new_board.generate_a_combo()
                    if (hero_letal):
                        return new_board
                    # print("combo "+ str(sim_count)+ ": " + str(new_board.command) ,file=sys.stderr)


                # Une chance sur deux de croiser:

                else:
                    boards_to_cross_with = final_boards[random.randint(0,len(final_boards)-1)]

                    for i in boards_to_cross_with.command:
                        if (i in new_board.availabilities()):
                            new_board.play_commands([i])
                    if (hero_letal):
                        return new_board

                sim_count += 1
                boards_to_mutate.append(new_board)


            final_boards = boards_to_mutate
    # final_boards.sort(reverse = True ,key=BoardManager.evaluate)
    print(sim_count+1, file=sys.stderr)
    return max(final_boards,key=BoardManager.evaluate)

def select_board_to_mutate(bdmgers, n = None):
    """
    Select randomly a board to mutate
    A better board will have a better probability to be chosen
    """
    if (random.randint(0,1) == 0):
        total_evaluation = 0
        for i in bdmgers:
            eval = i.evaluate()
            if (eval<0):
                total_evaluation += -1/eval
            else:
                total_evaluation += eval + 1
        repartition_function = 0
        rand = random.random()
        chosen_index = len(bdmgers)-1

        for i in range(chosen_index):
            eval = bdmgers[i].evaluate()
            if (eval<-1):
                repartition_function += (-1/eval)/total_evaluation
            else:
                repartition_function += (eval + 2)/total_evaluation
            if (rand < repartition_function):
                chosen_index = i
                break
        return bdmgers[chosen_index]
    else:
        chosen_boards = []
        for i in range(n-1):
            chosen_element = random.randint(0,len(bdmgers)-1)
            chosen_boards.append(bdmgers[i])
        return max(chosen_boards,key=BoardManager.evaluate)



def chose_card(bdmger):
    """
    Chose the card to draw.
    Return the index of the card to pick
    To adapt according to strategy.
    """
    max_object = 5

    # In the first part of the draw phase we just pick the best cards

    if (count < 17):
        chosen_card = max(bdmger.cards_to_draw, key=Card.card_evaluation)
        index = bdmger.cards_to_draw.index(chosen_card)

        return index

    # Then we try to have a good mana repartition and no more than 5 items

    else:
        card_index_which_can_be_chosen = []
        number_of_objects = bdmger.number_of_object_in_deck
        card_to_draw_mana_cost = [bdmger.cards_to_draw[0].get_cost(),bdmger.cards_to_draw[1].get_cost(),bdmger.cards_to_draw[2].get_cost()]
        number_of_cards_min_7_mana = sum(bdmger.creatures_mana_cost_list[6:])
        number_of_cards_max_3_mana = sum(bdmger.creatures_mana_cost_list[:4])

        if(number_of_cards_max_3_mana >= 7):

            if (number_of_objects >= 5):

                if ((bdmger.cards_to_draw[0].get_card_type() == 0) or (bdmger.cards_to_draw[1].get_card_type() == 0) or (bdmger.cards_to_draw[2].get_card_type() == 0)):
                    if (bdmger.cards_to_draw[0].get_card_type() == 0):
                        card_index_which_can_be_chosen.append(0)
                    if (bdmger.cards_to_draw[1].get_card_type() == 0):
                        card_index_which_can_be_chosen.append(1)
                    if (bdmger.cards_to_draw[2].get_card_type() == 0):
                        card_index_which_can_be_chosen.append(2)
                else:

                    card_index_which_can_be_chosen.append(0)
                    card_index_which_can_be_chosen.append(1)
                    card_index_which_can_be_chosen.append(2)

            else:

                card_index_which_can_be_chosen.append(0)
                card_index_which_can_be_chosen.append(1)
                card_index_which_can_be_chosen.append(2)

            for i in range(len(card_to_draw_mana_cost)):

                if (card_to_draw_mana_cost[i] > 7):
                    if (number_of_cards_min_7_mana >= 5):
                        if i in card_index_which_can_be_chosen:
                            card_index_which_can_be_chosen.pop(card_index_which_can_be_chosen.index(i))

        else:

            if (min(card_to_draw_mana_cost) > 3):

                    if (number_of_objects >= 5):

                        if ((bdmger.cards_to_draw[0].get_card_type() != 0) or (bdmger.cards_to_draw[1].get_card_type() != 0) or (bdmger.cards_to_draw[2].get_card_type() != 0)):
                            if (bdmger.cards_to_draw[0].get_card_type() != 0):
                                card_index_which_can_be_chosen.append(0)
                            if (bdmger.cards_to_draw[1].get_card_type() != 0):
                                card_index_which_can_be_chosen.append(1)
                            if (bdmger.cards_to_draw[2].get_card_type() != 0):
                                card_index_which_can_be_chosen.append(2)
                        else:

                            card_index_which_can_be_chosen.append(0)
                            card_index_which_can_be_chosen.append(1)
                            card_index_which_can_be_chosen.append(2)

                    else:

                        card_index_which_can_be_chosen.append(0)
                        card_index_which_can_be_chosen.append(1)
                        card_index_which_can_be_chosen.append(2)

                    for i in range(len(card_to_draw_mana_cost)):

                        if (card_to_draw_mana_cost[i] > 7):
                            if (number_of_cards_min_7_mana >= 5):
                                if i in card_index_which_can_be_chosen:
                                    card_index_which_can_be_chosen.pop(card_index_which_can_be_chosen.index(i))

            else:

                for i in range (len(card_to_draw_mana_cost)):
                    if (card_to_draw_mana_cost[i] <= 3):
                        card_index_which_can_be_chosen.append(i)

        # card_index_which_can_be_chosen contient les indices, il suffit de prendre la meilleure carte

        print(card_index_which_can_be_chosen,file=sys.stderr)
        list_of_cards_which_can_be_chosen = []

        for i in card_index_which_can_be_chosen:
            list_of_cards_which_can_be_chosen.append(bdmger.cards_to_draw[i])

        chosen_card = max(list_of_cards_which_can_be_chosen, key=Card.card_evaluation)
        index = bdmger.cards_to_draw.index(chosen_card)

        return index


def battle_action(bdmger):
    """
    Makes decisions during battle turns. Old version.
    """
    actions = bdmger.availabilities()
    # print(actions, file=sys.stderr)
    action_id = random.randint(0, len(actions) - 1)
    if action_id == 0:
        action_id = random.randint(0, len(actions) - 1)
    action = actions[action_id]
    bdmger.add_command(action)
    # print("battle action: " + action, file=sys.stderr)
    return ("PASS" in action)


def old_battle_action(bdmger):
    """
    Makes decisions during battle turns. Old version.
    """
    summon, green_items, red_items, blue_items, attackers, enemys_guards = \
        bdmger.availabilities()

    my_hand = bdmger.get_my_hand()
    my_mana = bdmger.me.get_player_mana()
    my_board = bdmger.get_my_board()
    enemys_board = bdmger.get_enemys_board()
    end_of_turn = False

    # 0=PASS 1=SUMMON 2=USE_GREEN 3=USE_RED 4=USE_BLUE 5=ATTACK
    action_to_make = random.randint(0, 5)

    if (action_to_make == 1):
        if (len(summon) != 0):
            monster_to_summon = random.randint(0, len(summon) - 1)
            bdmger.summon(summon[monster_to_summon])
        else:
            while (action_to_make == 1):
                action_to_make = random.randint(1, 5)

    if (action_to_make == 2):
        if (len(attackers) != 0):
            if (len(green_items) != 0):
                green_item_to_use = random.randint(0, len(green_items) - 1)
                attackers_to_use_on = random.randint(0, len(attackers) - 1)
                bdmger.use(green_items[green_item_to_use],
                           attackers[attackers_to_use_on])
            else:
                while (action_to_make == 2):
                    action_to_make = random.randint(0, 5)
        else:
            while (action_to_make == 2):
                action_to_make = random.randint(0, 5)

    if (action_to_make == 3):
        if (len(enemys_board) != 0):
            if (len(red_items) != 0):
                red_item_to_use = random.randint(0, len(red_items) - 1)
                enemy_to_use_on = random.randint(0, len(enemys_board) - 1)
                bdmger.use(red_items[red_item_to_use],
                           enemys_board[enemy_to_use_on])
            else:
                while (action_to_make == 3):
                    action_to_make = random.randint(0, 5)
        else:
            while (action_to_make == 3):
                action_to_make = random.randint(0, 5)

    if (action_to_make == 4):
        if (len(blue_items) != 0):
            blue_item_to_use = random.randint(0, len(blue_items) - 1)
            bdmger.use(blue_items[blue_item_to_use])
        else:
            while (action_to_make == 4):
                action_to_make = random.randint(0, 5)

    if (action_to_make == 5):
        if (len(attackers) != 0):
            attacker_who_attack = random.randint(0, len(attackers) - 1)
            if (len(enemys_guards) != 0):
                enemy_to_attack = random.randint(0, len(enemys_guards) - 1)
                bdmger.attack(attackers[attacker_who_attack],
                              enemys_guards[enemy_to_attack])
            else:
                bdmger.attack(attackers[attacker_who_attack])
        else:
            while (action_to_make == 4):
                action_to_make = random.randint(0, 5)

    if (action_to_make == 0):
        end_of_turn = True

    return end_of_turn


class Card(object):
    """
    Data structure to handle card information.
    """
    def __init__(self, card_number, instance_id, location, card_type, cost,
                 attack, defense, abilities, my_health_change,
                 opponent_health_change, card_draw):
        self.card_number = card_number
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change
        self.card_draw = card_draw
        self.has_attacked = False
        self.just_summoned = False

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

    def get_my_health_change(self):
        return self.my_health_change

    def get_opponent_health_change(self):
        return self.opponent_health_change

    def get_card_draw(self):
        return self.card_draw

    # abilities getters

    def has_charge(self):
        return "C" in self.get_abilities()

    def has_ward(self):
        return "W" in self.get_abilities()

    def has_breakthrough(self):
        return "B" in self.get_abilities()

    def has_drain(self):
        return "D" in self.get_abilities()

    def has_guard(self):
        return "G" in self.get_abilities()

    def has_lethal(self):
        return "L" in self.get_abilities()

    def summon_card(self, bdmger):
        """
        Call this function when card is being summoned.
        This will update the card's location, and BoardManager's informations.
        """
        self.location = 1
        bdmger.me.player_health += self.my_health_change
        bdmger.opponent_hero.player_health += self.opponent_health_change
        self.just_summoned = True

    def use(self, bdmger, card):
        """
        Call this function when card is being used.
        This will update the card's location, and BoardManager's informations.
        """
        bdmger.me.player_health += self.my_health_change
        bdmger.opponent_hero.player_health += self.opponent_health_change

        if card is not None:
            card.attack += self.attack
            card.defense += self.defense
            if (card.defense <= 0):
                card.location = -2
            if (card.location == 1):
                for i in range(len(self.abilities)-1) :
                    if (card.abilities[i] == "-"):
                        list_abilities = list(card.abilities)
                        list_abilities[i]=self.abilities[i]
                        card.abilities = "".join(list_abilities)
            elif (card.location == -1):
                for i in self.abilities :
                    if (i in card.abilities):
                         card.abilities=card.abilities.replace(i,"-")

        self.location = -2
        # # print(command, file=sys.stderr)

    def attack_something(self, bdmger, target_card=None):
        """
        Call this function when attack is being led.
        This will update the card's information,
        and BoardManager's informations.
        """

        global hero_letal

        if target_card is None:
            bdmger.opponent_hero.player_health -= self.attack
            if (bdmger.opponent_hero.player_health <= 0):
                hero_letal = True
            self.has_attacked = True
            return False, False

        points = target_card.defense
        if not target_card.has_ward():
            target_card.defense -= self.attack
        else:
            target_card.abilities = target_card.abilities.replace("W", "-")

        if not self.has_ward():
            self.defense -= target_card.attack
        else:
            self.abilities = self.abilities.replace("W", "-")

        if (self.defense <= 0 or ("L" in target_card.abilities)):
            # self = None
            self.location = -2

        if (target_card.defense <= 0 or ("L" in self.abilities)):
            target_card.location = -2

        if (self.has_breakthrough()) and \
                (target_card.get_location() == -2):
            bdmger.opponent_hero.player_health -= (self.attack - points)
            if (bdmger.opponent_hero.player_health <= 0):
                hero_letal = True
        self.has_attacked = True
        # print(command, file=sys.stderr)

        if ("D" in self.abilities):
            bdmger.me.player_health += self.attack

    def card_evaluation (self):
        """
        Evaluation of the strenght of a card
        Return an int
        """
        global weights_draw_card, weights_battle_card

        card_result =0
        if (count < 30):
            [weight_breakthrought, weight_charge, weight_drain, weight_guard, weight_letal, weight_ward, weight_attack, weight_cost, weight_defense, weight_opponent_card, weight_healthchange, weight_drawcard] = weights_draw_card

        else:
            [weight_breakthrought, weight_charge,weight_drain,weight_guard,weight_letal,weight_ward,weight_attack,weight_cost,weight_defense,weight_opponent_card,weight_healthchange, weight_drawcard] = weights_battle_card

        # Evaluation of all cards

        breakthrought = 0
        charge = 0
        drain = 0
        guard = 0
        letal = 0
        ward = 0

        spells = self.get_abilities()
        if "B" in spells:
            breakthrought = 1 * weight_breakthrought
        if "C" in spells:
            charge = 1 * weight_charge
        if "D" in spells:
            drain = 1 * weight_drain
        if "G" in spells:
            guard = 1 * weight_guard
        if "L" in spells:
            letal = 1 * weight_letal
        if "W" in spells:
            ward = 1 * weight_ward

        attack = self.get_attack() * weight_attack
        if (attack == 0 and count < 30):
            if (letal == 0):
                attack = -2
        healthchange = abs(weight_healthchange)
        drawcard = weight_drawcard
        location = self.get_location()
        if (location == 0 and not card.just_summoned):
            drawcard = 0

        type = self.get_card_type()

        if (count<30):
            if (type == 0):
                cost = 1/((self.get_cost() * weight_cost)+1)
            else:
                cost = self.get_cost() * weight_cost + 1
        else:
            cost = self.get_cost() * weight_cost + 1
        defense = self.get_defense() * weight_defense

        if location == 0:

            if type == 0:
                # print(str(i.get_instance_id())+ ": "  + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)/(cost+1)),file=sys.stderr)
                card_result += (attack + ((attack-1) * breakthrought) + ((attack-1) * charge) + ((attack-1) * drain)  + defense + (defense * guard) + letal + ward + healthchange + drawcard)/(cost)

            else:
                # print(str(i.get_instance_id())+ ": "  + str ((attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward)/(cost+1)),file=sys.stderr)
                if (type != 3):
                    card_result += (attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward + healthchange + drawcard)/(cost)
                else:
                    card_result += (1/2)*(attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward + healthchange + drawcard)/(cost)
        elif location == 1:
            # print(str(i.get_instance_id())+ ": "  + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)),file=sys.stderr)
            card_result += ((attack) + ((attack-1) * breakthrought) + ((attack-1) * drain)  + defense/3 + (defense/3 * guard) + letal + ward + healthchange + drawcard)
        elif (location == -1):
            # print(str(i.get_instance_id())+ ": " + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)),file=sys.stderr)
            card_result -= weight_opponent_card*(weight_opponent_card*attack + (weight_opponent_card*(attack-1) * breakthrought) + (weight_opponent_card*(attack-1) * drain) + (weight_opponent_card*(attack-1) * charge)  + defense/3 + (defense * guard) + letal + ward)

        return card_result


class Hero(object):
    """
    Handles Hero information.
    """

    def __init__(self, player_health, player_mana,
                 player_deck, player_rune, player_draw):
        """
        player_health, player_mana are self explanatory
        player_deck is the number of cards left in the deck.
        player_rune is how tf would I know.
        player_draw is the number of cards drawn during this turn.
        """
        self.player_health, self.player_mana, self.player_deck,\
            self.player_rune, self.player_draw = \
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


def process_opponent_actions(actions):
    """
    TODO mettre qqch ici ?
    """
    pass


class BoardManager(object):
    """
    Data structure to handle game information.
    Don't do any default actions in __init__,
    to avoid draw and battle phases conflicts.
    """

    def __init__(self, bdmger=None, command=[]):
        self.my_hand = []
        self.my_board = []
        self.enemys_board = []
        self.my_deck = []
        self.number_of_object_in_deck = 0
        self.creatures_mana_cost_list = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.cards_to_draw = []
        self.me = None

        self.opponent_hero = None
        self.opponent_actions = []
        self.opponent_hand = 0

        self.command = []
        # self.command_legal = True

        if not (bdmger is None):
            self.my_hand = deepcopy(bdmger.my_hand)
            self.my_board = deepcopy(bdmger.my_board)
            self.enemys_board = deepcopy(bdmger.enemys_board)
            self.my_deck = deepcopy(bdmger.my_deck)
            self.number_of_object_in_deck = deepcopy(bdmger.number_of_object_in_deck)
            self.creatures_mana_cost_list = deepcopy(bdmger.creatures_mana_cost_list)
            self.cards_to_draw = deepcopy(bdmger.cards_to_draw)
            self.me = deepcopy(bdmger.me)

            self.opponent_hero = deepcopy(bdmger.opponent_hero)
            self.opponent_actions = deepcopy(bdmger.opponent_actions)
            self.opponent_hand = deepcopy(bdmger.opponent_hand)

        # if not (bdmger is None) and len(command) != 0:
        #    self.play_command()

    def add_card(self, card):
        """
        Adds a card to the correct data structure attribute.
        """
        global count

        if not (card is Card):
            pass  # print(type(card), file=sys.stderr)

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
            # print("Adding hero in bdmger while heroes already set",
                    # file=sys.stderr)
            pass

    def add_opponent_informations(self, opponent_hand,
                                  card_numbers_and_actions):
        """
        Collects and stores non hero action informations.
        Potentially useless for now.
        """
        self.opponent_actions =\
            process_opponent_actions(card_numbers_and_actions)
        self.opponent_hand = opponent_hand

    def actualize_board(self):
        """
        Cleans board from dead cards.
        """
        hand_to_board = [card for card in self.my_hand
                         if (card.get_location() == 1)]
        self.my_hand = [card for card in self.my_hand
                        if (card.get_location() not in [1, -2])]
        self.my_board = [card for card in self.my_board
                         if (card.get_location() == 1)]
        self.enemys_board = [card for card in self.enemys_board
                             if (card.get_location() == -1)]

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

    def pick_card(self):
        carte_choisie = chose_card(self)
        self.my_deck += [self.cards_to_draw[carte_choisie]]
        if (self.cards_to_draw[carte_choisie].get_card_type() == 0):
            self.creatures_mana_cost_list[self.cards_to_draw[carte_choisie].get_cost()] += 1
        else:
            self.number_of_object_in_deck += 1

        command = ["PICK {}".format(carte_choisie)]
        self.command = command

    def summon(self, card):
        """
        Applies SUMMON directive.
        """
        id = str(card.get_instance_id())
        self.me.pay_mana(card.get_cost())
        card.summon_card(self)
        self.my_board += [deepcopy(card)]
        card.location = -2
        self.actualize_board()

    def attack(self, card, target_card=None):
        """
        Applies ATTACK directive.
        """
        id = str(card.get_instance_id())
        target_id = -1
        if not(target_card is None):
            target_id = target_card.get_instance_id()
        card.attack_something(self, target_card)
        self.actualize_board()
        # print("bdmger attack: " + self.command[-1], file=sys.stderr)

    def use(self, item, target=None):
        """
        Applies USE directive.
        """
        id = str(item.get_instance_id())
        target_id = "-1"
        if not (target is None):
            target_id = str(target.get_instance_id())
        self.me.pay_mana(item.get_cost())
        item.use(self, target)
        self.actualize_board()
        # print("bdmger use: " + self.command[-1], file=sys.stderr)

    def add_command(self, command):
        """
        Parse command and applies it.
        """
        # print("bdmger add_command before: ", file=sys.stderr)
        # print(self.command, file=sys.stderr)

        tmp_list = command.split(";")
        tmp_list = tmp_list[0].split(" ")  # ["USE","13","15"]
        if "PASS" in tmp_list[0]:
            pass

        elif tmp_list[0] == "SUMMON":
            id = int(tmp_list[1])
            card = [c for c in self.my_hand
                    if c.get_instance_id() == id][0]
            self.summon(card)

        else:
            # print(command,file=sys.stderr)
            id1, id2 = tmp_list[1], tmp_list[2]
            id1, id2 = int(id1), int(id2)
            card1 = [c for c in self.my_board + self.my_hand
                     if c.get_instance_id() == id1][0]
            if id2 == -1:
                card2 = None
            else:
                card2 = [c for c in self.my_board + self.enemys_board
                         if c.get_instance_id() == id2][0]
            if tmp_list[0] == "ATTACK":
                self.attack(card1, card2)
            if tmp_list[0] == "USE":
                self.use(card1, card2)
        self.command += [command]
        # print("bdmger add_command after: ", file=sys.stderr)
        # print(self.command, file=sys.stderr)

    def play_commands(self, commands):
        """
        Plays entire command.
        May and may not be useless.
        """
        for i in commands:
            self.add_command(i)
        # print("bdmger play_commands: ", file=sys.stderr)
        # print(self.command, file=sys.stderr)

    def availabilities(self):
        """
        Returns a list of command strings giving legal actions to take.
        Ex: ["SUMMON 1;","ATTACK 3 -1;"]
        """
        legal_actions = ["PASS ; "]

        # SUMMON ACTIONS
        summonable = [card.get_instance_id() for card in self.my_hand
                      if
                      ((card.get_cost() <= self.me.get_player_mana())
                       and
                       (card.get_card_type() == 0))
                      ]

        legal_actions += ["SUMMON {}; ".format(str(id))
                          for id in summonable]

        # People I can attack
        to_attack = [card for card in self.enemys_board
                     if
                     ("G" in card.get_abilities())
                     ]
        to_attack = [card.get_instance_id() for card in to_attack]

        if len(to_attack) == 0:
            to_attack = self.enemys_board

            to_attack = [card.get_instance_id() for card in to_attack] + [-1]

        # Who I can attack them with
        # Cards that were just summoned ?
        # Cards that already attacked ?
        ids_cannot_attack = []
        for card in self.my_board:
            id = card.get_instance_id()

            just_summoned = card.just_summoned

            has_charge = card.has_charge()
            has_attacked = card.has_attacked
            # if just summoned, no charge / already attacked
            if has_attacked:
                pass  # don't attack
            elif just_summoned and not has_charge:
                pass  # don't attack
            else:  # when hasn't attacked AND was not just summon without C
                for id2 in to_attack:
                    if (not (card.get_attack() == 0) or ("L" in card.get_abilities())):
                        legal_actions.append("ATTACK {} {}; "
                                            .format(str(id), str(id2)))

        for card in self.my_board:
            id1 = card.get_instance_id()
            if id1 in ids_cannot_attack:
                pass
        # items ?
        green_items = [card.get_instance_id() for card in self.my_hand
                       if
                       ((card.get_cost() <= self.me.get_player_mana())
                        and
                        (card.get_card_type() == 1))
                       ]

        red_items = [card.get_instance_id() for card in self.my_hand
                     if
                     (card.get_cost() <= self.me.get_player_mana()
                      and
                      card.get_card_type() == 2)
                     ]

        blue_items = [card.get_instance_id() for card in self.my_hand
                      if
                      (card.get_cost() <= self.me.get_player_mana()
                       and
                       card.get_card_type() == 3)
                      ]

        for id1 in green_items:
            for id2 in [card.get_instance_id() for card in self.my_board]:
                legal_actions.append("USE {} {}; "
                                     .format(str(id1), str(id2)))

        for id1 in red_items:
            for id2 in [card.get_instance_id() for card in self.enemys_board]:
                legal_actions.append("USE {} {}; "
                                     .format(str(id1), str(id2)))

        for id1 in blue_items:
            for id2 in [card.get_instance_id() for card in self.enemys_board]\
                    + [-1]:
                legal_actions.append("USE {} {}; "
                                     .format(str(id1), str(id2)))

        # print(legal_actions, file=sys.stderr)
        return legal_actions

    def generate_a_combo(self):
        """
        Generates a legal combo and stores it as a string list
        in command attribute
        """
        # print("bdmger generate_a_combo before: ", file=sys.stderr)
        # print(self.command, file=sys.stderr)

        while not battle_action(self):
            pass

        # print("bdmger generate_a_combo after: ", file=sys.stderr)
        # print(self.command, file=sys.stderr)

    def evaluate(self):
        """
        Evaluate the state of the board
        Return an int
        """
        global count
        result = 0

        # Evaluation of the state of Heroes
        [health_weight, deck_weight, mana_weight, rune_weight, hand_weight] = weights_hero

        # print("HEALTH: " + str ((self.me.get_player_health() - self.opponent_hero.get_player_health())*health_weight),file=sys.stderr)
        result += (self.me.get_player_health() - self.opponent_hero.get_player_health())*health_weight
        # print("DECK: " + str ((self.me.get_player_deck() - self.opponent_hero.get_player_deck())*deck_weight),file=sys.stderr)
        result += (self.me.get_player_deck() - self.opponent_hero.get_player_deck())*deck_weight
        # print("MANA: " + str (-(self.me.get_player_mana())*mana_weight),file=sys.stderr)
        result += -(self.me.get_player_mana())*mana_weight
        # print("RUNE: " + str ((self.me.get_player_rune() - self.opponent_hero.get_player_rune())*rune_weight),file=sys.stderr)
        result += (self.me.get_player_rune() - self.opponent_hero.get_player_rune())*rune_weight
        # print("HAND" + str ((len(self.get_my_hand()) - self.opponent_hand)*hand_weight),file=sys.stderr)
        result += (len(self.get_my_hand()) - self.opponent_hand)*hand_weight


        # Evaluation of all cards

        for i in (self.my_board + self.enemys_board + self.my_hand):

            result += i.card_evaluation()

        return result



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
        # print("gMger manages before: ", file=sys.stderr)
        # print(self.bdmger.command, file=sys.stderr)
        try:
            if count < 30:
                self.draw_phase()
            else:
                self.battle_phase()
        except Exception as e:
            print(e, file=sys.stderr)

        # print("gMger manages after: ", file=sys.stderr)
        # print(self.bdmger.command, file=sys.stderr)

    def draw_phase(self):
        """
        Choses cards to draw.
        """
        self.bdmger.pick_card()

    def battle_phase(self):
        """
        Choses battle actions to take and returns them in a command string.
        TODO: remplacer par keski faut.
        """
        simulation_result = simulation(self.bdmger)
        print("Result of Simulation:" + str(simulation_result.command), file=sys.stderr)

        self.bdmger.play_commands(simulation_result.command)


# the standard input according to the problem statement.
# game loop

while True:

    bdmger = BoardManager()
    card_numbers_and_actions = []

    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = \
            [int(j) for j in input().split()]
        hero = Hero(player_health, player_mana, player_deck,
                    player_rune, player_draw)
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
                    attack, defense, abilities, my_health_change,
                    opponent_health_change, card_draw)
        bdmger.add_card(card)

    gMger = GameManager(bdmger)
    gMger.manages()

    command = "".join(gMger.bdmger.command)

    count += 1 # count gives the turn's number
    if command == "":
        # print("PASS")
        pass
    else:
        # print(command, file=sys.stderr)

        #Giving the command to the game
        print(command)
