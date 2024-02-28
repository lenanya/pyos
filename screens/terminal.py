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
        
        self.current_folder = "./usr/files"
        self.lines = ["./usr/files: "]
        self.curr_line = 0
        self.usr_input = ""
        
        self.pex_active = False

        self.button_exit = button.Button((1920 * self.scale_horizontal - 55 * self.scale_horizontal), 100 * self.scale_vertical, 50 * self.scale_horizontal, 50 * self.scale_vertical, RED, self.screen, "X", self.font)

    def eval_cmd(self, cmd):
        self.lines.append("")
        terms_cmd = cmd.split(" ")
        if terms_cmd[0] == "echo":
            self.lines[self.curr_line + 1] = cmd[4::]
            self.curr_line += 1
        elif terms_cmd[0] == "pex":
            if terms_cmd[1] in os.listdir(self.current_folder): # TODO: bugfix if no file
                self.pex = pex.Pex(terms_cmd[1])
                self.pex_active = True
        elif terms_cmd[0] == "pexexit":
            self.pex_active = False
            self.usr_input = ""
            self.curr_line += 1
            self.lines[self.curr_line] = f"{self.current_folder}: {self.usr_input}"
        elif terms_cmd[0] == "cls":
            self.lines = []
            self.curr_line = 0
            self.lines.append("")
            self.lines.append("")
            self.lines.append("")
        elif terms_cmd[0] == "marisetogaya":
            self.lines[self.curr_line + 1] = "ITADAKI! SEIEKI <3"
            with open("./settings/desktop_background.txt", "w") as f:
                f.write("./assets/dontask.png")
            self.curr_line += 1
        
    def run(self, mouse_position, events):
        if self.pex_active:
            pex_output = self.pex.pex_run(mouse_position, events)
            if pex_output != "":
                self.eval_cmd(pex_output)
        else:
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
        if self.button_exit.is_pressed(event_pos) :
            self.pex_active = False
            self.current_folder = "./usr/files"
            self.lines = ["./usr/files: "]
            self.curr_line = 0
            self.usr_input = ""
            return "exit"
        
    # TODO: ADD MORE CMDS
    # TODO: FIX EXIT CMD
    # TODO: ADD SCROLLING (OOPS)
    # TODO: comment bruh
    # TODO: tree cmd