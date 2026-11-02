import random
import os
import subprocess
import time

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

    def playerTurn(self):
        pass

class ComputerPlayer(Player):
    def __init__(self, hand):
        self.hand = hand

    def playerTurn(self):
        pass

class HumanPlayer(Player):
    def __init__(self, hand):
        self.hand = hand

    def playerTurn(self, discardPile):
        print("Your Turn")
        print("---------")  
        print("Your hand: ")

        
        

        while True:
            for i, card in enumerate(self.hand, 1):
                print(f"{i}. {card}")

            try:
                option = int(input(f"Chose a card, 1-{max(self.hand)}: "))
                for i, card in enumerate(self.hand, 1):
                    if card[option] == card[i]:


            except:
                print("Invalid option, try again.")

        validCards = []

        for i, card in enumerate(self.hand, 1):
            print(f"{i}. {card}")
            if card.__class__.__name__ == "WildCard":
                validCards.append(i)

            elif card.__class__.__name__ == "ActionCard":
                if card.color == discardPile[-1].color:
                    validCards.append(i)
                try:
                    if card.action_type == discardPile[-1].action_type:
                        validCards.append(i)
                except:
                    continue

            elif card.__class__.__name__ == "NumberCard":
                try:
                    if card.color == discardPile[-1].color:
                        validCards.append(i)
                    elif card.value == discardPile[-1].value:
                        validCards.append(i)
                except:
                    continue
            




        while True:
            try:
                chosen_card = int(input("Choose a card: "))
                if chosen_card in validCards:
                    player_card = self.hand.pop(chosen_card - 1)
                    discardPile.append(player_card)
                    return
                else:
                    print("Invalid option, choose again")
                    
                

            except:
                print("Invalid option, choose again")

        
        



class Game:
    def __init__(self, deck):
        self.deck = deck
        self.discardPile = []
        self.players = []

    def startGame(self, playerAmount):
        self.players.append(HumanPlayer(self.deck.drawCard(7)))
        for _ in range(playerAmount - 1):
            self.players.append(ComputerPlayer(self.deck.drawCard(7)))
        self.discardPile.append(self.deck.drawCard(1)[0])
        print(f"Starting game with {playerAmount} players")
        
        

    def gameLoop(self):
        while True:
            for i, player in enumerate(self.players, start = 1):                
                print(f"Top Card: {self.discardPile[-1]}")
                
                if (i == 1):
                    player.playerTurn(self.discardPile)
                else:
                    pass
                    # player.chooseCard()

                time.sleep(1)
                

            



    

subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


cards = Deck.createDeck()
deck = Deck(cards)
deck.shuffleDeck()

game = Game(deck)
game.startGame(3)
game.gameLoop()