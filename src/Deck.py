import pygame
from itertools import count
import random
import os
from card import Card
from pile import pile


class Deck:
    def __init__(self, pileCards=[], imgs={}, dimensions=(80, 120)):
        self.dimensions = dimensions
        self.imgs = imgs
        self.pileCards = pileCards

        self.isSelected = False
        self.cardsSelected = []
        self.pileSelected = None

        self.selectedCardBoxDimension = None
        self.selectionHighlightedColor = (255, 0, 0)
        self.slotBGcolor = (0, 128, 0)

        self.suit = ['hearts', 'diamonds', 'spades', 'clubs']
        self.cards = []
        self.rank = ['ace', '2', '3', '4', '5', '6',
                     '7', '8', '9', '10', 'jack', 'queen', 'king']

        # card names
        name = os.path.join(
            '..', 'assets', 'cards', 'back_card.png')
        # link card with its image
        self.backCard = pygame.image.load(name)
        self.resizeCard = self.reSize()

    def reSize(self):
        return pygame.transform.scale(self.backCard, self.dimensions)

    def resizeImgs(self):
        for name, imgOFcard in self.imgs.items():
            self.imgs[name] = pygame.transform.scale(
                imgOFcard, self.dimensions)

    def _initialize_deck(self):
        for suit in self.suit:
            for rank in self.rank:
                name = os.path.join(
                    '..', 'assets', 'cards', '{}_of_{}.png'.format(rank, suit))
                self.imgs[name] = pygame.image.load(
                    name)
                self.cards.append(
                    Card(name, self.dimensions, rank, suit))
        self.resizeImgs()

    def _initialize_pileCards(self, display_size):
        display_width, display_height = display_size
        pile_spacing = 50
        start_x = 50
        start_y = self.dimensions[1] + 100
        foundation_x_step = self.dimensions[0] + pile_spacing
        foundation_start_x = display_width - (foundation_x_step * 4)
        tableau1 = pile([self.cards[0]], start_x, start_y, self.dimensions)
        tableau2 = pile(
            self.cards[1:3], start_x + self.dimensions[0] + pile_spacing, start_y, self.dimensions)
        tableau3 = pile(self.cards[3:6], start_x + self.dimensions[0]
                        * 2 + pile_spacing * 2, start_y, self.dimensions)
        tableau4 = pile(self.cards[6:10], start_x + self.dimensions[0]
                        * 3 + pile_spacing * 3, start_y, self.dimensions)
        tableau5 = pile(self.cards[10:15], start_x + self.dimensions[0]
                        * 4 + pile_spacing * 4, start_y, self.dimensions)
        tableau6 = pile(self.cards[15:21], start_x + self.dimensions[0]
                        * 5 + pile_spacing * 5, start_y, self.dimensions)
        tableau7 = pile(self.cards[21:28], start_x + self.dimensions[0]
                        * 6 + pile_spacing * 6, start_y, self.dimensions)
        stock = pile(
            self.cards[28:], start_x, pile_spacing, self.dimensions, pile_type="stock")
        waste = pile([], start_x + self.dimensions[0] + pile_spacing,
                     pile_spacing, self.dimensions, pile_type="waste")
        foundation1 = pile(
            [], foundation_start_x, pile_spacing, self.dimensions, pile_type="foundation")
        foundation2 = pile([], foundation_start_x + foundation_x_step,
                           pile_spacing, self.dimensions, pile_type="foundation")
        foundation3 = pile([], foundation_start_x + foundation_x_step * 2,
                           pile_spacing, self.dimensions, pile_type="foundation")
        foundation4 = pile([], foundation_start_x + foundation_x_step * 3,
                           pile_spacing, self.dimensions, pile_type="foundation")
        self.pileCards = [tableau1, tableau2, tableau3, tableau4, tableau5, tableau6, tableau7, stock, waste,
                          foundation1, foundation2, foundation3, foundation4]

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def reset_selection(self):
        self.isSelected = False
        self.pileSelected = None
        self.cardsSelected = []

    def _identify_clicked_pile(self, mouseCoordinate):
        for pile in self.pileCards:
            if pile.is_pile_clicked(mouseCoordinate):
                return pile
        return None

    def update_deck(self, piles_to_update, display_height):
        for pile in self.pileCards:
            pile.update_faceUp()
            pile.update_card_positions()
        if piles_to_update:
            for pile in piles_to_update:
                pile.fit_pile_on_screen(display_height)
                pile.update_card_positions()

    def handle_left_click(self, mouseCoordinate):
        piles_to_update = None
        valid_move = False
        if not self.isSelected:
            self.pileSelected = self._identify_clicked_pile(mouseCoordinate)
            if self.pileSelected:
                if self.pileSelected.pile_type == 'stock':
                    valid_move = True
            if self.pileSelected:
                self.isSelected, self.cardsSelected, deselect_pile = self.pileSelected.check_if_selected(
                    mouseCoordinate, self.pileCards)
                if deselect_pile:
                    self.reset_selection()
                else:
                    if len(self.cardsSelected) != 0:
                        self.selectedCardBoxDimension = self.pileSelected.get_selection_area(
                            self.cardsSelected[0])
        else:
            pile_to_transfer_to = self._identify_clicked_pile(mouseCoordinate)
            if self.pileSelected and pile_to_transfer_to:
                valid_move = self.pileSelected.move_cards_to_pile(
                    self.cardsSelected, pile_to_transfer_to, self.rank)
                piles_to_update = self.pileSelected, pile_to_transfer_to
            else:
                piles_to_update = None
            self.reset_selection()
        return piles_to_update, valid_move

    def handle_right_click(self, mouseCoordinate):
        self.reset_selection()

    def check_for_win_condition(self):
        foundation_piles = [
            pile for pile in self.pileCards if pile.pile_type == 'foundation']
        for pile in foundation_piles:
            if len(pile.cards) < 13:
                return False
        return True

    def display_deck(self, game_display):
        for pile in self.pileCards:
            if pile.pile_type == 'foundation' or (pile.pile_type == 'deck' and len(pile.cards) == 0):
                pygame.draw.rect(game_display, self.slotBGcolor, [
                                 pile.x, pile.y, pile.card_width, pile.card_height])
            for card in pile.cards:
                if self.isSelected and self.selectedCardBoxDimension and card == self.cardsSelected[0]:
                    pygame.draw.rect(
                        game_display, self.selectionHighlightedColor, self.selectedCardBoxDimension)
                img = self.imgs[card.name] if card.faceUp else self.resizeCard
                game_display.blit(img, [card.getX(), card.getY()])


class CompressedDeck:
    _ids = count(0)

    def __init__(self, pileCards):
        self.id = next(self._ids)
        self.pileCards = pileCards

    def decompress(self, imgs, dimensions):
        return Deck(self.pileCards, imgs, dimensions)

    def toString(self):
        return str([card for card in self.pileCards if card.faceUp])

    def print(self):
        return f"CompressedDeck #{self.id}"
