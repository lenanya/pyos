#pylint:disable=E0001
#pylint:disable=E0001
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

class Editor:
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        
        self.open_file = False
        
        self.current_folder = "./usr/files/"
        self.current_file = ""
        self.lines = [""]
        self.curr_line = 0
        self.lines_shown = [0, 100]
        self.files = [i for i in os.listdir(self.current_folder) if os.path.isfile(self.current_folder + i)]
        
        self.button_open = button.Button(0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, "Öffnen", self.font)
        self.open_buttons = []
        for i in range(len(self.files)):
            self.open_buttons.append(button.Button(5 * self.scale_horizontal, 105 * self.scale_vertical + 55 * i * self.scale_vertical, 190 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, self.files[i], self.font))
        
        self.open_file_hitbox = pygame.Rect(0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 60 * len(self.open_buttons) * self.scale_vertical)
        
        self.button_save = button.Button(205 * self.scale_horizontal, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, "Speichern", self.font)
        self.save_file = False
        
        self.save_file_hitbox = pygame.Rect(205 * self.scale_horizontal, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical)
        
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)
        
    def run(self, mouse_position, events):
        if not self.save_file:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # falls backspace
                        if self.lines[self.curr_line] == "" and self.curr_line > 0:
                            self.curr_line -= 1
                        self.lines[self.curr_line] = self.lines[self.curr_line][0:-1] # input um 1 verkuerzen
                    elif event.key == pygame.K_RETURN: # falls enter
                        self.lines.insert(self.curr_line + 1, "")
                        self.curr_line += 1
                    elif event.key == pygame.K_0: # TODO: arrow key
                        if self.curr_line != 0:
                            self.curr_line -= 1
                    elif event.key == pygame.K_1: # TODO: arrow key
                        if self.curr_line < len(self.lines):
                            self.curr_line += 1
                    else:
                        curr_char = event.unicode # gedrueckte taste zu input hinzufuegen
                        self.lines[self.curr_line] += curr_char
                    if self.curr_line >= self.lines_shown[1]:
                        self.lines_shown[0] += 1
                        self.lines_shown[1] += 1
                    if 0 != self.curr_line <= self.lines_shown[0]:
                        self.lines_shown[0] -= 1
                        self.lines_shown[1] -= 1
        else:
               for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # falls backspace
                        self.current_file = self.current_file[0:-1] # input um 1 verkuerzen
                    elif event.key == pygame.K_RETURN: # falls enter
                        text = ""
                        for i in self.lines:
                            text += i + "\n"
                        with open(self.current_folder + self.current_file, "w") as f:
                            f.write(text)
                        self.save_file = False
                    else:
                        curr_char = event.unicode # gedrueckte taste zu input hinzufuegen
                        self.current_file += curr_char
                    
    def draw(self):
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        
        if len(self.lines) != 0:
            txt_render = []
            for i in range(len(self.lines)):
                txt = self.lines[i]
                if i == self.curr_line:
                    txt += "_"
                txt_render.append(self.font.render(txt, 1, WHITE))
                
            txt_render = txt_render[self.lines_shown[0]:self.lines_shown[1]]
            
            for i in range(len(txt_render)):
                self.screen.blit(txt_render[i], (15 * self.scale_horizontal, 160 * self.scale_vertical + 40 * i * self.scale_vertical))
                
                
        if not self.open_file:
            self.button_open.draw()
        elif self.open_file:
            pygame.draw.rect(self.screen, WHITE, (0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 60 * len(self.open_buttons) * self.scale_vertical))
            for i in self.open_buttons:
                i.draw()
        if not self.save_file:
            self.button_save.draw()
        if self.save_file:
            pygame.draw.rect(self.screen, BLUE, (205 * self.scale_horizontal, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical))
            self.screen.blit(self.font.render(self.current_file, 1, WHITE), (205 * self.scale_horizontal, 105 * self.scale_vertical))
        
        self.button_exit.draw()
        
    def click_check(self, event_pos):
        if not self.open_file:
            if self.button_open.is_pressed(event_pos):
                self.open_file = True
                self.files = [i for i in os.listdir(self.current_folder) if os.path.isfile(self.current_folder + i)]
                self.open_buttons = []
                for i in range(len(self.files)):
                    self.open_buttons.append(button.Button(5 * self.scale_horizontal, 105 * self.scale_vertical + 55 * i * self.scale_vertical, 190 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, self.files[i], self.font))
                self.open_file_hitbox = pygame.Rect(0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 60 * len(self.open_buttons) * self.scale_vertical)
        if not self.save_file and not self.open_file:  
            if self.button_save.is_pressed(event_pos):
                self.save_file = True
        
        else:
            if not self.open_file_hitbox.collidepoint(event_pos):
                self.open_file = False
                
            if not self.save_file_hitbox.collidepoint(event_pos):
                self.save_file = False
                
            for i in self.open_buttons:
                if i.is_pressed(event_pos):
                    self.current_file =  i.text
                    with open(self.current_folder + self.current_file, "r") as f:
                        data = f.read()
                        print(data)
                    self.lines = data.split("\n")
                    amount_to_draw = round((970 * self.scale_vertical) / (40 * self.scale_vertical)) - 1 
                    self.lines_shown[1] = amount_to_draw
                    
                    
        if self.button_exit.is_pressed(event_pos):
            self.current_file = ""
            self.curr_line = 0
            self.lines = []
            self.save_file = False
            self.open_file = False
            return "exit"
            
            
            # TODO: fix keys