import random
import os
import subprocess

# subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


#Cards
class Card():
    def __init__(self, color):
        self.color = color

    
    COLORS = [
        "Red",
        "Green",
        "Blue",
        "Yellow"
    ]

    VALUES = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    ]

    ACTION_TYPES = [
        "Block", "Reverse", "+2"
    ]

    WILD_TYPES = [
        "Wild Card", "+4"
    ]


    def __str__(self):
        return ""

class NumberCard(Card):
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} | {self.value}"

class ActionCard(Card):
    def __init__(self, color, action_type):
        self.color = color
        self.action_type = action_type

    def __str__(self):
        return f"{self.color} | {self.action_type}"

class WildCard(Card):
    def __init__(self, color, wild_type):
        self.color = None
        self.wild_type = wild_type

    def __str__(self):
        return f"{self.color} | {self.wild_type}"


#Deck
class Deck():
    def __init__(self, cards=None):
        if cards == None:
            cards = []
        self.cards = cards

    def showAll(self):
        for card in self.cards:
            print(card)
        #print(len(self.cards))

    def drawCard(self, num):
        cards_dealt = self.cards[:num]
        self.cards = self.cards[num:]
        return cards_dealt

    def shuffleDeck(self):
        for c in range(len(self.cards)):
            r = random.randint(c, len(self.cards) - 1)

            temp_card = self.cards[r]
            self.cards[r] = self.cards[c]
            self.cards[c] = temp_card
            



    @staticmethod
    def createDeck():
        cards = []

        for color in Card.COLORS:
            cards.append(NumberCard(color, 0)) 
            for value in Card.VALUES[1:]:
                for x in range(2):
                    cards.append(NumberCard(color, value)) 
            for action in Card.ACTION_TYPES:
                for x in range(2):
                    cards.append(ActionCard(color, action)) 

        for wild in Card.WILD_TYPES:
            for x in range(4):
                cards.append(WildCard(None, wild)) 

        return cards





#Player
class Player():
    def __init__(self, hand):
        self.hand = hand

    def showHand(self):
        for card in self.hand:
            print(card)

class ComputarPlayer(Player):
    def __init__(self, hand):
        self.hand = hand

class HumanPlayer(Player):
    def __init__(self, hand):
        self.hand = hand



class Game:
    def __init__(self, playerAmount, deck):
        self.deck = deck

    

    

subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


cards = Deck.createDeck()
deck = Deck(cards)
deck.shuffleDeck()
deck.showAll()