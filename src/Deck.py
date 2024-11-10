import os
import random
import pygame
from itertools import count
from collections import deque
from pile import pile
from card import Card


class Deck:
    def __init__(self, card_piles=[], card_images={}, card_size=(100, 150)):
        self.cards = []
        self.suits = ['clubs', 'diamonds', 'hearts', 'spades']
        self.ranks = ['ace', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10', 'jack', 'queen', 'king']
        self.selection = False
        self.selected_cards = []
        self.selected_pile = None
        self.selection_rect = None
        self.selection_color = (0, 0, 0)
        self.empty_color = (100, 100, 200)
        self.card_piles = card_piles
        self.card_images = card_images
        self.card_size = card_size
        name = os.path.join(
            '..', 'assets', 'cards', 'back_card.png')
        self.card_back_image = pygame.image.load(name)
        self.card_back = self._resize_card_back()
        self.card_selection_history = deque()

    def _resize_card_back(self):
        return pygame.transform.scale(self.card_back_image, self.card_size)

    def _resize_all_card_images(self):
        for name, card_image in self.card_images.items():
            self.card_images[name] = pygame.transform.scale(
                card_image, self.card_size)

    def _initialize_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                name = os.path.join(
                    '..', 'assets', 'cards', '{}_of_{}.png'.format(rank, suit))
                self.card_images[name] = pygame.image.load(
                    name)
                self.cards.append(
                    Card(name, self.card_size, rank, suit))
        self._resize_all_card_images()

    def _initialize_card_piles(self, display_size):
        display_width, display_height = display_size
        pile_spacing = 50
        start_x = 50
        start_y = self.card_size[1] + 100
        foundation_x_step = self.card_size[0] + pile_spacing
        foundation_start_x = display_width - (foundation_x_step * 4)
        tableau1 = pile([self.cards[0]], start_x, start_y, self.card_size)
        tableau2 = pile(
            self.cards[1:3], start_x + self.card_size[0] + pile_spacing, start_y, self.card_size)
        tableau3 = pile(self.cards[3:6], start_x + self.card_size[0]
                        * 2 + pile_spacing * 2, start_y, self.card_size)
        tableau4 = pile(self.cards[6:10], start_x + self.card_size[0]
                        * 3 + pile_spacing * 3, start_y, self.card_size)
        tableau5 = pile(self.cards[10:15], start_x + self.card_size[0]
                        * 4 + pile_spacing * 4, start_y, self.card_size)
        tableau6 = pile(self.cards[15:21], start_x + self.card_size[0]
                        * 5 + pile_spacing * 5, start_y, self.card_size)
        tableau7 = pile(self.cards[21:28], start_x + self.card_size[0]
                        * 6 + pile_spacing * 6, start_y, self.card_size)
        stock = pile(
            self.cards[28:], start_x, pile_spacing, self.card_size, pile_type="stock")
        waste = pile([], start_x + self.card_size[0] + pile_spacing,
                     pile_spacing, self.card_size, pile_type="waste")
        foundation1 = pile(
            [], foundation_start_x, pile_spacing, self.card_size, pile_type="foundation")
        foundation2 = pile([], foundation_start_x + foundation_x_step,
                           pile_spacing, self.card_size, pile_type="foundation")
        foundation3 = pile([], foundation_start_x + foundation_x_step * 2,
                           pile_spacing, self.card_size, pile_type="foundation")
        foundation4 = pile([], foundation_start_x + foundation_x_step * 3,
                           pile_spacing, self.card_size, pile_type="foundation")
        self.card_piles = [tableau1, tableau2, tableau3, tableau4, tableau5, tableau6, tableau7, stock, waste,
                           foundation1, foundation2, foundation3, foundation4]

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def reset_selection(self):
        self.selection = False
        self.selected_pile = None
        self.selected_cards = []

    def _identify_clicked_pile(self, mouseCoordinate):
        for pile in self.card_piles:
            if pile.is_pile_clicked(mouseCoordinate):
                return pile
        return None

    def update_deck(self, piles_to_update, display_height):
        for pile in self.card_piles:
            pile.update_faceUp()
            pile.update_card_positions()
        if piles_to_update:
            for pile in piles_to_update:
                pile.fit_pile_on_screen(display_height)
                pile.update_card_positions()

    def handle_left_click(self, mouseCoordinate):
        piles_to_update = None
        valid_move = False
        if not self.selection:
            self.selected_pile = self._identify_clicked_pile(mouseCoordinate)
            if self.selected_pile:
                if self.selected_pile.pile_type == 'stock':
                    valid_move = True
            if self.selected_pile:
                self.selection, self.selected_cards, deselect_pile = self.selected_pile.check_if_selected(
                    mouseCoordinate, self.card_piles)
                if deselect_pile:
                    self.reset_selection()
                else:
                    if len(self.selected_cards) != 0:
                        self.selection_rect = self.selected_pile.get_selection_area(
                            self.selected_cards[0])
        else:
            pile_to_transfer_to = self._identify_clicked_pile(mouseCoordinate)
            if self.selected_pile and pile_to_transfer_to:
                valid_move = self.selected_pile.move_cards_to_pile(
                    self.selected_cards, pile_to_transfer_to, self.ranks)
                piles_to_update = self.selected_pile, pile_to_transfer_to
            else:
                piles_to_update = None
            self.reset_selection()
        return piles_to_update, valid_move

    def handle_right_click(self, mouseCoordinate):
        self.reset_selection()

    def check_for_win_condition(self):
        foundation_piles = [
            pile for pile in self.card_piles if pile.pile_type == 'foundation']
        for pile in foundation_piles:
            if len(pile.cards) < 13:
                return False
        return True

    def display_deck(self, game_display):
        for pile in self.card_piles:
            if pile.pile_type == 'foundation' or (pile.pile_type == 'deck' and len(pile.cards) == 0):
                pygame.draw.rect(game_display, self.empty_color, [
                                 pile.x, pile.y, pile.card_width, pile.card_height])
            for card in pile.cards:
                if self.selection and self.selection_rect and card == self.selected_cards[0]:
                    pygame.draw.rect(
                        game_display, self.selection_color, self.selection_rect)
                img = self.card_images[card.name] if card.faceUp else self.card_back
                game_display.blit(img, [card.getX(), card.getY()])


class CompressedDeck:
    _ids = count(0)

    def __init__(self, card_piles):
        self.id = next(self._ids)
        self.card_piles = card_piles

    def decompress(self, card_images, card_size):
        return Deck(self.card_piles, card_images, card_size)

    def toString(self):
        return str([card for card in self.card_piles if card.faceUp])

    def print(self):
        return f"CompressedDeck #{self.id}"
