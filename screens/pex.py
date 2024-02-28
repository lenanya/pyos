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

class Pex:
    def __init__(self, file):
        with open(f"./usr/files/{file}", "r") as f:
            data = f.read()
        self.lines = data.split("\n")
        self.terms = []
        for i in self.lines:
            if i == "\n":
                i = ""
        for i in self.lines:
            self.terms.append(i.split(" "))
        self.ptr = 0
        self.variables = {}
        self.functions = {}
        self.return_point = 0
            
    def pex_run(self, mouse_position, events):
        current = self.terms[self.ptr]
        print(current)
        
        if current[0] == "num":
            self.variables[current[1]] = float(current[3])
            self.ptr += 1
        elif current[0] == "str":
            self.variables[current[1]] = current[3]
            self.ptr += 1
        elif current[0] == "fn":
            self.functions[current[1]] = [self.ptr + 1, 0]
            self.ptr += 1
        elif current[0] == "if":
            comp_var1 = current[1]
            comp_var2 = current[3]
            
            if comp_var1 in self.variables:
                comp_var1 = self.variables[comp_var1]
            if comp_var2 in self.variables:
                comp_var2 = self.variables[comp_var2]
                
            if type(comp_var1) == int or float:
                comp_var1 = float(comp_var1)
            if type(comp_var2) == int or float:
                comp_var2 = float(comp_var2)
                
            if current[2] == "==":
                if comp_var1 == comp_var2:
                    self.ptr += 1
                else:
                    while self.terms[self.ptr][0] != "}":
                        self.ptr += 1
                    self.ptr += 1
                    
            elif current[2] == "!=":
                if comp_var1 != comp_var2:
                    self.ptr += 1
                else:
                    while self.terms[self.ptr][0] != "}":
                        self.ptr += 1
                    self.ptr += 1
                    
        elif current[0] == "print":
            if current[1] in self.variables:
                self.ptr += 1
                return f"echo {str(self.variables[current[1]])}"
            else:
                self.ptr += 1
                return f"echo {self.lines[self.ptr - 1][6::]}"
            
        elif current[0] in self.variables:
            sec_val = ""
            if current[2] in self.variables:
                sec_val = self.variables[current[2]]
            else:
                sec_val = current[2]
            if type(sec_val) == int or float:
                sec_val = float(sec_val)

            if current[1] == "=":
                self.variables[current[0]] = sec_val
            elif current[1] == "+=":
                self.variables[current[0]] += sec_val
            elif current[1] == "-=":
                self.variables[current[0]] -= sec_val
            self.ptr += 1
            
        elif current[0] == "while":
            self.return_point = self.ptr
            comp_var1 = current[1]
            comp_var2 = current[3]
            
            if comp_var1 in self.variables:
                comp_var1 = self.variables[comp_var1]
            if comp_var2 in self.variables:
                comp_var2 = self.variables[comp_var2]
                
            if type(comp_var1) == int or float:
                comp_var1 = float(comp_var1)
            if type(comp_var2) == int or float:
                comp_var2 = float(comp_var2)
                
            if current[2] == "==":
                if comp_var1 == comp_var2:
                    self.ptr += 1
                else:
                    while self.terms[self.ptr][0] != "]":
                        self.ptr += 1
                    self.ptr += 1
                    
            elif current[2] == "!=":
                if comp_var1 != comp_var2:
                    self.ptr += 1
                else:
                    while self.terms[self.ptr][0] != "]":
                        self.ptr += 1
                    self.ptr += 1
                    
        elif current[0] == "]":
            self.ptr = self.return_point
            
        else:
            self.ptr += 1
            
        if self.ptr < len(self.lines):
            return ""
        else:
            return "pexexit"
        
    # TODO: ADD MORE KEYWORDS
    # TODO: ????GRAPHICAL MODE