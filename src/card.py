import random


class Card:
    def __init__(self, name_of_image, card_size, rank, suit, face_up=False):
        self.name_of_image = name_of_image
        self.card_size = card_size
        self.suit = suit
        self.rank = rank
        self.face_up = face_up
        self.color = self._determine_color()
        self.position = (0, 0)

    def _determine_color(self):
        if self.suit == 'diamonds' or self.suit == 'hearts':
            return 'red'
        elif self.suit == 'spades' or self.suit == 'clubs':
            return 'black'

    def is_clicked(self, mouse_position):
        width, height = self.card_size
        mouse_x, mouse_y = mouse_position
        return self.get_x() < mouse_x < self.get_x() + width and self.get_y() < mouse_y < self.get_y() + height

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return self.__str__()
