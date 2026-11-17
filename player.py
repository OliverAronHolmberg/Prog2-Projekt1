from card import Card, NumberCard, ActionCard, WildCard
from deck import Deck
import time
import random

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand


class ComputarPlayer(Player):
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def chooseColor(self, preferredColor=None):
        colorCounts = {color: 0 for color in Card.Colors}
        for card in self.hand:
            if card.__class__.__name__ != "WildCard" and getattr(card, "color", None) in colorCounts:
                colorCounts[card.color] += 1

        orderedColors = list(Card.Colors)
        if preferredColor in orderedColors:
            orderedColors = [preferredColor] + [c for c in orderedColors if c != preferredColor]

        for color in orderedColors:
            if colorCounts[color] > 0:
                return color

        if preferredColor is not None:
            return preferredColor

        return Card.Colors[random.randint(0, len(Card.Colors) - 1)]

    def pickBestCard(self, topCard):
        for cardType in ("NumberCard", "ActionCard", "WildCard"):
            for idx, card in enumerate(self.hand):
                if not self.validMove(card, topCard):
                    continue
                if card.__class__.__name__ == cardType:
                    return idx
        return None

    def validMove(self, card, topCard):
        if card.__class__.__name__ == "WildCard":
            return True

        if card.color == topCard.color:
            return True

        if topCard.__class__.__name__ == "NumberCard" and card.__class__.__name__ == "NumberCard":
            if card.value == topCard.value:
                return True

        if topCard.__class__.__name__ == "ActionCard" and card.__class__.__name__ == "ActionCard":
            if card.actionType == topCard.actionType:
                return True

        return False

    def canPlay(self, topCard):
        for card in self.hand:
            if self.validMove(card, topCard):
                return True
        return False

    def canStack(self, drawStack):
        if drawStack <= 0:
            return False

        for card in self.hand:
            if card.__class__.__name__ == "ActionCard" and card.actionType == "+2":
                return True
            if card.__class__.__name__ == "WildCard" and card.wildType == "+4":
                return True
        return False

    def playTurn(self, topCard, deck, drawStack):
        print(f"Top card: {topCard}")
        print("-----------")
        print(f"{self.name}'s turn")
        print(f"{self.name} is thinking...")
        time.sleep(random.randint(1, 2))

        if drawStack > 0:
            for idx, card in enumerate(self.hand):
                if card.__class__.__name__ == "ActionCard" and card.actionType == "+2":
                    self.hand.pop(idx)
                    print(f"{self.name} stacks +2")
                    return card

            for idx, card in enumerate(self.hand):
                if card.__class__.__name__ == "WildCard" and card.wildType == "+4":
                    self.hand.pop(idx)
                    card.color = self.chooseColor(getattr(topCard, "color", None))
                    print(f"{self.name} stacks +4")
                    return card

            print(f"{self.name} can't stack and draws +{drawStack} cards.")
            for _ in range(drawStack):
                if not deck.cards:
                    break
                self.hand.append(deck.drawCards(1)[0])
            return "DrawStackPassed"

        if not self.canPlay(topCard):
            for _ in range(3):
                if not deck.cards:
                    break
                self.hand.append(deck.drawCards(1)[0])
                if self.canPlay(topCard):
                    break

            if not self.canPlay(topCard):
                print(f"{self.name} can't play and passes.")
                return "None"

        bestChoice = self.pickBestCard(topCard)
        if bestChoice is None:
            return "None"

        selectedCard = self.hand.pop(bestChoice)
        if selectedCard.__class__.__name__ == "WildCard":
            selectedCard.color = self.chooseColor(getattr(topCard, "color", None))

        print(f"{self.name} plays {selectedCard}")
        return selectedCard

    def __str__(self):
        return self.name


class HumanPlayer(Player):
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def chooseColor(self):
        Colors = ["Red", "Green", "Blue", "Yellow"]
        while True:
            for i, color in enumerate(Colors, 1):
                print(f"{i}. {color}")
            try:
                choice = int(input("Choose a color (1-4): "))
                if 1 <= choice <= len(Colors):
                    return Colors[choice - 1]
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
                if card.actionType == topCard.actionType:
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
            if card.actionType == topCard.actionType:
                return True

        return False

    def canStack(self, drawStack):
        if drawStack <= 0:
            return False

        for card in self.hand:
            if card.__class__.__name__ == "ActionCard" and card.actionType == "+2":
                return True
            if card.__class__.__name__ == "WildCard" and card.wildType == "+4":
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

                    selectedCard = self.hand[option - 1]

                    if selectedCard.__class__.__name__ == "ActionCard" and selectedCard.actionType == "+2":
                        self.hand.pop(option - 1)
                        return selectedCard

                    if selectedCard.__class__.__name__ == "WildCard" and selectedCard.wildType == "+4":
                        selectedCard.color = self.chooseColor()
                        self.hand.pop(option - 1)
                        return selectedCard

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
                    drawnCard = deck.drawCards(1)[0]
                    self.hand.append(drawnCard)

                    print(f"You drew: {drawnCard}")
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

            selectedCard = self.hand[option - 1]

            if self.validMove(selectedCard, topCard):
                if selectedCard.__class__.__name__ == "WildCard":
                    selectedCard.color = self.chooseColor()
                self.hand.pop(option - 1)
                return selectedCard

            print("Invalid card, try again.")