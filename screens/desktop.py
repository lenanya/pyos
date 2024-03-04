import pygame
from utils import button
import time

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
        
        # hintergrund bild laden
        with open("./settings/desktop_background.txt", "r") as f:
            self.bg_image = f.read()
        self.background = pygame.transform.scale(pygame.image.load(self.bg_image), (round(1920 * scale_horizontal), round(980 * scale_vertical)))
        # buttons fuer programme erstellen
        self.button_flappy = button.Button(10 * self.scale_horizontal, 110 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/flappy.png", "./assets/flappy_hover.png")
        self.button_minesweeper = button.Button(10 * self.scale_horizontal, 220 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/minesweeper.png", "./assets/minesweeper_hover.png")
        self.button_explorer = button.Button(10 * self.scale_horizontal, 330 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/explorer.png", "./assets/explorer_hover.png")
        self.button_terminal = button.Button(10 * self.scale_horizontal, 440 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/terminal.png", "./assets/terminal_hover.png")
        self.button_editor = button.Button(10 * self.scale_horizontal, 550 * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "", self.font, "./assets/editor.png", "./assets/editor_hover.png")

        
        
    # Funktionen des Fensters
    def run(self, mouse_position, events):
        # falls maus auf knopf => zu hover sprite wechseln
        if self.button_flappy.is_hover(mouse_position):
            self.button_flappy.sprite = self.button_flappy.image_on_hover
        else:
            self.button_flappy.sprite = self.button_flappy.image
            
        if self.button_minesweeper.is_hover(mouse_position):
            self.button_minesweeper.sprite = self.button_minesweeper.image_on_hover
        else:
            self.button_minesweeper.sprite = self.button_minesweeper.image
            
        if self.button_explorer.is_hover(mouse_position):
            self.button_explorer.sprite = self.button_explorer.image_on_hover
        else:
            self.button_explorer.sprite = self.button_explorer.image
        
        if self.button_terminal.is_hover(mouse_position):
            self.button_terminal.sprite = self.button_terminal.image_on_hover
        else:
            self.button_terminal.sprite = self.button_terminal.image
            
        if self.button_editor.is_hover(mouse_position):
            self.button_editor.sprite = self.button_editor.image_on_hover
        else:
            self.button_editor.sprite = self.button_editor.image
    
    # Funktion zum anzeigen des Fensters
    def draw(self):
        # hintergrundbild anzeigen
        with open("./settings/desktop_background.txt", "r") as f:
            self.bg_image = f.read()
        self.background = pygame.transform.scale(pygame.image.load(self.bg_image), (round(1920 * self.scale_horizontal), round(980 * self.scale_vertical)))
        self.screen.blit(self.background, (0, 100 * self.scale_vertical))
        self.button_flappy.draw() # alle buttons anzeigen
        self.button_minesweeper.draw()
        self.button_explorer.draw()
        self.button_terminal.draw()
        self.button_editor.draw()
        
    def click_check(self, event_pos):
        if self.button_flappy.is_pressed(event_pos): # ueberpruefen ob buttons gedrueckt sind,
            return "flappy"                          # wenn ja, name des programms returnen
        elif self.button_minesweeper.is_pressed(event_pos):
            return "minesweeper"
        elif self.button_explorer.is_pressed(event_pos):
            return "explorer"
        elif self.button_terminal.is_pressed(event_pos):
            return "terminal"
        elif self.button_editor.is_pressed(event_pos):
            return "editor"
        return "desktop"
    
# TODO: ADD PROGRAM NAMES 
# TODO: ADD RIGHT CLICK MENU
# TODO: fix lag