def evaluate(self):
        """
        Evaluate the state of the board
        """
        global count
        result = 0

    # Evaluation during Draw phase

        if (count<30):

            #Weight of Card's attribute

            weight_breakthrought = 1
            weight_charge = 1
            weight_drain = 1
            weight_guard = 1
            weight_letal = 6
            weight_ward = 6
            weight_attack = 1
            weight_cost = 1
            weight_defense = 1

            weight_card = [weight_breakthrought,weight_charge,weight_drain,weight_guard,weight_ward,weight_attack,weight_cost,weight_defense]

            #Evaluation of the card picked

            chosen_card = self.my_deck[-1]

            breakthrought = 0
            charge = 0
            drain = 0
            guard = 0
            letal = 0
            ward = 0

            spells = chosen_card.get_abilities()
            if "B" in spells :
                breakthrought = 1 * weight_breakthrought
            if "C" in spells :
                charge = 1 * weight_charge
            if "D" in spells :
                drain = 1 * weight_drain
            if "G" in spells :
                guard = 1 * weight_guard
            if "L" in spells :
                letal = 1 * weight_letal
            if "W" in spells :
                ward = 1 * weight_ward

            attack = chosen_card.get_attack() * weight_attack
            cost = chosen_card.get_cost() * weight_cost
            defense = chosen_card.get_defense() * weight_defense

            location = chosen_card.get_location()
            type = chosen_card.get_card_type()

            if type == 0:
                print(str(chosen_card.get_instance_id())+ ": "  + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)/(cost+1)),file=sys.stderr)
                result += (attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)/(cost+1)

            elif (type == 3 or type == 2):
                result += abs((attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward)/(cost+1))
            else:
                print(str(chosen_card.get_instance_id())+ ": "  + str ((attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward)/(cost+1)),file=sys.stderr)
                result += (attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward)/(cost+1)


    #Evaluation during Battle Phase

        else:

            #Evaluation of the state of Heroes

            health_weight = 1
            deck_weight = 1/6
            mana_weight = 1
            rune_weight = 1
            hand_weight = 1

            weight_hero = [health_weight, deck_weight, mana_weight, rune_weight, hand_weight]

            print("HEALTH: " + str ((self.me.get_player_health() - self.opponent_hero.get_player_health())*health_weight),file=sys.stderr)
            result += (self.me.get_player_health() - self.opponent_hero.get_player_health())*health_weight
            print("DECK: " + str ((self.me.get_player_deck() - self.opponent_hero.get_player_deck())*deck_weight),file=sys.stderr)
            result += (self.me.get_player_deck() - self.opponent_hero.get_player_deck())*deck_weight
            print("MANA: " + str (-(self.me.get_player_mana())*mana_weight),file=sys.stderr)
            result += -(self.me.get_player_mana())*mana_weight
            print("RUNE: " + str ((self.me.get_player_rune() - self.opponent_hero.get_player_rune())*rune_weight),file=sys.stderr)
            result += (self.me.get_player_rune() - self.opponent_hero.get_player_rune())*rune_weight
            print("HAND" + str ((len(self.get_my_hand()) - self.opponent_hand)*hand_weight),file=sys.stderr)
            result += (len(self.get_my_hand()) - self.opponent_hand)*hand_weight

            #Weight of Card's attribute

            weight_breakthrought = 1
            weight_charge = 1
            weight_drain = 1
            weight_guard = 1
            weight_letal = 6
            weight_ward = 6
            weight_attack = 1
            weight_cost = 1
            weight_defense = 1

            weight_card = [weight_breakthrought,weight_charge,weight_drain,weight_guard,weight_ward,weight_attack,weight_cost,weight_defense]

            #Evaluation of all cards

            for i in (self.my_board + self.enemys_board + self.my_hand) :

                breakthrought = 0
                charge = 0
                drain = 0
                guard = 0
                letal = 0
                ward = 0

                spells = i.get_abilities()
                if "B" in spells :
                    breakthrought = 1 * weight_breakthrought
                if "C" in spells :
                    charge = 1 * weight_charge
                if "D" in spells :
                    drain = 1 * weight_drain
                if "G" in spells :
                    guard = 1 * weight_guard
                if "L" in spells :
                    letal = 1 * weight_letal
                if "W" in spells :
                    ward = 1 * weight_ward

                attack = i.get_attack() * weight_attack
                cost = i.get_cost() * weight_cost
                defense = i.get_defense() * weight_defense

                location = i.get_location()
                type = i.get_card_type()

                if location == 0:

                    if type == 0:
                        print(str(i.get_instance_id())+ ": "  + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)/(cost+1)),file=sys.stderr)
                        result += (attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)/(cost+1)

                    else:
                        print(str(i.get_instance_id())+ ": "  + str ((attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward)/(cost+1)),file=sys.stderr)
                        result += (attack + (6 * breakthrought) + (6 * charge) + (6 * drain)  + defense + (6 * guard) + letal + ward)/(cost+1)

                elif location == 1:
                        print(str(i.get_instance_id())+ ": "  + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)),file=sys.stderr)
                        result += (attack + (attack * breakthrought) + (attack * drain)  + defense + (defense * guard) + letal + ward)
                else:
                    print(str(i.get_instance_id())+ ": " + str ((attack + (attack * breakthrought) + (attack * charge) + (attack * drain)  + defense + (defense * guard) + letal + ward)),file=sys.stderr)
                    result -= (attack + (attack * breakthrought) + (attack * drain)  + defense + (defense * guard) + letal + ward)

        return result
