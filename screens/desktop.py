import pygame
from utils import button

# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)

class Desktop():
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        
        self.background = pygame.transform.scale(pygame.image.load("./assets/desktop.png"), (round(1920 * scale_horizontal), round(980 * scale_vertical)))
        self.button_flappy = button.Button(10 * self.scale_horizontal, 110 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/flappy.png", "./assets/flappy_hover.png")
        self.button_minesweeper = button.Button(10 * self.scale_horizontal, 220 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/minesweeper.png", "./assets/minesweeper_hover.png")
        self.button_explorer = button.Button(10 * self.scale_horizontal, 330 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "expl", self.font)

    # Funktionen des Fensters
    def run(self, mouse_position, events):
        if self.button_flappy.is_hover(mouse_position):
            self.button_flappy.sprite = self.button_flappy.image_on_hover
        else:
            self.button_flappy.sprite = self.button_flappy.image
            
        if self.button_minesweeper.is_hover(mouse_position):
            self.button_minesweeper.sprite = self.button_minesweeper.image_on_hover
        else:
            self.button_minesweeper.sprite = self.button_minesweeper.image
    
    # Funktion zum anzeigen des Fensters
    def draw(self):
        self.screen.blit(self.background, (0, 100 * self.scale_vertical))
        self.button_flappy.draw()
        self.button_minesweeper.draw()
        self.button_explorer.draw()
        
    def click_check(self, event_pos):
        if self.button_flappy.is_pressed(event_pos):
            return "flappy"
        elif self.button_minesweeper.is_pressed(event_pos):
            return "minesweeper"
        elif self.button_explorer.is_pressed(event_pos):
            return "explorer"
        return "desktop"
    
# TODO: ADD PROGRAM NAMES 
# TODO: ADD RIGHT CLICK MENU
# TODO: UPDATE WALLPAPER
# TODO: ALLOW FOR FILES ON DESKTOP
# TODO: ?ADD DRAGGING
