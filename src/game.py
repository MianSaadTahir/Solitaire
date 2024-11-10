import pygame
from cardDeck import CardDeck, CompressedDeck
from ui import Text, Button
from copy import deepcopy

light_gray = (211, 211, 211)
dark_blue = (28, 40, 51)
coral = (255, 127, 80)
slate_gray = (112, 128, 144)
light_yellow = (255, 255, 204)
black = (0, 0, 0)

display_dimensions = (1100, 900)
pygame.init()
game_display = pygame.display.set_mode(display_dimensions)
pygame.display.set_caption('Solitaire')
clock = pygame.time.Clock()
FPS = 10


def quit_game():
    pygame.quit()
    quit()


def win_screen():
    quit_button = Button(display_dimensions, "Exit", (300, 0), (250, 120),
                         coral, text_color=light_yellow, text_size=30, action="quit")
    play_again_button = Button(display_dimensions, "Replay", (0, 0), (
        250, 120), slate_gray, text_color=light_yellow, text_size=30, action="play_again")
    start_menu_button = Button(display_dimensions, "Main Menu", (-300, 0), (250, 120),
                               dark_blue, text_color=light_yellow, text_size=30, action="start_menu")
    buttons = [quit_button, play_again_button, start_menu_button]

    win_text = Text(display_dimensions, (0, -200),
                    "You Won!!!", 80, light_yellow)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "quit":
                                quit_game()
                            elif button.action == "play_again":
                                game_loop()
                            elif button.action == "start_menu":
                                start_menu()

        game_display.fill(light_gray)
        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())
        win_text.display(game_display)

        pygame.display.update()
        clock.tick(FPS)


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


def game_loop():
    undo_button = Button(display_dimensions, "Undo", (10, 10), (40, 40),
                         slate_gray, centered=False, text_size=15, action="undo")
    pause_button = Button(display_dimensions, "Pause", (
        display_dimensions[0]-60, 10), (50, 40), slate_gray, centered=False, text_size=15, action="pause")
    buttons = [undo_button, pause_button]

    deck = CardDeck()
    deck._initialize_deck()
    deck.shuffle_deck()
    deck._initialize_card_piles(display_dimensions)

    move_history = MoveHistory(deck)

    while True:
        if deck.check_for_win_condition():
            win_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_w:
                    win_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    piles_to_update, valid_move = deck.handle_left_click(
                        mouse_pos)
                    deck.update_deck(piles_to_update, display_dimensions[1])
                    if valid_move:
                        move_history.make_valid_move(deck)

                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "undo":
                                deck = move_history.revert_move(deck)

                if event.button == 3:
                    deck.handle_right_click(mouse_pos)

        game_display.fill(dark_blue)
        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        deck.display_deck(game_display)

        pygame.display.update()
        clock.tick(FPS)


def start_menu():
    title = Text(display_dimensions, (0, -100), "Solitaire", 70, light_yellow)

    play_button = Button(display_dimensions, "Start Game", (0, 0), (250, 120),
                         dark_blue, text_color=light_yellow, text_size=30, action="start_game")
    quit_button = Button(display_dimensions, "Exit", (300, 0), (250, 120),
                         coral, text_color=light_yellow, text_size=30, action="quit")
    buttons = [play_button, quit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "start_game":
                                game_loop()
                            elif button.action == "quit":
                                quit_game()

        game_display.fill(light_gray)
        title.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(FPS)


start_menu()
