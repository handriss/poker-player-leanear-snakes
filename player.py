import json

game_state = {
    "tournament_id":"550d1d68cd7bd10003000003",     # Id of the current tournament

    "game_id":"550da1cb2d909006e90004b1",           # Id of the current sit'n'go game. You can use this to link a
                                                    # sequence of game states together for logging purposes, or to
                                                    # make sure that the same strategy is played for an entire game

    "round":0,                                      # Index of the current round within a sit'n'go

    "bet_index":0,                                  # Index of the betting opportunity within a round

    "small_blind": 10,                              # The small blind in the current round. The big blind is twice the
                                                    #     small blind

    "current_buy_in": 80,                          # The amount of the largest current bet from any one player

    "pot": 400,                                     # The size of the pot (sum of the player bets)

    "minimum_raise": 240,                           # Minimum raise amount. To raise you have to return at least:
                                                    #     current_buy_in - players[in_action][bet] + minimum_raise

    "dealer": 1,                                    # The index of the player on the dealer button in this round
                                                    #     The first player is (dealer+1)%(players.length)

    "orbits": 7,                                    # Number of orbits completed. (The number of times the dealer
                                                    #     button returned to the same player.)

    "in_action": 1,                                 # The index of your player, in the players array

    "players": [                                    # An array of the players. The order stays the same during the
        {                                           #     entire tournament

            "id": 0,                                # Id of the player (same as the index)

            "name": "Albert",                       # Name specified in the tournament config

            "status": "active",                     # Status of the player:
                                                    #   - active: the player can make bets, and win the current pot
                                                    #   - folded: the player folded, and gave up interest in
                                                    #       the current pot. They can return in the next round.
                                                    #   - out: the player lost all chips, and is out of this sit'n'go

            "version": "Default random player",     # Version identifier returned by the player

            "stack": 1010,                          # Amount of chips still available for the player. (Not including
                                                    #     the chips the player bet in this round.)

            "bet": 0                              # The amount of chips the player put into the pot
        },
        {
            "id": 1,                                # Your own player looks similar, with one extension.
            "name": "Fishes",
            "status": "active",
            "version": "Default random player",
            "stack": 1590,
            "bet": 80,
            "hole_cards": [                         # The cards of the player. This is only visible for your own player
                                                    #     except after showdown, when cards revealed are also included.
                {
                    "rank": "A",                    # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
                    "suit": "spades"                # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
                },
                {
                    "rank": "K",
                    "suit": "hearts"
                }
            ]
        },
        {
            "id": 2,
            "name": "Chuck",
            "status": "active",
            "version": "Default random player",
            "stack": 0,
            "bet": 0
        }
    ],
    "community_cards": [                            # Finally the array of community cards.
        {
            "rank": "2",
            "suit": "spades"
        },
        {
            "rank": "3",
            "suit": "hearts"
        },
        {
            "rank": "3",
            "suit": "clubs"
        }
    ]
}


class Player:

    VERSION = "Leanear Snakes"
    card_order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


    def get_own_cards(self, game_state):
        for player in game_state['players']:
            try:
                return player['hole_cards']
            except KeyError:
                pass


    def get_community_cards(self, game_state):
        try:
            return game_state['community_cards']
        except KeyError:
            return None


    def betRequest(self, game_state):
        self.own_cards = self.get_own_cards(game_state)
        self.community_cards = self.get_community_cards(game_state)

        # preflop
        if(self.count_active_players(game_state) > 2):
            if self.community_cards == []:
                if self.check_preflop():
                    return 5000
            return 0
        else:

            self.own_cards = self.get_own_cards(game_state)
            self.community_cards = self.get_community_cards(game_state)

            # preflop
            if self.community_cards == []:
                if self.check_preflop():
                    return 34000

            # post flop
            else:

                if self.check_high_card():
                    return 30000
            return 0

    def showdown(self, game_state):
        pass


    def check_preflop(self):
        if(self.count_active_players(game_state) > 2):
            high_card = ['A', 'K']
            if self.own_cards[0]['rank'] == self.own_cards[1]['rank']:
                return True
            if self.own_cards[0]['rank'] in high_card and self.own_cards[1]['rank'] in high_card:
                return True
            return False
        else:
            high_card = ['A', 'K', 'Q', 'J', '10']
            if self.own_cards[0]['rank'] == self.own_cards[1]['rank']:
                return True
            if self.own_cards[0]['rank'] in high_card or self.own_cards[1]['rank'] in high_card:
                return True
            return False


    def count_active_players(self, game_state):
        counter = 0
        for player in game_state['players']:
            if player['status'] == "active":
                counter += 1
        return counter


    def check_high_card(self):
            if self.card_order.index(self.own_cards[0]['rank']) > self.card_order.index(self.own_cards[1]['rank']):
                highest_in_hand = self.own_cards[0]
                print(highest_in_hand)
            else:
                highest_in_hand = self.own_cards[1]
            highest_on_table = self.community_cards[0]
            for card in self.community_cards:
                if self.card_order.index(card['rank']) > self.card_order.index(highest_on_table['rank']):
                    highest_on_table = card
            print(highest_on_table)
            if self.card_order.index(highest_in_hand['rank']) > self.card_order.index(highest_on_table['rank']):
                return True
            return False

    def check_ranks(self):
        """Checks ranks. It can return the following strings:
        Royal Flush
        Straight Flush
        Four of a Kind
        Full House
        Flush
        Straight
        Three of a Kind
        Two Pairs
        One Pair
        High card
        Nothing
        """

        hand_rank = []
        for card in self.own_cards:
            hand_rank.append(card['rank'])

        comminity_rank = []
        for card in self.community_cards:
            comminity_rank.append(card['rank'])

        all_rank = []
        for card in self.community_cards + self.own_cards:
            all_rank.append(card['rank'])

        rank_length = len(all_rank) - len(set(all_rank))



        # Royal Flush

        # Straight Flush

        # Four of a Kind
        if rank_length == 3:
            for card in hand_rank:
                if all_rank.count(card) > 3:
                    return "Four of a Kind"

        # Full House
        if rank_length == 3:
            for card in hand_rank:
                if all_rank.count(card) > 1:
                    return "Full House"

        # Flush

        # Straight

        # Three of a Kind
        if rank_length == 2:
            for card in hand_rank:
                if all_rank.count(card) > 2:
                    return "Set"

        # Two Pairs
        if rank_length == 2:
            for card in hand_rank:
                if all_rank.count(card) > 1:
                    return "Two Pairs"

        # One Pair
        if rank_length == 1:
            for card in hand_rank:
                if all_rank.count(card) > 1:
                    return "One Pair"

        # High card
        for card in hand_rank:
            for comm_card in comminity_rank:
                if self.card_order.index(card) < self.card_order.index(comm_card):
                    return "Nothing"
        return "High Card"



player = Player()
print(player.betRequest(game_state))
