def evaluate(self):
        """
        Evaluate the state of the board
        """
        
        global count
        result = 0
        
        #Battle Phase

        if (count >= 30): 
        
        #Hero 
        
            health_weight = 1
            deck_weight = 1/6
            mana_weight = 1
            rune_weight = 1
            hand_weight = 1

            weight = [health_weight, deck_weight, mana_weight, rune_weight, hand_weight]
            
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

            #Cards
            
            for i in (self.my_board + self.enemys_board + self.my_hand) :

                breakthrought = 0
                charge = 0
                drain = 0
                guard = 0
                letal = 0
                ward = 0

                spells = i.get_abilities()
                if "B" in spells :
                    breakthrought = 1
                if "C" in spells :
                    charge = 1
                if "D" in spells :
                    drain = 1
                if "G" in spells :
                    guard = 1
                if "L" in spells :
                    letal = 1 * 6
                if "W" in spells :
                    ward = 1 * 6

                attack = i.get_attack()
                cost = i.get_cost()
                defense = i.get_defense()
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
