import random
from card import Card, NumberCard, ActionCard, WildCard


class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    def extend(self, cards):
        self.cards.extend(cards)

    def showAll(self):
        for card in self.cards:
            print(card)

    def drawCards(self, num):
        cardsDealt = self.cards[:num]
        self.cards = self.cards[num:]
        return cardsDealt

    def shuffleDeck(self):
        for c in range(len(self.cards)):
            r = random.randint(c, len(self.cards) - 1)

            tempCard = self.cards[r]
            self.cards[r] = self.cards[c]
            self.cards[c] = tempCard

    @staticmethod
    def createDeck():
        cards = []

        for color in Card.Colors:
            cards.append(NumberCard(color, 0))
            for value in Card.Values[1:]:
                for x in range(2):
                    cards.append(NumberCard(color, value))
            for action in Card.ActionTypes:
                for x in range(2):
                    cards.append(ActionCard(color, action))

        for wild in Card.WildTypes:
            for x in range(4):
                cards.append(WildCard(None, wild))

        return cards
