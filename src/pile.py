from collections import namedtuple


class Pile:
    def __init__(self, cards, x, y, dimensions, type="tableau"):
        self.CardOrder = namedtuple(
            'CardOrder', ['foundation', 'rank', 'color_suit'])
        self.CardW, self.CardH = dimensions

        # Set a default value for draw_three
        self.draw_three = False  # This is your default setting for draw_three

        self.type = type
        if self.type == 'tableau':
            self.fanned = True
            self.order = self.CardOrder(
                foundation='king', rank=-1, color_suit='alt-color')
            self.faceUp = 'top'
            self.height = 500
        elif self.type == 'foundation':
            self.fanned = False
            self.order = self.CardOrder(
                foundation='ace', rank=1, color_suit='same-suit')
            self.faceUp = 'all'
            self.height = self.CardH
        elif self.type == 'waste':
            self.fanned = False
            self.order = self.CardOrder(
                foundation=None, rank=None, color_suit=None)
            self.faceUp = 'all'
            self.height = self.CardH
        elif self.type == 'stock':
            self.fanned = False
            self.order = self.CardOrder(
                foundation=None, rank=None, color_suit=None)
            self.faceUp = 'none'
            self.height = self.CardH

        self.max_card_spacing = 60
        self.min_card_spacing = 10
        self.card_spacing = self.max_card_spacing
        self.bottom_margin = 10
        self.cards = cards
        self.x = x
        self.y = y
        self.adjust_pile()

    def card_bottom(self):
        return self.cards[-1].coordinate[1] + self.CardH if self.cards else self.y

    def adjust_pile(self):
        self.FaceUpChange()
        self.CardCoordinateChange()

    def CardCoordinateChange(self):
        if len(self.cards) > 0:
            for index, card in enumerate(self.cards):
                if self.fanned:
                    card.coordinate = (self.x, self.y +
                                       (index * self.card_spacing))
                else:
                    card.coordinate = (self.x, self.y)

    def FaceUpChange(self):
        if len(self.cards) != 0:
            for index, card in enumerate(self.cards):
                if self.faceUp == 'none':
                    card.faceUp = False
                elif self.faceUp == 'top' and index == len(self.cards) - 1:
                    card.faceUp = True
                elif self.faceUp == 'all':
                    card.faceUp = True

    def fit_pile_on_screen(self, screen_height):
        screen_bottom = screen_height - self.bottom_margin
        if len(self.cards) > 0:
            if self.card_bottom() > screen_bottom:
                while self.card_spacing > self.min_card_spacing:
                    if self.card_bottom() < screen_bottom:
                        break
                    else:
                        self.card_spacing -= 1 / len(self.cards)
                        self.CardCoordinateChange()
            elif self.card_bottom() < screen_bottom:
                while self.card_spacing < self.max_card_spacing:
                    if self.card_bottom() > screen_bottom:
                        break
                    else:
                        self.card_spacing += 1 / len(self.cards)
                        self.CardCoordinateChange()
            self.card_spacing = round(self.card_spacing)

    def check_if_selected(self, mouseCoordinate, piles):
        selection = False
        selected_cards = []
        deselect_pile = False
        for index, card in enumerate(self.cards):
            if card.checkClick(mouseCoordinate) and card.faceUp:
                selection = True
                selected_cards = self.cards[index:]
        if self.type == 'stock':
            deselect_pile = True
            wastepile = next(
                (pile for pile in piles if pile.type == 'waste'), None)
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
        if target_pile.type in ['stock', 'waste']:
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
        rect_x = card.getX() - padding
        rect_y = card.getY() - padding
        card_index = self.cards.index(card)
        if self.fanned:
            distance_from_top = card_index
        else:
            distance_from_top = 0
        rect_w = self.CardW + (padding * 2)
        rect_h = self.CardH + (padding * 2)
        return [rect_x, rect_y, rect_w, rect_h]

    def isClicked(self, mouseCoordinate):
        Xmouse, Ymouse = mouseCoordinate
        return self.x < Xmouse < self.x + self.CardW and self.y < Ymouse < self.y + self.height
