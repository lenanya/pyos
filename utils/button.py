# Class fuer Knoepfe
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)
YELLOW = (255, 255, 0)

class Button():
    def __init__(self, x, y, width, height, color, screen, text, font, image=None, image_on_hover=None, text_color=WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen
        self.text = text
        self.font = font
        self.image = image
        self.image_on_hover = image_on_hover
        self.text_color = text_color
        if self.image != None:
            self.image = pygame.transform.scale(pygame.image.load(self.image), (round(self.width), round(self.height)))
        if self.image_on_hover != None:
            self.image_on_hover = pygame.transform.scale(pygame.image.load(self.image_on_hover), (round(self.width), round(self.height)))
        self.sprite = self.image
        self.hitbox = pygame.Rect((self.x, self.y, self.width, self.height))
    
    # Funktion zum Anzeigen des Knopfes
    def draw(self):
        text_to_draw = self.font.render(self.text, True, self.text_color)
        if self.sprite == None:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
            self.screen.blit(text_to_draw, (self.x, self.y))
        if self.sprite != None:
            self.screen.blit(self.sprite, (self.x, self.y))
            

    # Funktion um zu ueberpruefen ob die Maus auf dem Knopf ist
    def is_hover(self, mouse_position):
        return self.hitbox.collidepoint(mouse_position)
    
    # Funktion um zu ueberpruefen ob der Knopf gedrueckt wurde
    def is_pressed(self, event_pos):
        return self.hitbox.collidepoint(event_pos)
    
# TODO: FIX TEXT ALIGNMENT LMAO
# TODO: ADD TEXT ALIGNMENT SETTING 