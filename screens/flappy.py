import pygame
from random import randint
from utils import button

# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)
YELLOW = (255, 255, 0)

# spieler class erstellen
class Player():
	def __init__(self, y, size_horizontal, size_vertical, screen, scale_horizontal, scale_vertical):
		self.y = y
		self.size_horizontal = size_horizontal
		self.size_vertical = size_vertical
		self.screen = screen
		self.scale_horizontal = scale_horizontal
		self.scale_vertical = scale_vertical
		self.speed = 0 # variable fuer geschwindigkeit
		self.velocity = 5 * self.scale_vertical # variable fuer beschleunigung
		
	def draw(self):
        # spieler anzeigen
		pygame.draw.rect(self.screen, YELLOW, (200 * self.scale_horizontal, self.y, self.size_horizontal, self.size_vertical))
		
	def jump(self):
        # springen indem geschwindigkeit um 75 verringert wird
		self.speed -= 75 * self.scale_vertical
		
	def move(self):
		self.y += self.speed # spielerhoehe wird um geschwindigkeit erhoeht / vertieft
		if self.speed <= 20 * self.scale_vertical: # falls noch nicht terminalgeschwindigkeit
			self.speed += self.velocity # geschwindigkeit um beschleunigung erhoehen
		if self.y >= 1080 * self.scale_vertical or self.y <= 150 * self.scale_vertical:
			return True # falls bildschirmrand beruehrt, game over

# class fuer die roehren
class Pipe():
	def __init__(self, x, gap_y, gap_size, screen, scale_horizontal, scale_vertical):
		self.x = x
		self.gap_y = gap_y
		self.gap_size = gap_size
		self.screen = screen
		self.scale_horizontal = scale_horizontal
		self.scale_vertical = scale_vertical
		
	def draw(self):
        # roehren anzeigen
		pygame.draw.rect(self.screen, GREEN, (self.x, 150 * self.scale_vertical, 150 * self.scale_horizontal, self.gap_y - 150 * self.scale_vertical))
		pygame.draw.rect(self.screen, GREEN, (self.x, self.gap_y + self.gap_size, 150 * self.scale_horizontal, 10000))
		
	def move(self):
		self.x -= 10 * self.scale_horizontal # roehren nach links bewegen
        # wenn roehren vom bildschirm weg sind, position zuruecksetzen
        # und luecke zufaellig neu generieren
		if self.x + 150 * self.scale_horizontal <= 0:
			self.x = 1920 * self.scale_horizontal
			self.gap_y = randint(round(250 * self.scale_vertical), round(500 * self.scale_vertical))
			return True # um score vom player zu erhoehen
		return False
		
	def check_collision(self, player_y):
        # ueberprueft ob spieler mit roehren kollidiert
		if self.x <= 250 * self.scale_horizontal and self.x + 150 * self.scale_horizontal >= 200 * self.scale_horizontal:
			if not self.gap_y < player_y or not self.gap_y + self.gap_size > player_y + 50 * self.scale_vertical:
				return True
		return False


class FlappyBird():
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        # spieler und roehren objekte erstellen
        self.player = Player(490 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, self.screen, self.scale_horizontal, self.scale_vertical)
        self.pipe = Pipe(1920 * self.scale_horizontal, 300 * self.scale_vertical, 400 * self.scale_vertical, self.screen, self.scale_horizontal, self.scale_vertical)
        self.game_over = True
        # exit button erstellen
        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * scale_vertical, 50 * scale_horizontal, 50 * scale_vertical, RED, screen, "X", self.font)
        # variable fuer score erstellen
        self.player_score = 0
        
    def run(self, mouse_position, events):
           for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_position[1] > 150 * self.scale_vertical:
                        if not self.game_over: # falls spiel aktiv player springen lassen
                            self.player.jump()
                        else:
                            self.game_over = False # sonst spiel starten
							
           if not self.game_over: # falls spiel aktiv
               if self.player.move(): # falls spieler bildschirm rand beruehrt hat
                   # alles zuruecksetzen
                   self.game_over = True
                   self.player.y = 490 * self.scale_vertical
                   self.player.speed = 0
                   self.pipe.x = 1920 * self.scale_horizontal
                   self.pipe.gap_y  = 300 * self.scale_vertical
                   
               if self.pipe.move(): # falls roehren am spieler vorbei sind
                   self.player_score += 1 # score erhoehen
               
               if self.pipe.check_collision(self.player.y): # falls spieler roehren beruehrt
                   # alles zuruecksetzen
                   self.game_over = True
                   self.player.y = 490 * self.scale_vertical
                   self.player.speed = 0
                   self.pipe.x = 1920 * self.scale_horizontal
                   self.pipe.gap_y  = 300 * self.scale_vertical
                   
    
    def draw(self):
        # hintergrund anzeigen
        pygame.draw.rect(self.screen, BLACK, (0, 150 * self.scale_vertical, 1920 * self.scale_horizontal, 1000 * self.scale_vertical))
        self.button_exit.draw() # exit button anzeigen
        if not self.game_over: # falls spiel aktiv
            # score text anzeigen
            self.screen.blit(self.font.render(f"Score: {self.player_score}", 1, WHITE), (50 * self.scale_horizontal, 200 * self.scale_horizontal))
            self.player.draw() # spieler und roehren anzeigen
            self.pipe.draw()
        else: # falls spiel nicht aktiv
            self.player_score = 0 # score zuruecksetzen
            # statischen spieler anzeigen
            pygame.draw.rect(self.screen, YELLOW, (200 * self.scale_horizontal, 415 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical))
            # start text anzeigen
            self.screen.blit(self.font.render("Anklicken zum Starten", 1, WHITE), (800 * self.scale_horizontal, 450 * self.scale_vertical))
        
			
    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos):
            # falls exit knopf gedrueckt wird
            # spiel zuruecksetzen und schliessen
            self.game_over = True 
            return "exit"
        

# TODO: ADD SCORE
# TODO: ADD SPRITES (AAAAAAAAA)
# TODO: ADD ANIMATION 
# TODO: ADD SCALING DIFFICULTY (SPEED)
