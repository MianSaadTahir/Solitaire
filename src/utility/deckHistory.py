from copy import deepcopy
from cardDeck import CompressedDeck


class MoveHistory:
    def __init__(self, deck):
        self.current_index = 0
        self.history = []
        self.record_move(deck)

    def record_move(self, deck):
        self.history.append(CompressedDeck(deepcopy(deck.card_piles)))

    def make_valid_move(self, deck):
        self.record_move(deck)
        self.current_index += 1

    def revert_move(self, deck):
        if self.current_index > 0:
            del self.history[-1]
            self.current_index -= 1
            return deepcopy(self.history[self.current_index]).decompress(deck.card_images, deck.card_size)
        else:
            return deck
