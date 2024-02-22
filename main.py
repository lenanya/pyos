# Imports
import pygame
from utils import button
from screens import desktop, settings, flappy, minesweeper

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
colors = {"RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREY": (145, 145, 145),
    "TEAL": (0, 145, 255)}

# Bildschirmdaten
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
scale_horizontal = screen_width / 1920
scale_vertical = screen_height / 1080
framerate = 60

# Font
font = pygame.font.SysFont('Arial Black', int(round(32 * scale_vertical)))

# Bildschirmflaeche erstellen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("PyOS")

# Dictionary von Fenstern
screens = {}
screens["desktop"] = desktop.Desktop(scale_horizontal, scale_vertical, screen, font)
screens["settings"] = settings.Settings(scale_horizontal, scale_vertical, screen, font)
screens["flappy"] = flappy.FlappyBird(scale_horizontal, scale_vertical, screen, font)
screens["minesweeper"] = minesweeper.Minesweeper(scale_horizontal, scale_vertical, screen, font)

# Variable zum wechseln von Fenstern
current_screen = "desktop"

# Taskleiste erstellen
class Taskbar():
    def __init__(self):
        self.taskbar_button_home = button.Button(0,0,100 * scale_horizontal, 100 * scale_vertical, WHITE, screen, "", font, "./assets/home.png", "./assets/home_hover.png")
        self.show_home = False
        with open("./settings/taskbarcolor.txt", "r") as f:
            read_color = f.read()
        self.taskbar_color = colors[read_color]
        self.home_hitbox = pygame.Rect((0,0, 400 * scale_horizontal, 605 * scale_vertical))
        self.home_button_desktop = button.Button(5 * scale_horizontal, 5 * scale_vertical, 390 * scale_horizontal, 45 * scale_vertical, BLUE, screen, "Desktop", font)
        self.home_button_settings = button.Button(5 * scale_horizontal, 55 * scale_vertical, 390 * scale_horizontal, 45 * scale_vertical, BLUE, screen, "Einstellungen", font)
        self.home_button_shutdown = button.Button(5 * scale_horizontal, 555 * scale_vertical, 390 * scale_horizontal, 45 * scale_vertical, BLUE, screen, "Herunterfahren", font)
        self.taskbar_running_tasks = []
        self.taskbar_buttons_running_tasks = []

    # Funktion um Taskleiste anzuzeigen
    def draw(self):
        with open("./settings/taskbarcolor.txt", "r") as f:
            read_color = f.read()
        self.taskbar_color = colors[read_color]
        pygame.draw.rect(screen, self.taskbar_color, (0,0, screen_width, 100 * scale_vertical))
        self.taskbar_button_home.draw()
        if self.show_home:
            pygame.draw.rect(screen, WHITE, (0,0, 400 * scale_horizontal, 605 * scale_vertical))
            self.home_button_settings.draw()
            self.home_button_desktop.draw()
            self.home_button_shutdown.draw()
        if not self.show_home:
            for i in self.taskbar_buttons_running_tasks:
                i.draw()

    # Funktionen der Taskleiste
    def run(self, mouse_position):
        if self.taskbar_button_home.is_hover(mouse_position):
            self.taskbar_button_home.sprite = self.taskbar_button_home.image_on_hover
        else:
            self.taskbar_button_home.sprite = self.taskbar_button_home.image

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

        if not self.show_home:
            for i in self.taskbar_buttons_running_tasks:
                if i.is_hover(mouse_position):
                    i.sprite = i.image_on_hover
                else:
                    i.sprite = i.image

    def click_check(self, event_pos):
        if self.show_home:
            if self.home_button_settings.is_pressed(event_pos):
                return "settings"
            elif self.home_button_desktop.is_pressed(event_pos):
                return "desktop"
            elif self.home_button_shutdown.is_pressed(event_pos):
                return "shutdown"
        
        if not self.show_home:
            for i in self.taskbar_buttons_running_tasks:
                if i.is_pressed(event_pos):
                    return i.text

        if self.taskbar_button_home.is_pressed(event_pos):
            self.show_home = True
        if not self.home_hitbox.collidepoint(event_pos):
            self.show_home = False
        return None
        

taskbar = Taskbar()

