import random
import subprocess
import os
import time

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

    def drawCards(self, num):
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




class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

        COLORS = []

class HumanPlayer(Player):
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    
    def chooseColor(self):
        COLORS = ["Red", "Green", "Blue", "Yellow"]
        while True:
            for i, color in enumerate(COLORS, 1):
                print(f"{i}. {color}")
            try:
                choice = int(input("Choose a color (1-4): "))
                if 1 <= choice <= len(COLORS):
                    return COLORS[choice - 1]
                print("Invalid color, try again.")
            except:
                print("Invalid color, try again.")
    



    def playTurn(self, topCard, deck, drawStack):

        topCardType = topCard.__class__.__name__

        if not self.canPlay(topCard):
            print(f"{self.name} can't play a card, drawing up to 3 cards...")
            for _ in range(3):
                if not deck.cards:
                    print("No more cards in deck.")
                    break

                drawn_card = deck.drawCards(1)[0]
                self.hand.append(drawn_card)
                print(f"{self.name} drew 1 card: {drawn_card}")

                if self.canPlay(topCard):
                    print(f"{self.name} can play the drawn card: {drawn_card}")
                    if drawn_card.__class__.__name__ == "WildCard":
                        drawn_card.color = self.chooseColor()
                    self.hand.pop()
                    return drawn_card

            print(f"{self.name} still couldn't play after 3 cards.")
            return "None"

        while True:
            print(f"Top card: {topCard}")
            print("-----------")
            print(f"{self.name}'s turn: ")
            for i, card in enumerate(self.hand, 1):
                print(f"{i}. {card}")

            try:
                option = int(input("Choose a card: "))

                if option > 0 and option <= len(self.hand):
                    selected_card = self.hand[option - 1]

                    if topCardType == "WildCard" and topCard.wild_type == "+4":
                        if selected_card.__class__.__name__ == "WildCard":
                            if selected_card.wild_type == "+4":
                                selected_card.color = self.chooseColor()
                                self.hand.pop(option - 1)
                                return selected_card
                            else:
                                print("Invalid option, try again.")
                                continue

                        elif selected_card.__class__.__name__ == "ActionCard":
                            if selected_card.action_type == "+2" and selected_card.color == topCard.color:
                                self.hand.pop(option - 1)
                                return selected_card
                        else:
                            self.hand.extend(deck.drawCards(drawStack))
                            print(f"{self.name} drew {drawStack} cards")
                            return "None"

                    if selected_card.__class__.__name__ == "WildCard":
                        selected_card.color = self.chooseColor()
                        self.hand.pop(option - 1)
                        return selected_card

                    if selected_card.color == topCard.color:
                        self.hand.pop(option - 1)
                        return selected_card

                    if topCardType == "NumberCard" and selected_card.__class__.__name__ == "NumberCard":
                        if selected_card.value == topCard.value:
                            self.hand.pop(option - 1)
                            return selected_card

                    if topCardType == "ActionCard":
                        if selected_card.__class__.__name__ == "WildCard":
                            self.hand.pop(option - 1)
                            return selected_card

                        elif selected_card.__class__.__name__ == "ActionCard":
                            if selected_card.action_type == topCard.action_type:
                                self.hand.pop(option - 1)
                                return selected_card

                    elif topCardType == "NumberCard":
                        if selected_card.__class__.__name__ == "WildCard":
                            self.hand.pop(option - 1)
                            return selected_card

                    print("Invalid card, try again.")
                    if drawStack > 0:
                        print(f"You have a draw stack of {drawStack}.")
                    continue

                else:
                    print("Invalid option, try again")
            except:
                print("Invalid option, try again")

        

    def drawUpToThree(self, topCard, deck):
        for _ in range(3):
            if self.canPlay(topCard):
                return False

            if not deck.cards:
                print("No more cards in deck.")
                return False

            drawn_card = deck.drawCards(1)[0]
            self.hand.append(drawn_card)
            print(f"{self.name} drew 1 card: {drawn_card}")

            if self.canPlay(topCard):
                return True

        return False

    def canPlay(self, topCard):
        for card in self.hand:
            if card.__class__.__name__ == "WildCard":
                return True

            if card.color == topCard.color:
                return True

            if topCard.__class__.__name__ == "NumberCard" and card.__class__.__name__ == "NumberCard":
                if card.value == topCard.value:
                    return True

            if topCard.__class__.__name__ == "ActionCard" and card.__class__.__name__ == "ActionCard":
                if card.action_type == topCard.action_type:
                    return True

        return False
    

class Game():
    def __init__(self, deck=None):
        if deck == None:
            deck = []
        self.deck = deck
        self.discardPile = []

        self.players = []

    def initiateGame(self, playerAmount):
        self.players.append(HumanPlayer("Player 1", self.deck.drawCards(7)))
        for i in range(playerAmount - 1):
            self.players.append(HumanPlayer(f"Player {i + 2}", self.deck.drawCards(7)))

        self.discardPile.extend(self.deck.drawCards(1))


    def playGame(self):
        currentPlayerIdx = 0
        drawStack = 0
        playersOut = 0

        while True:
            if len(self.players) > 0:
                subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
                newTopCard = self.players[currentPlayerIdx].playTurn(self.discardPile[-1], self.deck, drawStack)
                print(f"Card chosen: {newTopCard}")
                if len(self.players[currentPlayerIdx].hand) < 1:
                    self.players.pop(currentPlayerIdx)
                    if playersOut == 0:
                        print(f"Player {currentPlayerIdx} has won")
                    else:
                        print(f"Player {currentPlayerIdx} has exited in {playersOut + 1}:nd place")

                if newTopCard is not None and newTopCard != "None":
                    self.discardPile.append(newTopCard)

                if newTopCard.__class__.__name__ == "WildCard" and newTopCard.wild_type == "+4":
                    drawStack += 4
                elif newTopCard.__class__.__name__ == "ActionCard" and newTopCard.action_type == "+2":
                    drawStack += 2
                elif newTopCard.__class__.__name__ == "ActionCard" and newTopCard.action_type == "Reverse":
                    self.players.reverse()
                elif newTopCard.__class__.__name__ == "ActionCard" and newTopCard.action_type == "Block":
                    currentPlayerIdx += 1
                

                currentPlayerIdx += 1
                if currentPlayerIdx >= len(self.players):
                    currentPlayerIdx = 0
                time.sleep(3)
            else:
                print("Game ended")
                return
            

cards = Deck.createDeck()       
deck = Deck(cards) 
deck.shuffleDeck()
game = Game(deck)

game.initiateGame(2)
game.playGame()