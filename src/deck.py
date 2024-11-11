import pygame
import random
import os
from card import Card
from pile import Pile


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

        # back card name
        name = os.path.join(
            '..', 'assets', 'cards', 'back_card.png')
        # link card with its image
        self.backCard = pygame.image.load(name)
        self.faceDownCard = self.placeFaceDownCard()

    def placeFaceDownCard(self):
        return pygame.transform.scale(self.backCard, self.dimensions)

    def initPile(self, size):
        width, h = size
        padding = 50
        # 100 to the right
        Xinitial = 90
        # 150 below card height (dimension)
        Yinitial = self.dimensions[1] + 150

        # stock and waste piles
        stock = Pile(
            self.cards[28:], Xinitial, padding, self.dimensions, type="stock")
        waste = Pile([], Xinitial + self.dimensions[0] + padding,
                     padding, self.dimensions, type="waste")

        # foundation piles spacing
        fPadding = self.dimensions[0] + padding
        # foundation pile initial position
        fInitial = width - (fPadding * 4)

        # foundations
        f1 = Pile(
            [], fInitial, padding, self.dimensions, type="foundation")
        f2 = Pile([], fInitial + fPadding,
                  padding, self.dimensions, type="foundation")
        f3 = Pile([], fInitial + fPadding * 2,
                  padding, self.dimensions, type="foundation")
        f4 = Pile([], fInitial + fPadding * 3,
                  padding, self.dimensions, type="foundation")

        # tableaus
        t1 = Pile([self.cards[0]], Xinitial, Yinitial, self.dimensions)
        t2 = Pile(
            self.cards[1:3], Xinitial + self.dimensions[0] + padding, Yinitial, self.dimensions)
        t3 = Pile(self.cards[3:6], Xinitial + self.dimensions[0]
                  * 2 + padding * 2, Yinitial, self.dimensions)
        t4 = Pile(self.cards[6:10], Xinitial + self.dimensions[0]
                  * 3 + padding * 3, Yinitial, self.dimensions)
        t5 = Pile(self.cards[10:15], Xinitial + self.dimensions[0]
                  * 4 + padding * 4, Yinitial, self.dimensions)
        t6 = Pile(self.cards[15:21], Xinitial + self.dimensions[0]
                  * 5 + padding * 5, Yinitial, self.dimensions)
        t7 = Pile(self.cards[21:28], Xinitial + self.dimensions[0]
                  * 6 + padding * 6, Yinitial, self.dimensions)

        # collection of all piles
        self.pileCards = [t1, t2, t3, t4, t5, t6,
                          t7, stock, waste, f1, f2, f3, f4]

    def initDeck(self):
        for suit in self.suit:
            for rank in self.rank:
                name = os.path.join(
                    '..', 'assets', 'cards', '{}_of_{}.png'.format(rank, suit))
                self.imgs[name] = pygame.image.load(
                    name)
                self.cards.append(
                    Card(name, self.dimensions, rank, suit))
        self.resizeImgs()

    # display deck
    def deckPrint(self, screen):
        for pile in self.pileCards:
            # draw blank box for foundations
            if pile.type == 'foundation' or (pile.type == 'deck' and len(pile.cards) == 0):
                pygame.draw.rect(screen, self.slotBGcolor, [
                                 pile.x, pile.y, pile.CardW, pile.CardH])
            # iterate through each card in a pile
            for card in pile.cards:
                # highlight the selected card if it is selected
                if self.isSelected and self.selectedCardBoxDimension and card == self.cardsSelected[0]:
                    # draw rectangular box around card
                    pygame.draw.rect(
                        screen, self.selectionHighlightedColor, self.selectedCardBoxDimension)
                # get relevant card image if face up else place back of card
                img = self.imgs[card.name] if card.faceUp else self.faceDownCard
                # place retrieved card image on screen display
                screen.blit(img, [card.getX(), card.getY()])

    # update deck after a card or a pile is moved
    def Deckupdate(self, changedPiles, Yaxis):
        for pile in self.pileCards:
            pile.FaceUpChange()
            pile.CardCoordinateChange()
        if changedPiles:
            for pile in changedPiles:
                pile.fit_pile_on_screen(Yaxis)
                pile.CardCoordinateChange()

    # shuffle the cards deck
    def deckShuffle(self):
        random.shuffle(self.cards)

    # in imgs dictionary, retrieve each img name and value and set its relevant dimension size
    def resizeImgs(self):
        for name, imgOFcard in self.imgs.items():
            self.imgs[name] = pygame.transform.scale(
                imgOFcard, self.dimensions)

    # chek if any pile of cards is clicked
    def checkPileClick(self, mouseCoordinate):
        for pile in self.pileCards:
            if pile.isClicked(mouseCoordinate):
                return pile
        return None

    # undo card selection
    def deSelect(self):
        self.isSelected = False
        self.pileSelected = None
        self.cardsSelected = []

    # card select mouse event
    def handle_left_click(self, mouseCoordinate):
        changedPiles = None
        valid_move = False

        if not self.isSelected:
            self.pileSelected = self.checkPileClick(mouseCoordinate)

            if self.pileSelected:
                self.isSelected, self.cardsSelected, deselect_pile = self.pileSelected.check_if_selected(
                    mouseCoordinate, self.pileCards)

            if self.pileSelected:
                if self.pileSelected.type == 'stock':
                    valid_move = True
                # undo selection
                if deselect_pile:
                    self.deSelect()
                else:
                    if len(self.cardsSelected) != 0:
                        self.selectedCardBoxDimension = self.pileSelected.get_selection_area(
                            self.cardsSelected[0])
        else:
            pile_to_transfer_to = self.checkPileClick(mouseCoordinate)
            if self.pileSelected and pile_to_transfer_to:
                valid_move = self.pileSelected.move_cards_to_pile(
                    self.cardsSelected, pile_to_transfer_to, self.rank)
                changedPiles = self.pileSelected, pile_to_transfer_to
            else:
                changedPiles = None
            self.deSelect()
        return changedPiles, valid_move

    # win condition
    def winCheck(self):
        foundations = [
            pile for pile in self.pileCards if pile.type == 'foundation']
        for pile in foundations:
            if len(pile.cards) < 13:
                return False
        return True