import random
import time

class Player:
    def __init__(self, is_ai, id):
        self.is_ai = is_ai
        self.cards = list()
        self.score = 0
        self.points = 0
        self.id = id

    def draw_cards(self, deck, index, n_cards):
        self.cards.extend(deck[index : index + n_cards])
        index += n_cards
        return index

    def sort_cards(self):
        cards = ['2', '3', '4', '5', '6' ,'7', '8', '9', '10', 'J', 'D', 'K', '1']
        suits = ['h', 'd', 'c', 's']
        self.cards = sorted(self.cards, key=lambda c : suits.index(c[0]) * 13 + (cards.index(c[1:])))

    def play_card(self, cards_on_table):
        '''
            checks:
            1. starting card
            2. ace or king on table
            3. hearts broken
            4. got Dame of hearts
            5. got hearts
            6. got Dames
        '''
        playable_cards = [i for i in range(len(self.cards))]
        # check 1
        if len(cards_on_table) > 0:
            starting_card = cards_on_table[0]
            if any([starting_card[0] in c for c in self.cards]):
                playable_cards = [i for i in playable_cards if self.cards[i][0] == starting_card[0]]
                # check 2
                if any([c == starting_card[0] + '1' or c == starting_card[0] + 'K' for c in cards_on_table]):
                    if any([c == starting_card[0] + 'D' for c in self.cards]):
                        playable_cards = [i for i in playable_cards if self.cards[i] == starting_card[0] + 'D']
            else:
                # check 4 / 5
                if any(['h' in c for c in self.cards]):
                    if any([c == 'hD' for c in self.cards]):
                        playable_cards = [self.cards.index('hD')]
                    else:
                        playable_cards = [i for i in playable_cards if 'h' in self.cards[i]]
                # check 6
                elif any(['D' in c for c in self.cards]):
                    playable_cards = [i for i in playable_cards if 'D' in self.cards[i]]

        if not self.is_ai:
            try:
                playing_card = int(input("enter card to play: "))
            except:
                playing_card = -1
                pass
            while playing_card not in playable_cards:
                try:
                    playing_card = int(input("enter card to play: "))
                except:
                    continue
        # ai implementation
        else:
            time.sleep(random.random() * 3 + 1)
            playing_card_index = int(random.random() * len(playable_cards))
            playing_card = playable_cards[playing_card_index]
            cards = ['2', '3', '4', '5', '6' ,'7', '8', '9', '10', 'J', 'D', 'K', '1']
            # print("playable_cards:")
            # print([self.cards[i] for i in playable_cards])
            # print("self cards:")
            # self.print_cards()
            # print("card scores:")
            if len(cards_on_table) > 0:
                points_on_table = False
                starting_card = cards_on_table[0]
                starting_card_score = cards.index(starting_card[1:])
                highest_card = starting_card
                highest_card_score = starting_card_score
                for card in cards_on_table:
                    card_score = cards.index(card[1:])
                    if card[0] == 'h' or card[1:] == 'D':
                        points_on_table = True
                    if card_score > highest_card_score and card[0] == starting_card[0]:
                        highest_card_score = cards.index(card[1:])
                        highest_card = card
                # print("starting card %s: %d" % (starting_card, starting_card_score))
                # print("highest card %s: %d" % (highest_card, highest_card_score))
                card_chosen = False
                for i in playable_cards:
                    card_score = cards.index(self.cards[i][1:])
                    # print("self card %s: %d" % (self.cards[i], cards.index(self.cards[i][1:])))
                    if card_score < highest_card_score and points_on_table:
                        card_chosen = True
                        playing_card = i
                if not card_chosen:
                    for i in playable_cards:
                        card_score = cards.index(self.cards[i][1:])
                        if card_score < cards.index('D') and len(cards_on_table) < 3:
                            playing_card = i
                            card_chosen = True
                if not card_chosen:
                    for i in playable_cards:
                        card_score = cards.index(self.cards[i][1:])
                        if len(cards_on_table) == 3 and card_score != cards.index('D'):
                            playing_card = i
                            card_chosen = True
            else:
                take_rand_card = []
                for i in playable_cards:
                    card_score = cards.index(self.cards[i][1:])
                    if card_score < cards.index('D'):
                        take_rand_card.append(i)

                if len(take_rand_card) > 0:
                    playing_card = take_rand_card[int(random.random() * len(take_rand_card))]

            # print("playing card index %d: %s" % (playing_card, self.cards[playing_card]))
        return self.cards.pop(playing_card)

    def start_new_round(self):
        self.cards = list()
        self.points = 0

    def calculate_points(self, cards_on_table):
        for c in cards_on_table:
            if c == 'hD':
                self.points += 14
            elif 'h' in c:
                self.points += 1
            elif 'D' in c:
                self.points += 13

    def print_cards(self):
        print(["{}: {}".format(i, self.cards[i]) for i in range(len(self.cards))])

    def __str__(self):
        return "___ player {} (points: {}, score: {}) ___".format(self.id, self.points, self.score)

