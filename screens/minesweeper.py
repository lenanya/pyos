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
        self.button_exit = button.Button((1920 - 55) * scale_horizontal, 100 * scale_vertical, 50 * scale_horizontal, 50 * scale_vertical, RED, screen, "X", self.font)
        self.playfield = []
        self.mines = []
        self.adjacencies = []
        self.list_of_mines = []
        self.list_of_clears = []
        self.game_over = True
        self.start_game_button = button.Button(640 * self.scale_horizontal, 390 * self.scale_vertical, 640 * self.scale_horizontal, 100 * self.scale_vertical, BLUE, screen, "Start new game", self.font)
        self.mines_left = 0
        self.mines_left_text = str(self.mines_left)
        self.mines_left_text_render = self.font.render(self.mines_left_text, 1, WHITE)


    def start_new_game(self):
        self.mines_left = 0
        self.mines_left_text = self.mines_left
        self.playfield = []
        for x in range(9):
            self.playfield.append([])
            for y in range(9):
                self.playfield[x].append("O")
                
        self.mines = []
        for i in range(20):
            self.mines.append([randint(0, 8), randint(0, 8)])
        for i in self.mines:
            self.playfield[i[0]][i[1]] = "X"
            self.mines_left += 1

        self.adjacencies = self.playfield
        for x in range(9):
            for y in range(9):
                mines_adjacent = 0
                if self.playfield[y][x] == "X":
                    mines_adjacent = self.adjacencies[y][x] = "X"
                else:
                    if 8 > y > 0:
                        if 8 > x > 0:
                            for i in range(-1, 2):
                                for e in range(-1, 2):
                                    if self.playfield[y + i][x + e] == "X":
                                        if e == 0 and i == 0:
                                            pass
                                        else:
                                            mines_adjacent += 1
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
                                        
                self.adjacencies[y][x] = mines_adjacent
        
        self.list_of_mines = []
        self.list_of_clears = []
        self.mines_left_text = str(self.mines_left)
        for y in range(1, 10):
            for x in range(1, 10):
                if self.adjacencies[y-1][x-1] == "X":
                    self.list_of_mines.append(button.Button(435 * self.scale_horizontal + 105 * x * self.scale_horizontal, 105 * y * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, WHITE, self.screen, "X", self.font))
                else:
                    self.list_of_clears.append(button.Button(435 * self.scale_horizontal + 105 * x * self.scale_horizontal, 105 * y * self.scale_vertical, 100 * self.scale_horizontal, 100 * self.scale_vertical, WHITE, self.screen, str(self.adjacencies[y-1][x-1]), self.font))

    def run(self, mouse_position, events):
        if self.game_over:
            if self.start_game_button.is_hover(mouse_position):
                self.start_game_button.color = TEAL
            else:
                self.start_game_button.color = BLUE
            
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_game_button.is_pressed(event.pos):
                        self.game_over = False
                        self.start_new_game()
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in self.list_of_clears:
                        if i.is_pressed(event.pos):
                            i.color = TEAL
                            i.text_color = WHITE
                    for i in self.list_of_mines:
                        if i.is_pressed(event.pos):
                            self.game_over = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    for i in self.list_of_clears:
                        if i.is_pressed(event.pos):
                            if i.color != TEAL and i.color != RED:
                                i.color = RED
                                i.text_color = RED
                                self.mines_left -= 1
                                self.mines_left_text = str(self.mines_left)
                            elif i.color == RED:
                                i.color = WHITE
                                i.text_color = WHITE
                                self.mines_left += 1
                                self.mines_left_text = str(self.mines_left)
                    for i in self.list_of_mines:
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
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        if not self.game_over:
            self.mines_left_text_render = self.font.render(f"Minen: {self.mines_left_text}", 1, WHITE)
            self.screen.blit(self.mines_left_text_render, (10 * self.scale_horizontal, 200 * self.scale_vertical))
            mines_cleared = 0
            for i in self.list_of_clears:
                i.draw()
            for i in self.list_of_mines:
                i.draw()
                if i.color == RED:
                    mines_cleared += 1

            if mines_cleared == 20:
                self.game_over = True
                
        else:
            self.start_game_button.draw()
        self.button_exit.draw()
        
			
    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos):
            self.game_over = True
            return "exit"
        

# TODO: ADD MINE COUNTER 
# TODO: ADD FLAG SPRITE
# TODO: FIX TEXT ALIGNMENT (BUTTONS!!!)
# TODO: ADD DIFFICULTY 
# TODO: ADD TIMER
# TODO: ?ADD AUTO UNVEILING
# TODO: ADD WIN CONDITION (OOPS)
