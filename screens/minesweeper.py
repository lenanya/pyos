import pygame
from utils import button 
from random import randint 

# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)
YELLOW = (255, 255, 0)

class Minesweeper():
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        # exit button erstellen
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * scale_vertical, 50 * scale_horizontal, 50 * scale_vertical, RED, screen, "X", self.font)
        self.playfield = [] # spielfeld erstellen
        self.mines = [] # liste von minen positionen erstellen
        self.adjacencies = [] # spielfeld aber mit zahlen wie viele minen vorhanden sind
        self.list_of_mines = [] # liste von minen
        self.list_of_clears = [] # liste von feldern ohne minen
        self.game_over = True # ob spiel aktiv ist
        # start knopf erstellen
        self.start_game_button = button.Button(640 * self.scale_horizontal, 390 * self.scale_vertical, 640 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, screen, "Start new game", self.font)
        self.mines_left = 0 # variable von uebrigen minen
        self.mines_left_text = str(self.mines_left) # text von uebrigen minen
        # text render von uebrigen minen
        self.mines_left_text_render = self.font.render(self.mines_left_text, 1, WHITE) 


    def start_new_game(self):
        # alles auf null setzen
        self.mines_left = 0
        self.mines_left_text = self.mines_left # text aktualisieren
        self.playfield = [] # spielfeld leeren
        for x in range(9):
            self.playfield.append([])
            for y in range(9):
                self.playfield[x].append("O") # erstmal matrix von 10x10 mit nur freien feldern erstellen
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                # O O O O O O O O O O
                
                
        self.mines = [] # minen leeren
        for i in range(20):
            self.mines.append([randint(0, 8), randint(0, 8)]) # zwanzig zufaellige koordinaten erstellen
            # bsp [[3, 5], [6, 4], [9, 3],...,usw]
        for i in self.mines:
            self.playfield[i[0]][i[1]] = "X" # felder in spielfeld zu minen einstellen
            self.mines_left += 1 # pro mine uebrige minen variable erhoehen
            
            # feld ist jetzt so:
            # O O O O X O O O O X
            # O X O O O O X O O O
            # O O O X O O O X O O
            # O X O O O O O O X O
            # O O X O O X O O O O
            # O O X O O O O O O O
            # O O O O X O X X X O
            # O X X O O O O O O O
            # O O O X O O O O O O
            # O O O O X O O X O O

        self.adjacencies = self.playfield # erstmal fuellen
        # jetzt kommt der komplizierte part, den man bestimmt auch haette
        # besser machen koennen, aber was dieser gigantische for/if turm macht,
        # ist fuer jedes feld zu alle benachbarten felder zu ueberpruefen und falls eine mine
        # vorhanden ist, seinen zaehler zu erhoehen
        # 
        # so hat am ende jedes feld eine zahl der benachbarten minen als text
        for x in range(9): # durch alle koordinaten durchiterieren
            for y in range(9):
                mines_adjacent = 0
                if self.playfield[y][x] == "X":
                    mines_adjacent = self.adjacencies[y][x] = "X"
                else:
                    if 8 > y > 0: # dieses ganze kram ist, weil ja nicht alle felder 8 nachbarn
                                  # haben und daher ueberprueft werden muss ob das feld
                                  # am rand liegt
                        if 8 > x > 0:
                            for i in range(-1, 2): # durch benachbarte felder iterieren
                                for e in range(-1, 2):
                                    if self.playfield[y + i][x + e] == "X": # falls feld eine mine ist
                                        if e == 0 and i == 0: # und nicht das eigene feld ist
                                            pass
                                        else:
                                            mines_adjacent += 1 # minen zaehler um 1 erhoehen
                                            
                        # dasselbe, nur fuer eine andere art von feld, wiederhole bis ende for/if turm
                        if x == 0:
                            for i in range(-1, 2):
                                for e in range(0, 2):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                        if x == 8:
                            for i in range(-1, 2):
                                for e in range(-1, 1):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                    if y == 0:
                        if 8 > x > 0:
                            for i in range(0, 2):
                                for e in range(-1, 2):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                        if x == 0:
                            for i in range(0, 2):
                                for e in range(0, 2):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                        if x == 8:
                            for i in range(0, 2):
                                for e in range(-1, 1):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                                        
                    if y == 8:
                        if 8 > x > 0:
                            for i in range(-1, 1):
                                for e in range(-1, 2):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                        if x == 0:
                            for i in range(-1, 1):
                                for e in range(0, 2):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                        if x == 8:
                            for i in range(-1, 1):
                                for e in range(-1, 1):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
                                         
                self.adjacencies[y][x] = mines_adjacent # letztendlich jedes feld mit seiner
                                                        # zahl an benachbarten minen aktualisieren
        
        self.list_of_mines = [] # listen der buttons leeren
        self.list_of_clears = []
        self.mines_left_text = str(self.mines_left) # text aktualisieren
        for y in range(1, 10): # 10x10 matrix von knoepfen erstellen, fuer jedes feld
            for x in range(1, 10):
                if self.adjacencies[y-1][x-1] == "X": # falls mine, minenknopf
                    self.list_of_mines.append(button.Button(435 * self.scale_horizontal + 105 * x * self.scale_horizontal, 105 * y * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, WHITE, self.screen, "X", self.font))
                else: # falls frei, freier knopf
                    self.list_of_clears.append(button.Button(435 * self.scale_horizontal + 105 * x * self.scale_horizontal, 105 * y * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, WHITE, self.screen, str(self.adjacencies[y-1][x-1]), self.font))

    def run(self, mouse_position, events):
        if self.game_over: # falls spiel nicht aktiv
            if self.start_game_button.is_hover(mouse_position): # start button hover 
                self.start_game_button.color = TEAL
            else:
                self.start_game_button.color = BLUE
            
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_game_button.is_pressed(event.pos): # falls start knopf gedrueckt
                        self.game_over = False # spiel auf aktiv setzen
                        self.start_new_game() # neues spiel starten
                        
        else: # falls spiel aktiv
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # falls linksklick
                    for i in self.list_of_clears: # fuer jeden knopf ueberpruefen ob er gedrueckt wurde
                        if i.is_pressed(event.pos): # falls feld frei farbe wechseln, zahl anzeigen
                            i.color = TEAL
                            i.text_color = WHITE
                    for i in self.list_of_mines: #
                        if i.is_pressed(event.pos): # falls feld mine, game over, spiel auf inaktiv setzen
                            self.game_over = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # falls rechtsklick
                    for i in self.list_of_clears:
                        if i.is_pressed(event.pos): # fuer jeden knopf ueberpruefen ob er gedrueckt wurde
                            if i.color != TEAL and i.color != RED: # falls ungeklickt, farbe auf rot setzen
                                i.color = RED                      # und anzahl des uebrige minen texts
                                i.text_color = RED                 # verringern
                                self.mines_left -= 1
                                self.mines_left_text = str(self.mines_left)
                            elif i.color == RED: # falls bereits markiert, demarkieren, 
                                i.color = WHITE  # und text wieder erhoehen
                                i.text_color = WHITE
                                self.mines_left += 1
                                self.mines_left_text = str(self.mines_left)
                    for i in self.list_of_mines: # fuer minen dasselbe
                        if i.is_pressed(event.pos):
                            if i.color != RED:
                                i.color = RED
                                i.text_color = RED
                                self.mines_left -= 1
                                self.mines_left_text = str(self.mines_left)
                            else:
                                i.color = WHITE
                                i.text_color = WHITE
                                self.mines_left += 1
                                self.mines_left_text = str(self.mines_left)
            
    
    def draw(self):
        # hintergrund anzeigen
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        if not self.game_over: # falls spiel aktiv
            # text anzeigen
            self.mines_left_text_render = self.font.render(f"Minen: {self.mines_left_text}", 1, WHITE)
            self.screen.blit(self.mines_left_text_render, (10 * self.scale_horizontal, 200 * self.scale_vertical))
            # lokale variable fuer gefundene minen
            mines_cleared = 0
            for i in self.list_of_clears: # alle freien felder anzeigen
                i.draw()
            for i in self.list_of_mines: # alle minen anzeigen 
                i.draw()
                if i.color == RED: # falls feldfarbe = rot, also markiert:
                    mines_cleared += 1 # variable erhoehen

            if mines_cleared == 20: # falls alle 20 minen markiert:
                self.game_over = True # spiel neustarten
                
        else: # falls spiel inaktiv
            self.start_game_button.draw() # start button anzeigen
            
        self.button_exit.draw() # und schliesslich, immer, exit button anzeigen
        
			
    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos): # falls exit knopf gedrueckt, auf desktop gehen
            self.game_over = True # und spiel zuruecksetzen
            return "exit"
        

# TODO: ADD DIFFICULTY 
# TODO: add start screen 
# TODO: add game over screen