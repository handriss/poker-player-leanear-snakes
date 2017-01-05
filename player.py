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
                    "rank": "7",                    # Rank of the card. Possible values are numbers 2-10 and J,Q,K,A
                    "suit": "hearts"                # Suit of the card. Possible values are: clubs,spades,hearts,diamonds
                },
                {
                    "rank": "10",
                    "suit": "spades"
                }
            ]
        },
        {
            "id": 2,
            "name": "Chuck",
            "status": "out",
            "version": "Default random player",
            "stack": 0,
            "bet": 0
        }
    ],
    # "community_cards": [                            # Finally the array of community cards.
    #     {
    #         "rank": "10",
    #         "suit": "spades"
    #     },
    #     {
    #         "rank": "10",
    #         "suit": "hearts"
    #     },
    #     {
    #         "rank": "10",
    #         "suit": "clubs"
    #     }
    # ]
}


class Player:

    VERSION = "Leanear Snakes"


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

        if self.community_cards is None:
            if self.check_preflop():
                return 10000

        return 0



    def showdown(self, game_state):
        pass


    def check_preflop(self):
        high_card = ['A', 'K', 'Q', 'J', '10']
        if self.own_cards[0]['rank'] == self.own_cards[1]['rank']:
            return True
        if self.own_cards[0]['rank'] in high_card or self.own_cards[0]['rank'] in high_card:
            return True
        return False




    def check_high_card(self):
        pass
        # get highest cards from hand

        # get highest card from community cards

        # is hand highest > community highest

    def check_one_pair(self):
        pass

    def check_two_pairs(self):
        pass

    def check_set(self):
        pass


player = Player()
print(player.betRequest(game_state))


