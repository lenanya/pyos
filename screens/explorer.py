import pygame
import os
from utils import button

# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)

class Explorer():
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font

        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)

        self.current_folder = "./usr/files/"
        self.dirs = []
        self.files = []
        self.buttons = []

        for i in os.listdir(self.current_folder):
            if os.path.isfile(self.current_folder+ i):
                self.files.append(i)
            else:
                self.dirs.append(i)

        print(self.dirs)
        print(self.files)

    def run(self, mouse_position, events):
        for i in self.dirs:
            self.buttons.append(button.Button((200 )))

    def draw(self):
        pygame.draw.rect(self.screen, GREY, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        self.button_exit.draw()

    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos):
            return "exit"
