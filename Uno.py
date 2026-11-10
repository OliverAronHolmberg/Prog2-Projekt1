import random
import subprocess
import os
import time

import bcolors

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
        color_code = bcolors.Bcolors.colors.get(self.color, bcolors.Bcolors.WHITE)
        return f"{color_code}{self.color} | {self.value}{bcolors.Bcolors.ENDC}"

class ActionCard(Card):
    def __init__(self, color, action_type):
        self.color = color
        self.action_type = action_type

    def __str__(self):
        color_code = bcolors.Bcolors.colors.get(self.color, bcolors.Bcolors.WHITE)
        return f"{color_code}{self.color} | {self.action_type}{bcolors.Bcolors.ENDC}"

class WildCard(Card):
    def __init__(self, color, wild_type):
        self.color = None
        self.wild_type = wild_type

    def __str__(self):
        if self.color is None:
            return f"{bcolors.Bcolors.PURPLE}Wild | {self.wild_type}{bcolors.Bcolors.ENDC}"
        color_code = bcolors.Bcolors.colors.get(self.color, bcolors.Bcolors.WHITE)
        return f"{color_code}{self.color} | {self.wild_type}{bcolors.Bcolors.ENDC}"


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

class ComputarPlayer(Player):
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def playTurn(self, topCard, deck, drawStack):
        print(f"{self.name}'s turn")

        

    
        

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

    def validMove(self, card, topCard):
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

    def canStack(self, drawStack):
        if drawStack <= 0:
            return False

        for card in self.hand:
            if card.__class__.__name__ == "ActionCard" and card.action_type == "+2":
                return True
            if card.__class__.__name__ == "WildCard" and card.wild_type == "+4":
                return True
        return False

    def playTurn(self, topCard, deck, drawStack):
        while True:
            print(f"Top card: {topCard}")
            print("-----------")
            print(f"{self.name}'s turn: ")
            for i, card in enumerate(self.hand, 1):
                print(f"{i}. {card}")

            if drawStack > 0:
                if self.canStack(drawStack):
                    print(f"{self.name} must either stack +2 or +4, or take the full +{drawStack} penalty.")
                    try:
                        option = int(input("Choose a card: "))
                    except:
                        print("Invalid option, try again")
                        continue

                    if option <= 0 or option > len(self.hand):
                        print("Invalid option, try again")
                        continue

                    selected_card = self.hand[option - 1]

                    if selected_card.__class__.__name__ == "ActionCard" and selected_card.action_type == "+2":
                        self.hand.pop(option - 1)
                        return selected_card

                    if selected_card.__class__.__name__ == "WildCard" and selected_card.wild_type == "+4":
                        selected_card.color = self.chooseColor()
                        self.hand.pop(option - 1)
                        return selected_card

                    print("Invalid. You must stack with +2 or +4, or take the penalty.")
                    continue

                print(f"{self.name} can't play +2/+4 and has to take the full +{drawStack} punishment.")
                input("Press Enter to draw the cards... ")
                for _ in range(drawStack):
                    if not deck.cards:
                        break
                    self.hand.append(deck.drawCards(1)[0])
                print(f"{self.name} picked up {drawStack} cards and skips the turn.")
                return "DrawStackPassed"

            if not self.canPlay(topCard):
                print(f"{self.name} can't play and has to draw 1 card at a time.")
                for _ in range(3):
                    if not deck.cards:
                        break

                    input("Press Enter to draw 1 card... ")
                    drawn_card = deck.drawCards(1)[0]
                    self.hand.append(drawn_card)

                    print(f"You drew: {drawn_card}")
                    print(f"Top card: {topCard}")
                    print("-----------")
                    print(f"{self.name}'s turn: ")
                    for i, card in enumerate(self.hand, 1):
                        print(f"{i}. {card}")

                    if self.canPlay(topCard):
                        print("You can play now. Choose a card from your hand.")
                        break

                if not self.canPlay(topCard):
                    print(f"{self.name} couldn't play after 3 cards and skips the turn.")
                    return "None"
                continue

            try:
                option = int(input("Choose a card: "))
            except:
                print("Invalid option, try again")
                continue

            if option <= 0 or option > len(self.hand):
                print("Invalid option, try again")
                continue

            selected_card = self.hand[option - 1]

            if self.validMove(selected_card, topCard):
                if selected_card.__class__.__name__ == "WildCard":
                    selected_card.color = self.chooseColor()
                self.hand.pop(option - 1)
                return selected_card

            print("Invalid card, try again.")


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
        direction = 1

        while True:
            if len(self.players) == 0:
                print("Game ended")
                return

            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
            move = self.players[currentPlayerIdx].playTurn(self.discardPile[-1], self.deck, drawStack)

            if move == "DrawStackPassed":
                drawStack = 0
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
                time.sleep(1)
                continue

            if move == "None":
                drawStack = 0
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
                time.sleep(1)
                continue

            self.discardPile.append(move)

            if len(self.players[currentPlayerIdx].hand) == 0:
                subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
                print(f"{self.players[currentPlayerIdx].name} has won!")
                return

            if move.__class__.__name__ == "WildCard" and move.wild_type == "+4":
                drawStack += 4
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
            elif move.__class__.__name__ == "ActionCard" and move.action_type == "+2":
                drawStack += 2
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
            elif move.__class__.__name__ == "ActionCard" and move.action_type == "Reverse":
                self.players.reverse()
                direction *= -1
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
            elif move.__class__.__name__ == "ActionCard" and move.action_type == "Block":
                currentPlayerIdx = (currentPlayerIdx + (2 * direction)) % len(self.players)
            else:
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)

            if len(self.players[currentPlayerIdx].hand) < 1:
                subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
                print(f"{self.players[currentPlayerIdx].name} wins!")
                return

            time.sleep(1)
            

cards = Deck.createDeck()       
deck = Deck(cards) 
deck.shuffleDeck()
game = Game(deck)

game.initiateGame(3)
game.playGame()