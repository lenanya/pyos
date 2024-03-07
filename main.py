# Imports
import pygame
import sys
from utils import button
from screens import desktop, settings, flappy, minesweeper, explorer, terminal, editor

# pygame initialisieren
pygame.init()

# Timer 
clock = pygame.time.Clock()

# Farben
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (145, 145, 145)
TEAL = (0, 145, 255)
# dictionary fuer farben, benoetigt fuer taskleiste
colors = {"RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREY": (145, 145, 145),
    "TEAL": (0, 145, 255)}

# Bildschirmdaten
screen_width = pygame.display.Info().current_w # bildschirmbreite
screen_height = pygame.display.Info().current_h # bildschirmhoehe

# verhaeltnis zu standard bildschirm um alles zu skalieren
scale_horizontal = screen_width / 1920 
scale_vertical = screen_height / 1080

framerate = 60

# Font
if scale_vertical <= scale_horizontal:
    font = pygame.font.SysFont('Arial Black', int(round(32 * scale_vertical))) # auch auf hoehe skaliert
else:
    font = pygame.font.SysFont('Arial Black', int(round(32 * scale_horizontal)))           
                                    
# Bildschirmflaeche erstellen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("PyOS")

# Dictionary von Fenstern um wechseln zu vereinfachen
screens = {}
screens["desktop"] = desktop.Desktop(scale_horizontal, scale_vertical, screen, font)
screens["settings"] = settings.Settings(scale_horizontal, scale_vertical, screen, font)
screens["flappy"] = flappy.FlappyBird(scale_horizontal, scale_vertical, screen, font)
screens["minesweeper"] = minesweeper.Minesweeper(scale_horizontal, scale_vertical, screen, font)
screens["terminal"] = terminal.Terminal(scale_horizontal, scale_vertical, screen, font)
screens["editor"] = editor.Editor(scale_horizontal, scale_vertical, screen, font)


# Variable zum Wechseln von Fenstern
current_screen = "desktop"

# Taskleiste erstellen
class Taskbar():
    def __init__(self):
        # Home button
        self.taskbar_button_home = button.Button(0,0,100 * scale_horizontal, 100 * scale_vertical, WHITE, screen, "", font, "./assets/home.png", "./assets/home_hover.png")
        self.show_home = False # Variable ob das home menue angezeigt wird
        
        # Taskbar Farbe aus Einstellungen lesen
        with open("./settings/taskbarcolor.txt", "r") as f: # datei im lesemodus oeffnen
            read_color = f.read() # farbe auslesen
        self.taskbar_color = colors[read_color] # hier kommt das dictionary von vorhin zu gebrauch
        
        # Home Menue mit knoepfen erstellen, hitbox ist um
        # das menue auszublenden wenn ausserhalb von dem menu gedrueckt wird
        self.home_hitbox = pygame.Rect((0,0, 400 * scale_horizontal, 605 * scale_vertical))
        self.home_button_desktop = button.Button(5 * scale_horizontal, 5 * scale_vertical, 390 * scale_horizontal, 45 * scale_vertical, BLUE, screen, "Desktop", font)
        self.home_button_settings = button.Button(5 * scale_horizontal, 55 * scale_vertical, 390 * scale_horizontal, 45 * scale_vertical, BLUE, screen, "Einstellungen", font)
        self.home_button_shutdown = button.Button(5 * scale_horizontal, 555 * scale_vertical, 390 * scale_horizontal, 45 * scale_vertical, BLUE, screen, "Herunterfahren", font)
        
        # Listen um offene Apps zu merken und buttons fuer sie zu erstellen
        self.taskbar_running_tasks = []
        self.taskbar_buttons_running_tasks = []

    # Funktion um Taskleiste anzuzeigen
    def draw(self):
        # Taskbar Farbe aus Einstellungen lesen
        with open("./settings/taskbarcolor.txt", "r") as f:
            read_color = f.read()
        self.taskbar_color = colors[read_color]
        
        # Taskleiste anzeigen
        pygame.draw.rect(screen, self.taskbar_color, (0,0, screen_width, 100 * scale_vertical))
        
        # Home button anzeigen
        self.taskbar_button_home.draw()
        
        # Home Menue anzeigen falls noetig
        if self.show_home:
            # hintergrund vom home menue
            pygame.draw.rect(screen, WHITE, (0,0, 400 * scale_horizontal, 605 * scale_vertical))
            # buttons im home menue anzeigen
            self.home_button_settings.draw()
            self.home_button_desktop.draw()
            self.home_button_shutdown.draw()
        
        # offene apps auf taskleiste anzeigen, falls home menue nicht angezeigt
        if not self.show_home:
            for i in self.taskbar_buttons_running_tasks: # durch offene apps iterieren
                i.draw() # buttons anzeigen

    # Funktionen der Taskleiste
    def run(self, mouse_position):
        # sprites / farbe von buttons in taskleiste / home menue zu hover / hellblau
        # aender falls die maus ueber ihnen ist
        if self.taskbar_button_home.is_hover(mouse_position): # falls maus auf knopf :
            self.taskbar_button_home.sprite = self.taskbar_button_home.image_on_hover # bild wird zu hover version geaendert
        else:                                                 # sonst:
            self.taskbar_button_home.sprite = self.taskbar_button_home.image # bild wird zu dem normalen gewechselt

        if self.home_button_desktop.is_hover(mouse_position):
            self.home_button_desktop.color = TEAL
        else:
            self.home_button_desktop.color = BLUE

        if self.home_button_settings.is_hover(mouse_position):
            self.home_button_settings.color = TEAL
        else:
            self.home_button_settings.color = BLUE

        if self.home_button_shutdown.is_hover(mouse_position):
            self.home_button_shutdown.color = TEAL
        else:
            self.home_button_shutdown.color = BLUE

        
        # dasselbe fuer offene apps, falls kein home menue angezeigt wird
        if not self.show_home:
            for i in self.taskbar_buttons_running_tasks: # durch liste iterieren
                if i.is_hover(mouse_position): # dasselbe wie beim home menue
                    i.sprite = i.image_on_hover # "
                else:                          # "
                    i.sprite = i.image          # "

    # funktion um zu ueberpruefen ob buttons gedrueckt sind
    def click_check(self, event_pos): # erhaelt event position von hauptschleife
        # home menue buttons ueberpruefen, und das jeweilige fenster an
        # die hauptschleife returnen, um das fenster zu wechseln
        if self.show_home:
            if self.home_button_settings.is_pressed(event_pos):
                return "settings"
            elif self.home_button_desktop.is_pressed(event_pos):
                return "desktop"
            elif self.home_button_shutdown.is_pressed(event_pos):
                return "shutdown"
        
        # offene apps buttons ueberpruefen,
        if not self.show_home:
            for i in self.taskbar_buttons_running_tasks: # durch tasks iterieren
                if i.is_pressed(event_pos): # falls knopf gedrueckt:
                    return i.text # returned den text des buttons, also
                                  # den namen der app/des fensters

        # home menue button ueberpruefen
        if self.taskbar_button_home.is_pressed(event_pos):
            self.show_home = True
        if not self.home_hitbox.collidepoint(event_pos): # falls ausserhalb von home menue gedrueckt wird
            self.show_home = False
        return None # falls keiner der buttons gedrueckt ist
        

