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
        
        self.show_taskbar_color_changer = False # ob menue fuer farbe angezeigt wird
        # hitbox um zu gucken ob ausserhalb des menues geklick wird
        self.taskbar_color_changer_hitbox = pygame.Rect((50 * self.scale_horizontal, 150 * self.scale_vertical, 400 * self.scale_horizontal, 400 * self.scale_vertical))

        # buttons fuer farbwechselmenue
        self.button_taskbar_color = button.Button(50 * self.scale_horizontal, 150 * self.scale_vertical, 400 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, self.screen, "Farbe der Taskleiste", self.font)
        self.button_taskbar_blue = button.Button(55 * self.scale_horizontal, 155 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Blau", self.font)
        self.button_taskbar_red = button.Button(55 * self.scale_horizontal, 255 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Rot", self.font)
        self.button_taskbar_green = button.Button(55 * self.scale_horizontal, 355 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Grün", self.font)
        self.button_taskbar_white = button.Button(55 * self.scale_horizontal, 455 * self.scale_vertical, 390 * self.scale_horizontal, 90 * self.scale_vertical, BLUE, self.screen, "Weiß", self.font)
                
        # exit knopf
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)
		
		
		
    # Funktionen des Fensters
    def run(self, mouse_position, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: # falls geklick wird
                if self.show_taskbar_color_changer: # falls farbwechselmenue sichtbar ist
                    self.click_check(event.pos) # ueberpruefen ob einer der buttons gedrueckt ist
                if self.button_taskbar_color.is_pressed(event.pos): # falls einstellungsknopf gedrueckt wird
                    self.show_taskbar_color_changer = True # farbwechselmenue anzeigen

        # wie in main.py, buttons farbe/sprite aendern falls hover
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
        # hintergrund
        pygame.draw.rect(self.screen, GREY, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        self.button_taskbar_color.draw() # einstellungsknopf anzeigen
        self.button_exit.draw() # exit button anzeigen
        if self.show_taskbar_color_changer: # falls einstellung offen, buttons anzeigen
            # hintergrund fuer menue anzeigen
            pygame.draw.rect(self.screen, WHITE, (50 * self.scale_horizontal, 150 * self.scale_vertical, 400 * self.scale_horizontal, 400 * self.scale_vertical))
            # knoepfe anzeigen
            self.button_taskbar_blue.draw()
            self.button_taskbar_red.draw()
            self.button_taskbar_green.draw()
            self.button_taskbar_white.draw()

    def click_check(self, event_pos):
        # falls exit button gedrueckt ist
        # auf den desktop gehen
        if self.button_exit.is_pressed(event_pos): 
            return "exit"
        
        if self.show_taskbar_color_changer: # falls farbwechselmenue offen ist
            # fuer jeden knopf ueberpruefen ob gedrueckt
            if self.button_taskbar_blue.is_pressed(event_pos): 
                with open("./settings/taskbarcolor.txt", "w") as f: # einstellungsdatei oeffnen
                    f.write("BLUE") # ausgewaehlte farbe schreiben
            if self.button_taskbar_red.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("RED")
            if self.button_taskbar_green.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("GREEN")
            if self.button_taskbar_white.is_pressed(event_pos):
                with open("./settings/taskbarcolor.txt", "w") as f:
                    f.write("WHITE")
                    
            if not self.taskbar_color_changer_hitbox.collidepoint(event_pos): # falls ausserhalb von menue geklickt
                self.show_taskbar_color_changer = False # menue nicht mehr anzeigen
            return "settings" # falls nicht geschlossen, fenster bleibt gleich


# TODO: ADD MORE TASKBAR COLORS / CUSTOM ONES
# TODO: ADD MORE SETTINGS
# TODO: MOVE SETTINGS TO JSON FILE 
# TODO: ADD WALLPAPER SETTING
# TODO: ADD TIME ZONE SETTING
# TODO: ?ADD LANGUAGES
