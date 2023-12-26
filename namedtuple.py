from random import choice


class Deck:
    def __init__(self):
        # builds the whole deck (2♥️, 3♦️, ..., J♣️, K♠️)
        self._cards = [
            self.Card(rank, suit)
            for suit in self.Card.suits["symbols"]
            for rank in self.Card.ranks
        ]

    def __len__(self):
        return len(self._cards)

    # makes the class iterable
    def __getitem__(self, position):
        return self._cards[position]

    # logic to check if something exists in class
    def __contains__(self, item):
        if not isinstance(item, self.Card):
            raise TypeError("this is not a Card type")

    class Card:
        # creates 2 lists: [2..10] + ['J','Q','K','A'] representing the range
        # for the cards
        ranks = [str(n) for n in range(2, 11)] + list("JQKA")
        suits = {
            "symbols": "♣ ♦ ♥ ♠".split(),  # another list within these strings
            "values": {
                "♠": 3,
                "♥": 2,
                "♦": 1,
                "♣": 0,
            },  # the importance of every symbol
        }
        rank = choice(ranks)
        suit = choice(suits["symbols"])

        def __init__(self, rank, suit) -> None:
            if rank not in self.ranks:
                raise ValueError(
                    "rank should be one of '" + self.ranks.__str__()
                )
            if suit not in (self.suits["symbols"]):
                raise ValueError(
                    "suit should be one of '" + self.suits.__str__()
                )
            self.rank = rank
            self.suit = suit

        def __str__(self) -> str:
            return self.suit + self.rank

        def __int__(self):
            rank_value = self.ranks.index(
                self.rank
            )  # the index of the object card rank in the self.ranks
            # calculates the importance of a card like 2♣️=0, A=51
            return (
                rank_value * len(self.suits["values"]) +
                self.suits["values"][self.suit]
            )

        # less or equal comparison of cards
        def __le__(self, other):
            return self.__int__() <= other.__int__()

        # less than comparison of cards
        def __lt__(self, other):
            return self.__int__() < other.__int__()

        # greater or equal comparison of cards
        def __ge__(self, other):
            return self.__int__() >= other.__int__()

        # greater than comparison of cards
        def __gt__(self, other):
            return self.__int__() > other.__int__()


if __name__ == "__main__":
    deck = Deck()
    print(len(deck))
    print(deck._cards)
    print(deck[9])
    # random card (run the code twice to find out)
    card1 = choice(deck)
    card2 = choice(deck)
    print(card1, card2)
    # slicing the cards, multiple cards
    cards5 = deck[:5]  # the first 5 cards
    print(cards5)
    cards_5 = deck[5:]  # the whole deck - last 5 cards
    print(cards_5)
    cards2_5 = deck[2:5]  # from index 2 to 5
    print(cards2_5)
    print(Deck.Card("4", "♠") in cards2_5)  # hit __contains__ magic method
    print(deck[0], " = ", int(deck[0]))  # hit __int__ magic method
    print(deck[51], " = ", int(deck[51]))
    for card in sorted(
        deck
    ):  # we can sort once we implemented the comparison magic methods
        print(card, int(card))
    for card in reversed(deck):
        print(card, int(card))
    # 'x' in deck  # this will throw an exception since we added a validation
    # to special method __contains__()
