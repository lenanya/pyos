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

class Player():
	def __init__(self, y, size_horizontal, size_vertical, screen, scale_horizontal, scale_vertical):
		self.y = y
		self.size_horizontal = size_horizontal
		self.size_vertical = size_vertical
		self.screen = screen
		self.scale_horizontal = scale_horizontal
		self.scale_vertical = scale_vertical
		self.velocity = 5 * self.scale_vertical
		self.speed = 0
		
	def draw(self):
		pygame.draw.rect(self.screen, YELLOW, (200 * self.scale_horizontal, self.y, self.size_horizontal, self.size_vertical))
		
	def jump(self):
		self.speed -= 75 * self.scale_vertical
		
	def move(self):
		self.y += self.speed
		if self.speed <= 20 * self.scale_vertical:
			self.speed += self.velocity
		if self.y >= 1080 * self.scale_vertical or self.y <= 150 * self.scale_vertical:
			return True

class Pipe():
	def __init__(self, x, gap_y, gap_size, screen, scale_horizontal, scale_vertical):
		self.x = x
		self.gap_y = gap_y
		self.gap_size = gap_size
		self.screen = screen
		self.scale_horizontal = scale_horizontal
		self.scale_vertical = scale_vertical
		
	def draw(self):
		pygame.draw.rect(self.screen, GREEN, (self.x, 150 * self.scale_vertical, 150 * self.scale_horizontal, self.gap_y - 150 * self.scale_vertical))
		pygame.draw.rect(self.screen, GREEN, (self.x, self.gap_y + self.gap_size, 150 * self.scale_horizontal, 10000))
		
	def move(self):
		self.x -= 10 * self.scale_horizontal
		if self.x + 150 * self.scale_horizontal <= 0:
			self.x = 1920 * self.scale_horizontal
			self.gap_y = randint(round(250 * self.scale_vertical), round(500 * self.scale_vertical))
			return True 
		return False
		
	def check_collision(self, player_y):
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
        self.player = Player(490 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, self.screen, self.scale_horizontal, self.scale_vertical)
        self.pipe = Pipe(1920 * self.scale_horizontal, 300 * self.scale_vertical, 400 * self.scale_vertical, self.screen, self.scale_horizontal, self.scale_vertical)
        self.game_over = True
        self.button_exit = button.Button((1920 - 55) * scale_horizontal, 100 * scale_vertical, 50 * scale_horizontal, 50 * scale_vertical, RED, screen, "X", self.font)
        self.player_score = 0
        
    def run(self, mouse_position, events):
           for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_position[1] > 150 * self.scale_vertical:
                        if not self.game_over:
                            self.player.jump()
                        else:
                            self.game_over = False
							
           if not self.game_over: 
               if self.player.move():
                   self.game_over = True
                   self.player.y = 490 * self.scale_vertical
                   self.player.speed = 0
                   self.pipe.x = 1920 * self.scale_horizontal
                   self.pipe.gap_y  = 300 * self.scale_vertical
                   
               if self.pipe.move():
                   self.player_score += 1
               
               if self.pipe.check_collision(self.player.y):
                   self.game_over = True
                   self.player.y = 490 * self.scale_vertical
                   self.player.speed = 0
                   self.pipe.x = 1920 * self.scale_horizontal
                   self.pipe.gap_y  = 300 * self.scale_vertical
                   
    
    def draw(self):
        pygame.draw.rect(self.screen, WHITE, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 50 * self.scale_vertical))
        pygame.draw.rect(self.screen, BLACK, (0, 150 * self.scale_vertical, 1920 * self.scale_horizontal, 1000 * self.scale_vertical))
        self.button_exit.draw()
        if not self.game_over:
            self.screen.blit(self.font.render(f"Score: {self.player_score}", 1, WHITE), (50 * self.scale_horizontal, 200 * self.scale_horizontal))
            self.player.draw()
            self.pipe.draw()
            return 0
        else:
            self.player_score = 0
            pygame.draw.rect(self.screen, YELLOW, (200 * self.scale_horizontal, 415 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical))
            self.screen.blit(self.font.render("Anklicken zum Starten", 1, WHITE), (800 * self.scale_horizontal, 450 * self.scale_vertical))
        
			
    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos):
            self.game_over = True
            return "exit"
        

# TODO: ADD SCORE
# TODO: ADD SPRITES (AAAAAAAAA)
# TODO: ADD ANIMATION 
# TODO: ADD SCALING DIFFICULTY (SPEED)