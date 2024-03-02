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
        
        # basic variablen
        self.current_folder = "./usr/files/" # ordner
        self.current_file = "" # variable fuer momentane datei
        self.lines = [""] # liste fuer zeilen 
        self.curr_line = 0 # momentane zeile
        self.lines_shown = [0, round((920 * self.scale_vertical) / (40 * self.scale_vertical)) - 1] # angezeigte zeilen
        self.files = [i for i in os.listdir(self.current_folder) if os.path.isfile(self.current_folder + i)] # vorhandene dateien
        
        # knopf zum oeffnen von dateien 
        self.button_open = button.Button(0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, "Öffnen", self.font)
        self.open_buttons = [] # liste fuer knoepfe
        for i in range(len(self.files)): # fuer jede datei einen knopf hinzufuegen
            self.open_buttons.append(button.Button(5 * self.scale_horizontal, 105 * self.scale_vertical + 55 * i * self.scale_vertical, 190 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, self.files[i], self.font))
        
        # hitbox falls man ausserhalb klickt
        self.open_file_hitbox = pygame.Rect(0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 60 * len(self.open_buttons) * self.scale_vertical)
        
        # knopf zum speichern
        self.button_save = button.Button(205 * self.scale_horizontal, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, "Speichern", self.font)
        self.save_file = False # variable um zu ueberpruefen ob gerade gespeichert wird
        
        # hitbox falls man ausserhalb klickt
        self.save_file_hitbox = pygame.Rect(205 * self.scale_horizontal, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical)
        
        #exit knopf
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)
        
    def run(self, mouse_position, events):
        if not self.save_file: # falls das save menu nicht geoeffnet ist
            for event in events:
                if event.type == pygame.KEYDOWN: # input manager
                    if event.key == pygame.K_BACKSPACE: # falls backspace
                        if self.lines[self.curr_line] == "" and self.curr_line > 0: # wenn zeile leer
                            self.lines.pop(self.curr_line) # zeile entfernen
                            self.curr_line -= 1 # eine zeile zurueckgehen
                        else: # wenn zeile nicht leer
                            self.lines[self.curr_line] = self.lines[self.curr_line][0:-1] # zeile um 1 verkuerzen
                    elif event.key == pygame.K_RETURN: # falls enter
                        self.lines.insert(self.curr_line + 1, "") # neue zeile einfuegen
                        self.curr_line += 1 # zu neuer zeile gehen
                    elif event.key == pygame.K_UP: # pfeiltaste nach oben
                        if self.curr_line != 0: # falls nicht in zeile null
                            self.curr_line -= 1 # eine zeile nach oben gehen
                    elif event.key == pygame.K_DOWN: # pfeiltaste nach unten
                        # falls zeile nicht die letzte und nicht die einzige
                        if self.curr_line < len(self.lines[self.lines_shown[0]:self.lines_shown[1]]) and len(self.lines[self.lines_shown[0]:self.lines_shown[1]]) != 1:
                            self.curr_line += 1 # eine zeile nach unten gehen
                    else: # fuer jede andere taste
                        curr_char = event.unicode # taste zu unicode konvertieren und als curr_char speichern
                        self.lines[self.curr_line] += curr_char # gedrueckte taste zu zeile hinzufuegen
                    if self.curr_line >= self.lines_shown[1]: # falls momentane zeile ausserhalb der angezeigten
                        self.lines_shown[0] += 1 # angezeigte zeilen anpassen
                        self.lines_shown[1] += 1
                    if 0 != self.curr_line <= self.lines_shown[0]:
                        self.lines_shown[0] -= 1 # angezeigte zeilen anpassen
                        self.lines_shown[1] -= 1
        else: # falls das save menue geoeffnet ist
            for event in events: 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: # falls backspace
                        self.current_file = self.current_file[0:-1] # dateinamen um 1 verkuerzen
                    elif event.key == pygame.K_RETURN: # falls enter
                        text = "" # variable fuer text
                        for i in self.lines: # alle zeilen + \n in text hinzufuegen
                            text += i + "\n"
                        with open(self.current_folder + self.current_file, "w") as f: # in datei schreiben
                            f.write(text)
                        self.save_file = False # save menue schliessen
                    else: # fuer alle anderen tasten
                        curr_char = event.unicode # taste zu unicode konvertieren
                        self.current_file += curr_char # gedrueckte taste zu dateinamen hinzufuegen
                    
    def draw(self):
        # hintergrund
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        
        if len(self.lines) != 0: # falls zeilen vorhanden 
            txt_render = [] # liste fuer text render objekte
            for i in range(len(self.lines)): # durch zeilen iterieren
                txt = f"{self.lines_shown[0] + i}: " + self.lines[i] # zeilenzahl + text
                if i == self.curr_line: # falls die zeile die momentan editierte ist
                    txt += "_" # "cursor" ans ende hinzufuegen
                txt_render.append(self.font.render(txt, 1, WHITE)) # text zur liste hinzufuegen
                
            txt_render = txt_render[self.lines_shown[0]:self.lines_shown[1] + 1] # text render liste an angezeigte zeilen anpassen
             
            for i in range(len(txt_render)): # durch liste iterieren und anzeigen
                self.screen.blit(txt_render[i], (15 * self.scale_horizontal, 160 * self.scale_vertical + 40 * i * self.scale_vertical))
                
                
        if not self.open_file: # falls das oeffnen menue geschlossen ist
            self.button_open.draw() # oeffnen button anzeigen
        elif self.open_file: # falls das oeffnen menue offen ist
            # hintergrund vom menue
            pygame.draw.rect(self.screen, WHITE, (0, 100 * self.scale_vertical, 400 * self.scale_horizontal, 60 * (len(self.open_buttons) + 1) * self.scale_vertical))
            for i in self.open_buttons: # durch buttons iterieren
                i.draw() # buttons anzeigen
        if not self.save_file and not self.open_file: # falls beide menues geschlossen sind
            self.button_save.draw() # speicher button anzeigen
        if self.save_file: # falls save menue offen ist
            # hintergrund vom menue
            pygame.draw.rect(self.screen, GREY, (205 * self.scale_horizontal, 100 * self.scale_vertical, 200 * self.scale_horizontal, 50 * self.scale_vertical))
            # eingabefeld fuer dateiname anzeigen mit momentanem namen und cursor
            self.screen.blit(self.font.render(self.current_file + "_", 1, WHITE), (205 * self.scale_horizontal, 105 * self.scale_vertical))
        
        self.button_exit.draw() # exit button anzeigen
        
    def click_check(self, event_pos):
        if not self.open_file: # falls oeffnen menue geschlossen ist
            if self.button_open.is_pressed(event_pos): # falls oeffnen button gedrueckt 
                self.open_file = True # oeffnen auf true setzen
                # dateinamen auslesen
                self.files = [i for i in os.listdir(self.current_folder) if os.path.isfile(self.current_folder + i)]
                self.open_buttons = [] # liste fuer knoepfe leeren
                for i in range(len(self.files)): # durch dateinamen iterieren
                    # fuer jede datei einen button hinzufuegen
                    self.open_buttons.append(button.Button(5 * self.scale_horizontal, 155 * self.scale_vertical + 55 * i * self.scale_vertical, 390 * self.scale_horizontal, 50 * self.scale_vertical, GREY, self.screen, self.files[i], self.font))
                # button fuer neue datei hinzufuegen
                self.open_buttons.append(button.Button(5 * self.scale_horizontal, 155 * self.scale_vertical + 55 * len(self.open_buttons) * self.scale_vertical, 390 * self.scale_horizontal, 50 * self.scale_vertical, BLACK, self.screen, "Neue Datei", self.font))
                # hitbox an groesse anpassen (anzahl knoepfe)
                self.open_file_hitbox = pygame.Rect(0, 100 * self.scale_vertical, 200 * self.scale_horizontal, 60 * (len(self.open_buttons) + 1) * self.scale_vertical)
        if not self.save_file and not self.open_file: # falls beide menues geschlossen sind
            if self.button_save.is_pressed(event_pos): # falls save button gedrueckt wird
                self.save_file = True # save auf true setzen
        
        else: # falls eins von den menues offen ist
            if not self.open_file_hitbox.collidepoint(event_pos): # falls man ausserhalb des oeffnen menues klickt
                self.open_file = False # oeffnen menue schliessen
                
            if not self.save_file_hitbox.collidepoint(event_pos): # falls man ausserhalb des save menues klickt
                self.save_file = False # save menue schliessen
                
            if self.open_file: # falls oeffnen menue offen ist
                for i in self.open_buttons[0:-1]: # durch buttons iterieren (ohne neue datei)
                    if i.is_pressed(event_pos): # falls button gedrueckt
                        self.current_file =  i.text # momentane datei = name von knopf, also dateiname
                        with open(self.current_folder + self.current_file, "r") as f: # daten aus datei auslesen
                            data = f.read()
                        self.lines = data.split("\n") # zeilen in liste speichern
                        # menge die zu zeichnen ist anpassen 
                        amount_to_draw = round((970 * self.scale_vertical) / (40 * self.scale_vertical)) - 1
                        # angezeigte zeilen anpassen
                        self.lines_shown[0] = 0
                        self.lines_shown[1] = amount_to_draw
                if self.open_buttons[-1].is_pressed(event_pos): # falls "neue datei" button gedrueckt ist
                    self.lines = [""] # zeilen leeren
                    # menge die zu zeichnen ist anpassen
                    amount_to_draw = round((970 * self.scale_vertical) / (40 * self.scale_vertical)) - 1
                    # angezeigte zeilen anpassen
                    self.lines_shown[0] = 0
                    self.lines_shown[1] = amount_to_draw
                    self.current_file = "" # momentane datei auf keine setzen
                    
                    
        if self.button_exit.is_pressed(event_pos): # falls exit knopf gedrueckt wird
            self.current_file = "" # alles zuruecksetzen / schliessen
            self.curr_line = 0
            self.lines = []
            self.save_file = False
            self.open_file = False
            return "exit" # auf den desktop zurueckkehren
            