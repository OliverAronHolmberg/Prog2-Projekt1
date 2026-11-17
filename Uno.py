import time
import subprocess
import os

from player import Player, HumanPlayer, ComputarPlayer
from card import Card, ActionCard, NumberCard, WildCard
from deck import Deck



class Game:
    def __init__(self, deck=None, terminal = False):
        if deck is None:
            deck = []
        self.deck = deck
        self.discardPile = []
        self.players = []
        self.gameOptions = ["Any - New game", "Q - Quit"]
        self.terminal = terminal

    def mainMenu(self):
        while True:
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
            print("Welcome to UNO")
            print("--------------")
            for option in self.gameOptions:
                print(f" * {option}")

            choose = input("Choose an option: ")
            if choose.upper() == "Q":
                exit(0)
            else:
                while True:
                    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
                    print("NEW GAME")
                    print("---------")
                    try:
                        playerAmount = int(input("How many players?: "))
                        self.initiateGame(playerAmount)
                        self.playGame()
                        break
                    except:
                        print("Invalid input, try again.")

    def initiateGame(self, playerAmount):
        self.players.append(HumanPlayer("Player 1", self.deck.drawCards(7)))
        for i in range(playerAmount - 1):
            self.players.append(ComputarPlayer(f"Player {i + 2}", self.deck.drawCards(7)))

        while True:
            startCard = self.deck.drawCards(1)
            if not startCard:
                raise ValueError("The deck is empty, cannot start the game.")

            self.discardPile.append(startCard[0])

            if self.discardPile[-1].__class__.__name__ in ("WildCard", "ActionCard"):
                self.deck.extend(self.discardPile[-1:])
                self.discardPile.pop()
                self.deck.shuffleDeck()
                continue

            break
        return

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

            if len(self.deck.cards) < 1:
                tempDeck = self.discardPile[:-1]
                self.discardPile = self.discardPile[-1]
                self.deck.extend(tempDeck)
                self.deck.shuffleDeck()

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

            if move.__class__.__name__ == "WildCard" and move.wildType == "+4":
                drawStack += 4
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
            elif move.__class__.__name__ == "ActionCard" and move.actionType == "+2":
                drawStack += 2
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
            elif move.__class__.__name__ == "ActionCard" and move.actionType == "Reverse":
                direction *= -1
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)
            elif move.__class__.__name__ == "ActionCard" and move.actionType == "Block":
                currentPlayerIdx = (currentPlayerIdx + (2 * direction)) % len(self.players)
            else:
                currentPlayerIdx = (currentPlayerIdx + direction) % len(self.players)

            if len(self.players[currentPlayerIdx].hand) < 1:
                subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
                print(f"{self.players[currentPlayerIdx].name} wins!")
                return

            time.sleep(1)


if __name__ == "__main__":
    cards = Deck.createDeck()
    deck = Deck(cards)
    deck.shuffleDeck()
    game = Game(deck, False)

    game.mainMenu()
