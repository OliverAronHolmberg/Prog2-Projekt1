import bcolors

class Card:
    def __init__(self, color):
        self.color = color

    Colors = [
        "Red",
        "Green",
        "Blue",
        "Yellow"
    ]

    Values = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    ]

    ActionTypes = [
        "Block", "Reverse", "+2"
    ]

    WildTypes = [
        "Wild Card", "+4"
    ]

    def __str__(self):
        return ""


class NumberCard(Card):
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        colorCode = bcolors.Bcolors.colors.get(self.color, bcolors.Bcolors.WHITE)
        return f"{colorCode}{self.color} | {self.value}{bcolors.Bcolors.ENDC}"


class ActionCard(Card):
    def __init__(self, color, actionType):
        self.color = color
        self.actionType = actionType

    def __str__(self):
        colorCode = bcolors.Bcolors.colors.get(self.color, bcolors.Bcolors.WHITE)
        return f"{colorCode}{self.color} | {self.actionType}{bcolors.Bcolors.ENDC}"


class WildCard(Card):
    def __init__(self, color, wildType):
        self.color = None
        self.wildType = wildType

    def __str__(self):
        if self.color is None:
            return f"{bcolors.Bcolors.PURPLE}Wild | {self.wildType}{bcolors.Bcolors.ENDC}"
        colorCode = bcolors.Bcolors.colors.get(self.color, bcolors.Bcolors.WHITE)
        return f"{colorCode}{self.color} | {self.wildType}{bcolors.Bcolors.ENDC}"