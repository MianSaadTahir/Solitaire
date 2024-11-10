import pygame
from Deck import Deck

light_gray = (211, 211, 211)
dark_blue = (28, 40, 51)
coral = (255, 127, 80)
slate_gray = (112, 128, 144)
light_yellow = (255, 255, 204)
black = (0, 0, 0)

display_dimensions = (1100, 900)
pygame.init()
screen = pygame.display.set_mode(display_dimensions)
pygame.display.set_caption('Solitaire')


def quit_game():
    pygame.quit()
    quit()


def game_loop():

    deck = Deck()
    deck.initDeck()
    deck.deckShuffle()
    deck.initPile(display_dimensions)

    while True:
        # if deck.winCheck():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    changedPiles, valid_move = deck.handle_left_click(
                        mouse_pos)
                    deck.Deckupdate(changedPiles, display_dimensions[1])

        screen.fill(dark_blue)

        deck.deckPrint(screen)

        pygame.display.update()


game_loop()
