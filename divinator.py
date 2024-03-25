from random import choice, randint
from lexicon import *


class Divination:
    def __init__(self):
        pass


class EightBall:
    def __init__(self):
        self._responses = ("it is certain", "it is decidedly so", "without a doubt", "yes definitely",
                           "you may rely on it",
                           "as i see it, yes", "most likely", "outlook good", "yes", "signs point to yes",
                           "reply hazy, try again", "ask again later", "better not tell you now", "cannot predict now",
                           "concentrate and ask again", "don't count on it", "my reply is no", "my sources say no",
                           "outlook not so good", "very doubtful")

    def get_response(self):
        return choice(self._responses)

    def divination(self):
        return f'my magic eight ball says "{self.get_response()}"'


class Tarot:
    def __init__(self):
        self._minor_num = ("ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "page",
                           "knight", "queen", "king")
        self._minor_suit = ("wands", "swords", "cups", "pentacles")
        self._minors = f"the {choice(self._minor_num)} of {choice(self._minor_suit)}"
        self._majors = choice(("the fool", "the magician", "the high priestess", "the empress", "the emperor",
                               "the hierophant", "the lovers", "the chariot", "strength", "the hermit",
                               "the wheel of fortune",
                               "justice", "the hanged man", "death", "temperance", "the devil", "the tower", "the star",
                               "the moon", "the sun", "judgement", "the world"))
        # TODO: move some of this to the divination method
        self._response = choice([self._majors, self._minors])

    def divination(self):
        return self._response


class PlayingCard:
    def __init__(self):
        self._num = ("ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                     "jack", "queen", "king")
        self._suit = ("clubs", "spades", "hearts", "diamonds")

    def get_num(self):
        return self._num

    def get_suit(self):
        return self._suit

    def divination(self):
        return f"the {choice(self.get_num())} of {choice(self.get_suit())}"


class Die:
    def __init__(self):
        self._dice = {4: "a four-sided die", 6: "a six-sided die", 8: "an eight-sided die", 10: "a ten-sided die",
                      12: "a twelve-sided die", 20: "a twenty-sided die"}
        self._numbers = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
                         9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
                         15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}

    def get_dice(self):
        return self._dice


    def get_numbers(self):
        return self._numbers

    def divination(self):
        die = choice([2, 4, 6, 8, 10, 12, 20])
        if die == 2:
            return f'i flipped a coin, it came up {choice(("heads", "tails"))}'
        result = randint(1, die)
        return f'i rolled {self.get_dice()[die]}, it came up {self.get_numbers()[result]}'