running = True

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            change = taskbar.click_check(event.pos)
            if change == "shutdown":
                running = False
                break
            if change != None and change in screens.keys():
                current_screen = change
                
            if current_screen == "desktop":
                current_screen= screens["desktop"].click_check(event.pos)

            elif current_screen == "flappy":
                if screens["flappy"].click_check(event.pos) == "exit":
                    for i in range(len(taskbar.taskbar_buttons_running_tasks)):
                        if i < len(taskbar.taskbar_running_tasks):
                            if type(taskbar.taskbar_running_tasks[i]) == flappy.FlappyBird:
                                taskbar.taskbar_running_tasks.pop(i)
                                for e in range(1, len(taskbar.taskbar_buttons_running_tasks)):
                                    if i + e < len(taskbar.taskbar_buttons_running_tasks):
                                        taskbar.taskbar_buttons_running_tasks[i + e].x -= 105 * scale_horizontal
                                        taskbar.taskbar_buttons_running_tasks[i + e].hitbox.x -= 105 * scale_horizontal
                                taskbar.taskbar_buttons_running_tasks.pop(i)
                    current_screen = "desktop"

            elif current_screen == "settings":
                if screens["settings"].click_check(event.pos) == "exit":
                    for i in range(len(taskbar.taskbar_buttons_running_tasks)):
                        if i < len(taskbar.taskbar_running_tasks):
                            if type(taskbar.taskbar_running_tasks[i]) == settings.Settings:
                                taskbar.taskbar_running_tasks.pop(i)
                                for e in range(1, len(taskbar.taskbar_buttons_running_tasks)):
                                    if i + e < len(taskbar.taskbar_buttons_running_tasks):
                                        taskbar.taskbar_buttons_running_tasks[i + e].x -= 105 * scale_horizontal
                                        taskbar.taskbar_buttons_running_tasks[i + e].hitbox.x -= 105 * scale_horizontal
                                taskbar.taskbar_buttons_running_tasks.pop(i)
                    current_screen = "desktop"
            
            elif current_screen == "minesweeper":
                if screens["minesweeper"].click_check(event.pos) == "exit":
                    for i in range(len(taskbar.taskbar_buttons_running_tasks)):
                        if i < len(taskbar.taskbar_running_tasks):
                            if type(taskbar.taskbar_running_tasks[i]) == minesweeper.Minesweeper:
                                taskbar.taskbar_running_tasks.pop(i)
                                for e in range(1, len(taskbar.taskbar_buttons_running_tasks)):
                                    if i + e < len(taskbar.taskbar_buttons_running_tasks):
                                        taskbar.taskbar_buttons_running_tasks[i + e].x -= 105 * scale_horizontal
                                        taskbar.taskbar_buttons_running_tasks[i + e].hitbox.x -= 105 * scale_horizontal
                                taskbar.taskbar_buttons_running_tasks.pop(i)
                    current_screen = "desktop"

        # Alle events der Liste hinzufuegen
        events.append(event)
        
    
    # Variable die das momentane Fenster beinhaltet
    current = screens[current_screen]
    if current not in taskbar.taskbar_running_tasks and current_screen != "desktop":
        taskbar.taskbar_running_tasks.append(current)
        taskbar.taskbar_buttons_running_tasks.append(button.Button(105 * len(taskbar.taskbar_running_tasks) * scale_horizontal, 0 * scale_vertical, 100 * scale_horizontal, 100 * scale_vertical, BLUE, screen, current_screen, font, f"./assets/{current_screen}.png", f"./assets/{current_screen}_hover.png"))

    # Funktionen des Fensters ausfuehren
    current.run(mouse_position, events)

    # Funktionen der Taskleiste ausfuehren
    taskbar.run(mouse_position)

    # Momentanes Fenster anzeigen
    current.draw()
    
    # Taskleiste anzeigen
    taskbar.draw()

    # Bildschirm updaten
    pygame.display.flip()

    # Framerate festlegen
    clock.tick(framerate)

# TODO: ADD TASKBAR RIGHT CLICK MENU
# TODO: ADD TIME 
# TODO: ADD PINNING TO TASKBAR
# TODO: ?SHOW WIFI 
# TODO: ADD FILE MANAGER
# TODO: ADD TEXT EDITOR
# TODO: ?ADD TETRIS
# TODO: ?ADD HTML RENDERER
