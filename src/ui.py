import os
import pygame
from math import sqrt

check_img = pygame.image.load(os.path.join(
    '..', 'assets', 'cards', 'Assess.jpg'))


class Button:
    def __init__(self, display_dimensions, text, offsets, dimensions, color, text_size=16, text_color=(0, 0, 0), enabled=True, centered=True, action=None):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.width, self.height = dimensions
        self.enabled = enabled
        self.disabled_color = (200, 200, 200)
        self.disabled_text_color = (230, 230, 230)
        self.text = text
        self.text_color = text_color
        text_display_color = self.disabled_color if not self.enabled else self.text_color
        self.text_object = Text(
            display_dimensions, (0, 0), text, text_size, text_display_color, centered=False)
        self.color = color
        self.highlight_strength = 20
        self.centered = centered
        self.action = action

    def get_x(self):
        return ((self.display_width // 2) - (self.width // 2)) + self.x_offset if self.centered else self.x_offset

    def get_y(self):
        return ((self.display_height // 2) - (self.height // 2)) + self.y_offset if self.centered else self.y_offset

    def check_for_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.get_x() < mouse_x < self.get_x() + self.width and self.get_y() < mouse_y < self.get_y() + self.height

    def check_if_clicked(self, mouse_pos):
        return self.check_for_mouse_over(mouse_pos) and self.enabled

    def highlight_color(self):
        return tuple(min(255, value + self.highlight_strength) for value in self.color)

    def display(self, game_display, mouse_pos):
        button_color = self.highlight_color() if self.check_for_mouse_over(
            mouse_pos) and self.enabled else self.color
        if not self.enabled:
            button_color = self.disabled_color
            self.text_object.color = self.disabled_text_color
        button_info = (self.get_x(), self.get_y(), self.width, self.height)
        pygame.draw.rect(game_display, button_color, list(button_info))
        self.text_object.button_text_display(game_display, button_info)


class RadioGroup:
    def __init__(self, *args):
        self.radios = list(args)

    def __iter__(self):
        return iter(self.radios)

    def check_if_clicked(self, mouse_pos):
        for radio in self.radios:
            radio.check_if_clicked(mouse_pos, self)

    def display(self, game_display):
        for radio in self.radios:
            radio.display(game_display)


class Radio:
    def __init__(self, display_dimensions, offsets, centered=True, checked=False, enabled=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.centered = centered
        self.checked = checked
        self.enabled = enabled
        self.size = 10
        self.margin = 4
        self.color = (200, 200, 200)
        self.checked_color = (50, 50, 50)

    def get_x(self):
        return (self.display_width // 2) + self.x_offset if self.centered else self.x_offset

    def get_y(self):
        return (self.display_height // 2) + self.y_offset if self.centered else self.y_offset

    def check_for_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        distance = sqrt((abs(self.get_x() - mouse_x) ** 2) +
                        (abs(self.get_y() - mouse_y) ** 2))
        return distance < self.size

    def check_if_clicked(self, mouse_pos, radio_group):
        if self.check_for_mouse_over(mouse_pos) and self.enabled:
            for radio in radio_group:
                radio.checked = radio == self

    def display(self, game_display):
        pygame.draw.circle(game_display, self.color,
                           (self.get_x(), self.get_y()), self.size)
        if self.checked:
            pygame.draw.circle(game_display, self.checked_color,
                               (self.get_x(), self.get_y()), self.size - self.margin)


class Checkbox:
    def __init__(self, display_dimensions, offsets, centered=True, checked=False, enabled=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.centered = centered
        self.checked = checked
        self.enabled = enabled
        self.size = 20
        self.checkmark = check_img
        self.color = (200, 200, 200)
        self.checked_color = (50, 50, 50)

    def get_x(self):
        return ((self.display_width // 2) - (self.size // 2)) + self.x_offset if self.centered else self.x_offset

    def get_y(self):
        return ((self.display_height // 2) - (self.size // 2)) + self.y_offset if self.centered else self.y_offset

    def check_for_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.get_x() < mouse_x < self.get_x() + self.size and self.get_y() < mouse_y < self.get_y() + self.size

    def check_if_clicked(self, mouse_pos):
        if self.check_for_mouse_over(mouse_pos) and self.enabled:
            self.checked = not self.checked

    def display(self, game_display):
        pygame.draw.rect(game_display, self.color, [
                         self.get_x(), self.get_y(), self.size, self.size])
        if self.checked:
            self.checkmark = pygame.transform.scale(
                self.checkmark, (self.size, self.size))
            game_display.blit(self.checkmark, [self.get_x(), self.get_y()])


class Text:
    def __init__(self, display_dimensions, offsets, text, size, color, font="OpenSans-Bold", centered=True):
        self.display_width, self.display_height = display_dimensions
        self.x_offset, self.y_offset = offsets
        self.text = text
        self.size = size
        self.color = color
        name_of_font = os.path.join(
            '..', 'assets', 'fonts', font + '.ttf')
        self.font = pygame.font.Font(name_of_font, self.size)
        self.centered = centered

    def text_objects(self):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        return text_surface, text_rect

    def display(self, game_display):
        text_surface, text_rect = self.text_objects()
        if self.centered:
            text_rect.center = (self.display_width // 2 + self.x_offset,
                                self.display_height // 2 + self.y_offset)
            game_display.blit(text_surface, text_rect)
        else:
            game_display.blit(text_surface, [self.x_offset, self.y_offset])

    def button_text_display(self, game_display, button_info):
        text_surface, text_rect = self.text_objects()
        x, y, width, height = button_info
        text_rect.center = (x + width // 2, y + height // 2)
        game_display.blit(text_surface, text_rect)