taskbar = Taskbar() # taskbar klassen objekt erstellen

running = True # variable die bestimmt ob das "OS" an ist

# Hauptschleife
while running:

    # Maus Position updaten
    mouse_position = pygame.mouse.get_pos()
    
    # Liste von events erstellen um sie an Classes weitergeben zu koennen
    events = []

    # Event handler
    for event in pygame.event.get():
        # Um das Fenster schliessen zu koennen
        if event.type == pygame.QUIT:
            running = False

        # ueberpruefen ob geklickt wird
        elif event.type == pygame.MOUSEBUTTONDOWN:
            change = taskbar.click_check(event.pos) # ueberpruefen ob eins der offenen programme
                                                    # auf der taskleiste geklickt wurde
            if change == "shutdown":
                running = False
                break # break -> hauptschleife abbrechen 
            if change != None and change in screens.keys(): 
                current_screen = change # momentaner bildschirm wird aktualisiert
                
            if current_screen == "desktop": # falls auf dem desktop: 
                current_screen = screens["desktop"].click_check(event.pos) # ueberpruefen ob
                                                                           # auf dem desktop etwas geklick wurde

            # ueberpruefen ob in dem momentan offenen fenster der button zum schliessen
            # gedrueckt wurde und falls dem so ist, dieses schliessen und aus den
            # listen der offenen apps entfernen
            if screens[current_screen].click_check(event.pos) == "exit": # falls exit knopf gedrueckt
                app_index = taskbar.taskbar_running_tasks.index(current_screen)
                taskbar.taskbar_running_tasks.pop(app_index) # app aus liste entfernen
                # andere apps und ihre buttons in der taskleiste nach vorne holen
                for e in range(app_index, len(taskbar.taskbar_buttons_running_tasks)):
                    if e < len(taskbar.taskbar_buttons_running_tasks): # falls app nicht die letzte
                        
                        taskbar.taskbar_buttons_running_tasks[e].x -= 105 * scale_horizontal # knopf vorziehen
                        taskbar.taskbar_buttons_running_tasks[e].hitbox.x -= 105 * scale_horizontal # hitbox vom knopf vorziehen
                        
                taskbar.taskbar_buttons_running_tasks.pop(app_index) # app aus liste von buttons entfernen
                        
                current_screen = "desktop" # app geschlossen, also => desktop


        events.append(event) # Alle events der Liste hinzufuegen
        
    current = screens[current_screen] # Variable die das momentane Fenster beinhaltet
    
    if current_screen not in taskbar.taskbar_running_tasks and current_screen != "desktop": # um keine app doppelt zu haben
        taskbar.taskbar_running_tasks.append(current_screen) # app der liste hinzufuegen
        # knopf fuer die app in die liste hinzufuegen
        taskbar.taskbar_buttons_running_tasks.append(button.Button(105 * len(taskbar.taskbar_running_tasks) * scale_horizontal, 0 * scale_vertical, 100 * scale_horizontal, 100 * scale_vertical, BLUE, screen, current_screen, font, f"./assets/{current_screen}.png", f"./assets/{current_screen}_hover.png"))

    current.run(mouse_position, events) # Funktionen des momentanen Fensters ausfuehren

    taskbar.run(mouse_position) # Funktionen der Taskleiste ausfuehren

    current.draw() # Momentanes Fenster anzeigen
    
    taskbar.draw() # Taskleiste anzeigen

    pygame.display.flip() # Bildschirm updaten

    clock.tick(framerate) # Framerate festlegen
    
sys.exit() # wenn hauptschleife beendet, programm schliessen

