import pygame
import os
from utils import button
from screens import pex
import time

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
        
        self.pex = "" # variable fuer pex klasse
        
        # ordner festlegen
        self.current_folder = "./usr/files"
        self.lines = ["./usr/files: "] # liste fuer linien festlegen
        self.curr_line = 0 # pointer fuer linien
        self.usr_input = "" # variable fuer input
        
        self.pex_active = False # variable ob pex aktiv
        self.pex_input_active = False # variable ob pex programm input verlangt
        self.pex_input = "" # variable fuer pex input
        self.pex_input_variable = "" # pex variable in die der input gespeichert wird

        self.text_color = WHITE # variable fuer text farbe
        
        # exit button
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)

    def eval_cmd(self, cmd):
        self.lines.append("")
        terms_cmd = cmd.split(" ") # befehl in teile aufteilen
        if terms_cmd[0] == "echo": # ausgabe
            self.lines[self.curr_line + 1] = cmd[5::] # alles nach 'echo ' ausgeben
            self.curr_line += 1
        elif terms_cmd[0] == "pex": # programm ausfuehren
            if len(terms_cmd) < 2: # falls keine Datei angegeben
                self.lines[self.curr_line + 1] = "Keine Datei angegeben"
                self.curr_line += 1
            elif terms_cmd[1] in os.listdir(self.current_folder): # falls datei vorhanden
                self.pex = pex.Pex(terms_cmd[1]) # pex klasse mit dieser datei initialisieren
                self.pex_active = True # pex auf aktiv setzen
            else: # falls datei nicht vorhanden
                self.lines[self.curr_line + 1] = "Datei nicht vorhanden"
                self.curr_line += 1
        elif terms_cmd[0] == "pexexit": # wird von pex gesendet wenn das programm beendet wird oder einen fehler hat
            self.pex_active = False # pex beenden und zuruecksetzen
            self.pex_input_active = False
            self.pex_input = ""
            self.usr_input = ""
            self.curr_line += 1
            self.lines[self.curr_line] = f"{cmd[8::]}" # exit code ausgeben
            self.curr_line += 1
            self.lines[self.curr_line] = f"{self.current_folder}: {self.usr_input}"
        elif terms_cmd[0] == "cls": # clear
            self.lines = []
            self.curr_line = 0
            self.lines.append("")
            self.lines.append("")
            self.lines.append("")
        elif terms_cmd[0] == "pinput": # fuer pex um input zu erhalten
            self.pex_input_active = True
            self.pex_input = ""
            self.pex_input_variable = terms_cmd[1]
            self.curr_line += 1
            self.lines[self.curr_line] = "to pex: _"
        elif terms_cmd[0] == "color": # text farbe aendern mit 3 zahlen von 0 - 255
            for i in terms_cmd[1:4]: # sichergehen dass es zahlen sind
                valid_color = True
                if not i.isnumeric():
                    valid_color = False
                    break
                if not 0 <= int(i) <= 255: # sichergehen, dass die zahlen zwischen 0 und 255 sind
                    valid_color = False
                    break
            if valid_color:
                self.text_color = [int(i) for i in terms_cmd[1:4]]
        
    def run(self, mouse_position, events):
        if self.pex_active: # falls pex aktiv
            if not self.pex_input_active:
                try:
                    pex_output = self.pex.pex_run(mouse_position, events) # output von pex erhalten
                except IndexError:
                    pex_output ="pexexit Programm hat kein \'end\'"
                except Exception: # falls ein fehler von pex ausgeht
                    pex_output = "pexexit Fehler"
                if pex_output != "": # wenn pex etwas returnt
                    self.eval_cmd(pex_output) # als befehl evaluieren
                
            if self.pex_input_active:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.lines.append("")
                        if event.key == pygame.K_BACKSPACE: # falls backspace
                            self.pex_input = self.pex_input[0:-1] # input um 1 verkuerzen
                        elif event.key == pygame.K_RETURN: # falls enter
                            if self.pex_input.isnumeric(): # falls input zahl ist zu float konvertieren
                                self.pex_input = float(self.pex_input)
                            self.pex.variables[self.pex_input_variable] = self.pex_input  # input an pex geben
                            self.pex_input = "" # input zuruecksetzen
                            self.pex_input_active = False
                            self.curr_line += 1
                        else:
                            curr_char = event.unicode # gedrueckte taste zu input hinzufuegen
                            self.pex_input += curr_char
                        if self.pex_input_active:   
                            self.lines[self.curr_line] = f"to pex: {self.pex_input}_"
                        
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
                    if not self.pex_active:
                        self.lines[self.curr_line] = f"{self.current_folder}: {self.usr_input}"

    def draw(self):
        # hintergrund
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        txt = "" # text variable
        txt_render = [] # liste von text render objekten
        lines = [i for i in self.lines if i] # platzhalter zeilen entfernen
        
        for i in range(len(lines)): # durch zeilen iterieren
            txt = lines[i] # zeilenzahl + text
            if i == self.curr_line and time.time() % 1 > 0.5: # falls die zeile die momentan editierte ist
                txt += "_" # "cursor" ans ende hinzufuegen
            txt_render.append(self.font.render(txt, 1, WHITE)) # text zur liste hinzufuegen
        # nur so viele zeilen wie auf den bildschirm passen
        amount_to_draw = round((970 * self.scale_vertical) / (40 * self.scale_vertical)) - 1 
       
        txt_render = txt_render[-amount_to_draw::] # laenge anpassen
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
        
    # TODO: tree cmd
    # TODO: help cmd