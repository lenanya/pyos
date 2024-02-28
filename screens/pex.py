# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)

# interpreter fuer pex (pyos executable), die eigene programmiersprache die mit pyOS enthalten ist

class Pex:
    def __init__(self, file):
        # code aus datei auslesen und formatieren
        with open(f"./usr/files/{file}", "r") as f:
            data = f.read() 
        self.lines = data.split("\n")
        self.terms = []
        for i in self.lines:
            if i == "\n":
                i = ""
        for i in self.lines:
            self.terms.append(i.split(" "))
        # pointer und variablen sowie funktionen dict erstellen
        self.ptr = 0
        self.variables = {}
        self.functions = {}
        self.return_point = 0
            
    def pex_run(self, mouse_position, events):
        current = self.terms[self.ptr] # momentane zeile
        
        if current[0] == "num": # pex ist static type also muss man den variablen typ angeben, num = float
            self.variables[current[1]] = float(current[3]) # wert in dict eingeben
            self.ptr += 1 # zeilenpointer erhoehen
        elif current[0] == "str": # str = string
            self.variables[current[1]] = current[3] 
            self.ptr += 1 
        elif current[0] == "fn": # fn = funktion
            self.functions[current[1]] = [self.ptr + 1, 0] # startpunkt speichen, zweiter wert in der liste 
                                                           # ist um am ende der funktion zurueck zu kommen
            self.ptr += 1
        elif current[0] == "if": # if 
            comp_var1 = current[1] # werte die verglichen werden sollen speichern
            comp_var2 = current[3]
            
            if comp_var1 in self.variables: # ueberpruefen ob es variablen sind
                comp_var1 = self.variables[comp_var1]
            if comp_var2 in self.variables:
                comp_var2 = self.variables[comp_var2]
                
            if type(comp_var1) == int or float: # falls zahl zu float convertieren
                comp_var1 = float(comp_var1)
            if type(comp_var2) == int or float:
                comp_var2 = float(comp_var2)
                
            if current[2] == "==": # operatoren ueberpruefen und condition
                if comp_var1 == comp_var2: # falls True => nichts
                    self.ptr += 1
                else: # falls False => zu ende von if springen
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
                    
        elif current[0] == "print": # ausgabe im terminal
            if current[1] in self.variables:
                self.ptr += 1
                return f"echo {str(self.variables[current[1]])}"
            else:
                self.ptr += 1
                return f"echo {self.lines[self.ptr - 1][6::]}"
            
        elif current[0] in self.variables: # variablen redefinieren / mathe operationen
            sec_val = ""
            if current[2] in self.variables:
                sec_val = self.variables[current[2]] 
            else:
                sec_val = current[2] # variable 
            if type(sec_val) == int or float:
                sec_val = float(sec_val)

            if current[1] == "=":
                self.variables[current[0]] = sec_val # variable1 = variable2 (oder wert)
            elif current[1] == "+=":
                self.variables[current[0]] += sec_val # variable1 = variable1 + variable2 (oder wert)
            elif current[1] == "-=":
                self.variables[current[0]] -= sec_val # variable1 = variable1 - variable2 (oder wert)
            self.ptr += 1
            
        elif current[0] == "while": # while schleife
            self.return_point = self.ptr # return punkt erstellen
            comp_var1 = current[1] # werte anlegen
            comp_var2 = current[3]
            
            if comp_var1 in self.variables: # ueberpruefen ob werte variablen sind
                comp_var1 = self.variables[comp_var1] 
            if comp_var2 in self.variables:
                comp_var2 = self.variables[comp_var2]
                
            if type(comp_var1) == int or float: # falls zahl zu float konvertieren
                comp_var1 = float(comp_var1)
            if type(comp_var2) == int or float:
                comp_var2 = float(comp_var2)
                
            if current[2] == "==": # operation fuer die kondition ueberpruefen
                if comp_var1 == comp_var2:
                    self.ptr += 1 # falls True: => nichts
                else:
                    while self.terms[self.ptr][0] != "]":
                        self.ptr += 1 # falls False: => ans ende von schleife springen
                    self.ptr += 1
                    
            elif current[2] == "!=":
                if comp_var1 != comp_var2:
                    self.ptr += 1
                else:
                    while self.terms[self.ptr][0] != "]":
                        self.ptr += 1
                    self.ptr += 1
                    
        elif current[0] == "]": # ende von while schleife, springt zu schleifenbeginn
            self.ptr = self.return_point 
            
        else:
            self.ptr += 1 # wenn zeile kein befehl, ignorieren
            
        if self.ptr < len(self.lines): 
            return "" 
        else:
            return "pexexit" # wenn alle zeilen ausgefuehrt, schliessen
        
    # TODO: ADD MORE KEYWORDS
    # TODO: ????GRAPHICAL MODE
    # TODO: add function working (oops)
    # TODO: add other comperative ops
    # TODO: add more math ops
    # TODO: string concat?