def main():
    n_players = 4
    players = [Player(1, i) for i in range(n_players)]
    players[0].is_ai = 0
    cards = ['2', '3', '4', '5', '6' ,'7', '8', '9', '10', 'J', 'D', 'K', '1']
    suits = ['h', 'd', 'c', 's']
    deck = list()
    deck_index = 0
    n_rounds = 8
    dealer = 0
    dealing = [4, 5, 4]
    n_cards = sum(dealing)

    for s in suits:
        for c in cards:
            deck.append(s + c)

    cards_on_table = list()

    for r in range(n_rounds):
        deck_index = 0
        deck = shuffle(deck)
        print("\nplayer {} is dealing...".format(dealer))
        for d in dealing:
            for p in range(n_players):
                starting_player = players[(dealer + p + 1) % n_players]
                deck_index = starting_player.draw_cards(deck, deck_index, d)
        for p in players:
            p.sort_cards()

        starting_player_index = (dealer + 1) % n_players
        starting_player = players[starting_player_index]
        winning_player_score = 0
        winning_player = starting_player
        winning_player_index = starting_player_index
        print("\n____ round {} ____".format(r))
        while len(starting_player.cards) > 0:
            cards_on_table = list()
            winning_player_score = 0
            for p in range(n_players):
                print(starting_player)
                if starting_player.is_ai == 0:
                    starting_player.print_cards()
                card_played = starting_player.play_card(cards_on_table)
                cards_on_table.append(card_played)
                print("cards on table:")
                print(cards_on_table)
                if len(cards_on_table) > 0 and card_played[0] == cards_on_table[0][0]:
                    playing_card_score = cards.index(card_played[1:])
                    # print("playing_card_score: %d" % playing_card_score)
                    # print("winning_player_score: %d" % winning_player_score)
                    if playing_card_score > winning_player_score:
                        winning_player = starting_player
                        winning_player_score = playing_card_score
                        winning_player_index = starting_player_index
                elif len(cards_on_table) == 0:
                    winning_player_score = cards.index(cards_on_table[0][1:])

                starting_player_index = (starting_player_index + 1) % n_players
                starting_player = players[starting_player_index]

            winning_player.calculate_points(cards_on_table)
            print("{} wins the trick".format(winning_player))
            starting_player = winning_player
            starting_player_index = winning_player_index

        for p in players:
            if p.points == 65:
                winning_player = p
        if winning_player.points == 65:
            for p in players:
                if p.id != winning_player.id:
                    p.score += 65
                p.start_new_round()
        else:
            for p in players:
                p.score += p.points
                p.start_new_round()

        print("\n______ final score ______")
        for p in players:
            print(p)
        dealer = (dealer + 1) % n_players


def shuffle(deck):
    for i in reversed(range(1, len(deck))):
        j = int(random.random() * i)
        deck[i], deck[j] = deck[j], deck[i]
    return deck

if __name__ == '__main__':
    main()
