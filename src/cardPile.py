from collections import namedtuple


class CardPile:
    def __init__(self, cards, x, y, card_size, pile_type="tableau"):
        self.CardOrder = namedtuple(
            'CardOrder', ['foundation', 'rank', 'color_suit'])
        self.card_width, self.card_height = card_size

        # Set a default value for draw_three
        self.draw_three = False  # This is your default setting for draw_three

        self.pile_type = pile_type
        if self.pile_type == 'tableau':
            self.fanned = True
            self.order = self.CardOrder(
                foundation='king', rank=-1, color_suit='alt-color')
            self.face_up = 'top'
            self.height = 500
        elif self.pile_type == 'foundation':
            self.fanned = False
            self.order = self.CardOrder(
                foundation='ace', rank=1, color_suit='same-suit')
            self.face_up = 'all'
            self.height = self.card_height
        elif self.pile_type == 'waste':
            self.fanned = False
            self.order = self.CardOrder(
                foundation=None, rank=None, color_suit=None)
            self.face_up = 'all'
            self.height = self.card_height
        elif self.pile_type == 'stock':
            self.fanned = False
            self.order = self.CardOrder(
                foundation=None, rank=None, color_suit=None)
            self.face_up = 'none'
            self.height = self.card_height

        self.max_card_spacing = 60
        self.min_card_spacing = 10
        self.card_spacing = self.max_card_spacing
        self.bottom_margin = 10
        self.cards = cards
        self.x = x
        self.y = y
        self.adjust_pile()

    def card_bottom(self):
        return self.cards[-1].position[1] + self.card_height if self.cards else self.y

    def adjust_pile(self):
        self.update_face_up()
        self.update_card_positions()

    def update_card_positions(self):
        if len(self.cards) > 0:
            for index, card in enumerate(self.cards):
                if self.fanned:
                    card.position = (self.x, self.y +
                                     (index * self.card_spacing))
                else:
                    card.position = (self.x, self.y)

    def update_face_up(self):
        if len(self.cards) != 0:
            for index, card in enumerate(self.cards):
                if self.face_up == 'none':
                    card.face_up = False
                elif self.face_up == 'top' and index == len(self.cards) - 1:
                    card.face_up = True
                elif self.face_up == 'all':
                    card.face_up = True

    def fit_pile_on_screen(self, screen_height):
        screen_bottom = screen_height - self.bottom_margin
        if len(self.cards) > 0:
            if self.card_bottom() > screen_bottom:
                while self.card_spacing > self.min_card_spacing:
                    if self.card_bottom() < screen_bottom:
                        break
                    else:
                        self.card_spacing -= 1 / len(self.cards)
                        self.update_card_positions()
            elif self.card_bottom() < screen_bottom:
                while self.card_spacing < self.max_card_spacing:
                    if self.card_bottom() > screen_bottom:
                        break
                    else:
                        self.card_spacing += 1 / len(self.cards)
                        self.update_card_positions()
            self.card_spacing = round(self.card_spacing)

    def check_if_selected(self, mouse_position, piles):
        selection = False
        selected_cards = []
        deselect_pile = False
        for index, card in enumerate(self.cards):
            if card.is_clicked(mouse_position) and card.face_up:
                selection = True
                selected_cards = self.cards[index:]
        if self.pile_type == 'stock':
            deselect_pile = True
            wastepile = next(
                (pile for pile in piles if pile.pile_type == 'waste'), None)
            if len(self.cards) != 0:
                if self.draw_three:
                    index_range = min(len(self.cards), 3)
                    for _ in range(index_range):
                        wastepile.cards.append(self.cards[-1])
                        del self.cards[-1]
                else:
                    wastepile.cards.append(self.cards[-1])
                    del self.cards[-1]
            else:
                self.cards = wastepile.cards[::-1]
                wastepile.cards = []
        return selection, selected_cards, deselect_pile

    def is_transfer_valid(self, target_pile, selected_cards, rank_order):
        if len(target_pile.cards) != 0:
            bottom_card = target_pile.cards[-1]
        else:
            bottom_card = None
        top_card = selected_cards[0]
        valid = True
        if target_pile.pile_type in ['stock', 'waste']:
            valid = False
        if bottom_card is None:
            if target_pile.order.foundation is not None:
                if top_card.rank != target_pile.order.foundation:
                    valid = False
        else:
            if target_pile.order.rank is not None:
                rank_index = rank_order.index(bottom_card.rank)
                if top_card.rank != rank_order[rank_index + target_pile.order.rank]:
                    valid = False
            if target_pile.order.color_suit is not None:
                if target_pile.order.color_suit == 'alt-color':
                    if top_card.color == bottom_card.color:
                        valid = False
                elif target_pile.order.color_suit == 'same-suit':
                    if top_card.suit != bottom_card.suit:
                        valid = False
        return valid

    def move_cards_to_pile(self, selected_cards, target_pile, rank_order):
        if self.is_transfer_valid(target_pile, selected_cards, rank_order):
            for card in selected_cards:
                target_pile.cards.append(card)
                self.cards.remove(card)
            return True
        return False

    def get_selection_area(self, card):
        padding = 10
        rect_x = card.get_x() - padding
        rect_y = card.get_y() - padding
        card_index = self.cards.index(card)
        if self.fanned:
            distance_from_top = card_index
        else:
            distance_from_top = 0
        rect_w = self.card_width + (padding * 2)
        rect_h = self.card_height + (padding * 2)
        return [rect_x, rect_y, rect_w, rect_h]

    def is_pile_clicked(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        return self.x < mouse_x < self.x + self.card_width and self.y < mouse_y < self.y + self.height
