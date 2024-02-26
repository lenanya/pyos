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

class Settings():
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        
        self.show_taskbar_color_changer = False
        self.taskbar_color_changer_hitbox = pygame.Rect((50 * self.scale_horizontal, 150 * self.scale_vertical, 400 * self.scale_horizontal, 400 * self.scale_vertical))

        self.button_taskbar_color = button.Button(50 * self.scale_horizontal, 150 * self.scale_vertical, 400 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "Farbe der Taskleiste", self.font)
        self.button_taskbar_blue = button.Button(55 * self.scale_horizontal, 155 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Blau", self.font)
        self.button_taskbar_red = button.Button(55 * self.scale_horizontal, 255 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Rot", self.font)
        self.button_taskbar_green = button.Button(55 * self.scale_horizontal, 355 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Grün", self.font)
        self.button_taskbar_white = button.Button(55 * self.scale_horizontal, 455 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Weiß", self.font)
                
        
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)
		
		
		
    # Funktionen des Fensters
    def run(self, mouse_position, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_taskbar_color_changer:
                    self.click_check(event.pos)
                if self.button_taskbar_color.is_pressed(event.pos):
                    self.show_taskbar_color_changer = True

        if self.button_taskbar_color.is_hover(mouse_position):
            self.button_taskbar_color.color = TEAL
        else:
            self.button_taskbar_color.color = BLUE
            
        if self.button_taskbar_blue.is_hover(mouse_position):
            self.button_taskbar_blue.color = TEAL
        else:
            self.button_taskbar_blue.color = BLUE
            
        if self.button_taskbar_red.is_hover(mouse_position):
            self.button_taskbar_red.color = TEAL
        else:
            self.button_taskbar_red.color = BLUE
            
        if self.button_taskbar_green.is_hover(mouse_position):
            self.button_taskbar_green.color = TEAL
        else:
            self.button_taskbar_green.color = BLUE
        
        if self.button_taskbar_white.is_hover(mouse_position):
            self.button_taskbar_white.color = TEAL
        else:
            self.button_taskbar_white.color = BLUE
    
    
    # Funktion zum anzeigen des Fensters
    def draw(self):
        pygame.draw.rect(self.screen, GREY, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        self.button_taskbar_color.draw()
        pygame.draw.rect(self.screen, WHITE, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 50 * self.scale_vertical))
        self.button_exit.draw()
        if self.show_taskbar_color_changer:
            pygame.draw.rect(self.screen, WHITE, (50 * self.scale_horizontal, 150 * self.scale_vertical, 400 * self.scale_horizontal, 400 * self.scale_vertical))
            self.button_taskbar_blue.draw()
            self.button_taskbar_red.draw()
            self.button_taskbar_green.draw()
            self.button_taskbar_white.draw()

    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos):
            return "exit"
        if self.show_taskbar_color_changer:
            
            if self.button_taskbar_blue.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("BLUE")
            if self.button_taskbar_red.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("RED")
            if self.button_taskbar_green.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("GREEN")
            if self.button_taskbar_white.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("WHITE")
                    
            if not self.taskbar_color_changer_hitbox.collidepoint(event_pos):
                self.show_taskbar_color_changer = False
            return "settings"


# TODO: ADD MORE TASKBAR COLORS / CUSTOM ONES
# TODO: ADD MORE SETTINGS
# TODO: MOVE SETTINGS TO JSON FILE 
# TODO: ADD WALLPAPER SETTING
# TODO: ADD TIME ZONE SETTING
# TODO: ?ADD LANGUAGES
