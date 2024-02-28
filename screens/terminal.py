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

class Terminal:
    def __init__(self, scale_horizontal, scale_vertical, screen, font):
        self.scale_horizontal = scale_horizontal
        self.scale_vertical = scale_vertical
        self.screen = screen
        self.font = font
        
        self.current_folder = "./usr/files"
        self.lines = ["./usr/files: "]
        self.curr_line = 0
        self.usr_input = ""

        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)

    def eval_cmd(self, cmd):
        terms_cmd = cmd.split(" ")
        if terms_cmd[0] == "echo":
            self.lines[self.curr_line + 1] = cmd[4::]
            self.curr_line += 1
        elif terms_cmd[0] == "cd":
            if len(terms_cmd) > 1:
                self.current_folder = self.current_folder + "/" + terms_cmd[1]
            else: 
                self.current_folder = "./usr/files"
        
    def run(self, mouse_position, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.lines.append("")
                if event.key == pygame.K_BACKSPACE:
                    self.usr_input = self.usr_input[0:-1]
                elif event.key == pygame.K_RETURN:
                    self.eval_cmd(self.usr_input)
                    self.usr_input = ""
                    self.curr_line += 1
                else:
                    curr_char = event.unicode
                    self.usr_input += curr_char
                self.lines[self.curr_line] = f"{self.current_folder}: {self.usr_input}"

    def draw(self):
        pygame.draw.rect(self.screen, BLACK, (0, 100 * self.scale_vertical, 1920 * self.scale_horizontal, 980 * self.scale_vertical))
        txt = ""
        txt_render = []
        for i in self.lines:
            txt = i
            txt_render.append(self.font.render(txt, 1, WHITE))
        for i in range(len(txt_render)):
            self.screen.blit(txt_render[i], (10 * self.scale_horizontal, 110 * self.scale_vertical + 40 * i * self.scale_vertical))
        
        self.button_exit.draw()


    def click_check(self, event_pos):
        if self.button_exit.is_pressed(event_pos):
            return "exit"
