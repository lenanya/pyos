import pygame
import os
from utils import button
from screens import pex

# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)

class Terminal:
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        
        # ordner festlegen
        self.current_folder = "./usr/files"
        self.lines = ["./usr/files: "] # liste fuer linien festlegen
        self.curr_line = 0 # pointer fuer linien
        self.usr_input = "" # variable fuer input
        
        self.pex_active = False # variable ob pex aktiv

        # exit button
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)

    def eval_cmd(self, cmd):
        self.lines.append("")
        terms_cmd = cmd.split(" ") # befehl in teile aufteilen
        if terms_cmd[0] == "echo": # ausgabe
            self.lines[self.curr_line + 1] = cmd[4::]
            self.curr_line += 1
        elif terms_cmd[0] == "pex": # programm ausfuehren
            if terms_cmd[1] in os.listdir(self.current_folder): # TODO: bugfix if no file
                self.pex = pex.Pex(terms_cmd[1])
                self.pex_active = True
        elif terms_cmd[0] == "pexexit": # wird von pex gesendet
            self.pex_active = False
            self.usr_input = ""
            self.curr_line += 1
            self.lines[self.curr_line] = f"{self.current_folder}: {self.usr_input}"
        elif terms_cmd[0] == "cls": # clear
            self.lines = []
            self.curr_line = 0
            self.lines.append("")
            self.lines.append("")
            self.lines.append("")
        
    def run(self, mouse_position, events):
        if self.pex_active: # falls pex aktiv
            pex_output = self.pex.pex_run(mouse_position, events) # output von pex erhalten
            if pex_output != "": # wenn pex etwas returnt
                self.eval_cmd(pex_output) # als befehl evaluieren
        else: # falls pex nicht aktiv
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.lines.append("")
                    if event.key == pygame.K_BACKSPACE: # falls backspace
                        self.usr_input = self.usr_input[0:-1] # input um 1 verkuerzen
                    elif event.key == pygame.K_RETURN: # falls enter
                        self.eval_cmd(self.usr_input)  # befehl ausfuehren
                        self.usr_input = "" # input zuruecksetzen
                        self.curr_line += 1
                    else:
                        curr_char = event.unicode # gedrueckte taste zu input hinzufuegen
                        self.usr_input += curr_char
                    self.lines[self.curr_line] = f"{self.current_folder}: {self.usr_input}"

    def draw(self):
        # hintergrund
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        txt = "" # text variable
        txt_render = [] # liste von text render objekten
        for i in self.lines: # durch zeilen iterieren
            txt = i 
            txt_render.append(self.font.render(txt, 1, WHITE)) # fuer jede zeile text render objekt erstellen
        for i in range(len(txt_render)): # alle text render objekte anzeigen
            self.screen.blit(txt_render[i], (10 * self.scale_horizontal, 110 * self.scale_vertical + 40 * i * self.scale_vertical))
        
        self.button_exit.draw() # exit button anzeigen


    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos): # falls exit knopf gedrueckt
            self.pex_active = False                # alles zuruecksetzen
            self.current_folder = "./usr/files"    # und auf desktop zurueckkehren
            self.lines = ["./usr/files: "]
            self.curr_line = 0
            self.usr_input = ""
            return "exit"
        
    # TODO: ADD MORE CMDS
    # TODO: ADD SCROLLING (OOPS)
    # TODO: tree cmd