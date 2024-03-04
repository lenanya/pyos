from random import randint

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
            self.terms.append(i.split(" "))
            
        # pointer und variablen sowie funktionen dict erstellen
        self.ptr = 0
        self.variables = {}
        self.functions = {}
        self.lists = {}
        self.return_point = []
            
    def pex_run(self, mouse_position, events):
        current = self.terms[self.ptr] # momentane zeile
        
        if current[0] == "num": # pex ist static type also muss man den variablen typ angeben, num = float
            assign_val = current[3]
            
            if assign_val in self.variables: # falls wert variable
                assign_val = self.variables[assign_val]
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # !!! Dieser teil kommt sehr oft vor, also kommentiere ich ihn nur hier einmal !!!
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            elif assign_val.endswith(")"): # falls wert aus liste
                name = assign_val[0:assign_val.find("(")] # name 
                index = assign_val[assign_val.find("(") + 1 : assign_val.find(")")] # index aus klammern holen
                if index in self.variables: # falls index variable ist
                    try: # falls variable zahl ist
                        index = int(self.variables[index]) # wert der variable als zahl in index speichern
                    except Exception: # falls variable keine zahl ist 
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})" # programm mit fehler beenden
                else: # falls index keine variable ist
                    try: # falls index zahl ist
                        index = int(index) # index zu zahl konvertieren
                    except Exception: # falls index keine zahl ist
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})" # programm mit fehler beenden
                assign_val = self.lists[name][index] # wert von liste an index in variable speichern
            
            try: # zu float konvertieren
                assign_val = float(assign_val)
            except Exception: # falls keine zahl
                return f"pexexit Nicht-Zahl als num deklariert (Zeile {self.ptr + 1})" # programm mit fehler beenden
            
            self.variables[current[1]] = assign_val # wert in dict eingeben
            self.ptr += 1 # zeilenpointer erhoehen
        elif current[0] == "str": # str = string
            self.variables[current[1]] = current[3] 
            self.ptr += 1 
        elif current[0] == "fn": # fn = funktion
            self.functions[current[1]] = [self.ptr + 1, 0] # startpunkt speichen, zweiter wert in der liste 
                                                           # ist um am ende der funktion zurueck zu kommen
            while self.terms[self.ptr][0] != "return":     # funktion beim einspeichern nicht ausfuehren
                self.ptr += 1
            self.ptr += 1
            
        elif current[0] == "if": # if 
            comp_var1 = current[1] # werte die verglichen werden sollen speichern
            comp_var2 = current[3]
            
            if comp_var1 in self.variables: # ueberpruefen ob es variablen sind
                comp_var1 = self.variables[comp_var1]
            elif str(comp_var1).endswith(")"):
                name = comp_var1[0:comp_var1.find("(")]
                index = comp_var1[comp_var1.find("(") + 1 : comp_var1.find(")")]
                if index in self.variables:
                    try:
                        index = int(self.variables[index])
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                else:
                    try:
                        index = int(index)
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                comp_var1 = self.lists[name][index]
            if comp_var2 in self.variables:
                comp_var2 = self.variables[comp_var2]
            elif str(comp_var1).endswith(")"):
                name = comp_var2[0:comp_var2.find("(")]
                index = comp_var2[comp_var2.find("(") + 1 : comp_var2.find(")")]
                if index in self.variables:
                    try:
                        index = int(self.variables[index])
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                else:
                    try:
                        index = int(index)
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                comp_var2 = self.lists[name][index]
                
            if str(comp_var1).isnumeric(): # falls zahl zu float convertieren
                comp_var1 = float(comp_var1)
            if str(comp_var2).isnumeric():
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
            else:
                return f"pexexit Kein valider if operator \'{current[2]}\' (Zeile {self.ptr + 1})"
            
        elif current[0] == "print": # ausgabe im terminal
            if current[1] in self.variables:
                self.ptr += 1
                return f"echo {str(self.variables[current[1]])}"
            elif str(current[1]).endswith(")"):
                name = current[1][0:current[1].find("(")]
                index = current[1][current[1].find("(") + 1 : current[1].find(")")]
                if index in self.variables:
                    try:
                        index = int(self.variables[index])
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                else:
                    try:
                        index = int(index)
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                self.ptr += 1
                return f"echo {self.lists[name][index]}"
            else:
                self.ptr += 1
                return f"echo {self.lines[self.ptr - 1][6::]}"
            
        elif current[0] in self.variables: # variablen redefinieren / mathe operationen
            sec_val = ""
            if current[2] in self.variables:
                sec_val = self.variables[current[2]]
            elif str(current[2]).endswith(")"):
                name = current[2][0:current[2].find("(")]
                index = current[2][current[2].find("(") + 1 : current[2].find(")")]
                if index in self.variables:
                    try:
                        index = int(self.variables[index])
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                else:
                    try:
                        index = int(index)
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                sec_val = self.lists[name][index]
            else:
                sec_val = current[2] # variable 
            if str(sec_val).isnumeric():
                sec_val = float(sec_val)

            if current[1] == "=":
                self.variables[current[0]] = sec_val # variable1 = variable2 (oder wert)
            elif current[1] == "+=":
                if type(self.variables[current[0]]) != type(sec_val):
                    return f"pexexit Inkompatibler Datentyp (Zeile {self.ptr + 1})"
                self.variables[current[0]] += sec_val # variable1 = variable1 + variable2 (oder wert)
            elif current[1] == "-=":
                if type(self.variables[current[0]]) != float or type(sec_val) != float:
                    return f"pexexit Inkompatibler Datentyp (Zeile {self.ptr + 1})"
                self.variables[current[0]] -= sec_val # variable1 = variable1 - variable2 (oder wert)
            elif current[1] == "*=":
                if type(self.variables[current[0]]) != float or type(sec_val) != float:
                    return f"pexexit Inkompatibler Datentyp (Zeile {self.ptr + 1})"
                self.variables[current[0]] *= sec_val
            elif current[1] == "/=":
                if type(self.variables[current[0]]) != float or type(sec_val) != float:
                    return f"pexexit Inkompatibler Datentyp (Zeile {self.ptr + 1})"
                self.variables[current[0]] /= sec_val
            self.ptr += 1
            
        elif current[0] == "while": # while schleife
            if self.ptr not in self.return_point:
                self.return_point.append(self.ptr) # return punkt erstellen
            comp_var1 = current[1] # werte anlegen
            comp_var2 = current[3]
            
            if comp_var1 in self.variables: # ueberpruefen ob es variablen sind
                comp_var1 = self.variables[comp_var1]
           
            elif str(comp_var1).endswith(")"):
                name = comp_var1[0:comp_var1.find("(")] 
                index = comp_var1[comp_var1.find("(") + 1 : comp_var1.find(")")] 
                if index in self.variables: 
                    try:
                        index = int(self.variables[index])
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                else:
                    try:
                        index = int(index)
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                comp_var1 = self.lists[name][index]
            if comp_var2 in self.variables:
                comp_var2 = self.variables[comp_var2]
            elif str(comp_var2).endswith(")"):
                name = comp_var2[0:comp_var2.find("(")]
                index = comp_var2[comp_var2.find("(") + 1 : comp_var2.find(")")]
                if index in self.variables:
                    try:
                        index = int(self.variables[index])
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                else:
                    try:
                        index = int(index)
                    except Exception:
                        return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                comp_var2 = self.lists[name][index]
                
            if str(comp_var1).isnumeric(): # falls zahl, zu float konvertieren
                comp_var1 = float(comp_var1)
            if str(comp_var2).isnumeric():
                comp_var2 = float(comp_var2)
                
            if current[2] == "==": # operation fuer die kondition ueberpruefen
                if comp_var1 == comp_var2:
                    self.ptr += 1 # falls True: => nichts
                else:
                    while self.terms[self.ptr][0] != "]":
                        self.ptr += 1 # falls False: => ans ende von schleife springen
                    self.ptr += 1
                    self.return_point.pop(len(self.return_point) - 1)
                    
            elif current[2] == "!=":
                if comp_var1 != comp_var2:
                    self.ptr += 1
                else:
                    while self.terms[self.ptr][0] != "]":
                        self.ptr += 1
                    self.ptr += 1
                    self.return_point.pop(len(self.return_point) - 1)
                    
        elif current[0] == "]": # ende von while schleife, springt zu schleifenbeginn
            self.ptr = self.return_point[len(self.return_point) - 1]
            
        elif current[0] in self.functions: # funktion ausfuehren
            self.functions[current[0]][1] = self.ptr + 1 # returnpunkt in funktion speichern
            self.ptr = self.functions[current[0]][0] # zeilenpointer auf start der funktion setzen
            
        elif current[0] == "return": # von funktion returnen
            self.ptr = self.functions[current[1]][1] # zeilenpointer auf vorher gespeicherten returnpunkt setzen
        
        elif current[0] == "ereturn": # "early return" also vor funktionsende
            self.ptr = self.functions[current[1]][1]
            
        elif current[0] == "input": # input erfragen
            self.ptr += 1
            return f"pinput {current[1]}"
            
        elif current[0] == "del": # variable loeschen
            self.ptr += 1
            self.variables.pop(current[1])
            
        elif current[0] == "list": # liste erstellen
            name = current[1] # name
            values = [] # werte
            for i in current[3:len(current) + 1]: # durch alle werte iterieren
                try: # falls wert zahl ist
                    values.append(float(i)) # zahl hinzufuegen
                except Exception: # sonst
                    values.append(i) # wert hinzufuegen
              
            self.lists[name] = values # dictionary eintrag erstellen
            self.ptr += 1
          
        elif str(current[0]).endswith(")"): # falls index von liste geaendert wird
            name = current[0][0:current[0].find("(")] # name
            index = current[0][current[0].find("(") + 1 : current[0].find(")")] # index aus den klammern
            if index in self.variables: # falls index variable ist
                try: # gucken ob variable eine zahl ist
                    index = int(self.variables[index])
                except Exception: # falls nicht, programm mit fehler beenden
                    return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
            else: # falls index keine variable ist
                try: # gucken ob index eine zahl ist
                    index = int(index)
                except Exception: # falls nicht, programm mit fehler beenden
                    return f"pexexit Index ist keine Zahl (Zeile {self.ptr + 1})"
                
            value = current[2] # wert 

            try: # falls wert eine zahl ist 
              value = float(value) # zu zahl konvertieren
            except Exception: # sonst nichts
              pass 
            
            self.lists[name][index] = value # wert an index in dict ersetzen
            self.ptr += 1
          
        elif current[0] == "append": # eintrag an liste anhaengen
            name = current[1] # name
            if name not in self.lists: # falls liste nicht vorhanden
              self.ptr += 1 
              return "" # nichts tun

            value = current[3] # wert 

            try: # falls wert zahl ist zu zahl konvertieren, sonst nichts tun
              value = float(value) 
            except Exception:
              pass 
             
            self.lists[name][1].append(value) # in list dictionary einfuegen
            self.ptr += 1
            
        elif current[0] == "clear": # terminal leeren
            self.ptr += 1
            return "cls" # clear befehl im terminal
        
        elif current[0] == "random": # zufaellige zahl zwischen angegeben argumenten
            name = current[1] # name
            lower = current[2] # untere grenze
            upper = current[3] # obere grenze
            try: # zu zahlen konvertieren
                lower = int(lower)
                upper = int(upper)
            except Exception: # falls keine zahl
                return f"pexexit Argument bei random ist keine Integer (Zeile {self.ptr + 1})" # programm mit fehler beenden
            self.variables[name] = randint(lower, upper) # in variablen dict einfuegen
            self.ptr += 1

        else:
            self.ptr += 1 # wenn zeile kein befehl, ignorieren
  
        if self.ptr < len(self.lines): 
            return "" 
        else:
            return "pexexit Programm beendet" # wenn alle zeilen ausgefuehrt, schliessen
        
    # TODO: ADD MORE KEYWORDS
    # TODO: ????GRAPHICAL MODE
    # TODO: add other comperative ops
    # TODO: write pex docs