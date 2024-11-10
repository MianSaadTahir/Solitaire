import random


class Card:
    def __init__(self, name_of_image, card_size, rank, suit, face_up=False):
        self.name_of_image = name_of_image
        self.card_size = card_size
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
        self.color = self.checkColor()
        self.position = (0, 0)

    def checkColor(self):
        if self.suit == 'clubs' or self.suit == 'spades':
            return 'black'
        elif self.suit == 'hearts' or self.suit == 'diamonds':
            return 'red'

    def is_clicked(self, mouse_position):
        width, height = self.card_size
        mouse_x, mouse_y = mouse_position
        return self.getX() < mouse_x < self.getX() + width and self.getY() < mouse_y < self.getY() + height

    def getX(self):
        return self.position[0]

    def getY(self):
        return self.position[1]

    def toString(self):
        return "{} of {}".format(self.rank, self.suit)

    def print(self):
        return self.toString()
