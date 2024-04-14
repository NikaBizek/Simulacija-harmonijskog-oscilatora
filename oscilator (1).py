import pygame
import sys
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

pygame.init()

# konstante
WIDTH, HEIGHT = 900, 600
BACKGROUND_COLOR = (255, 255, 255)
BALL_COLOR = (0, 0, 255)
SPRING_COLOR = (0, 0, 0)
LINE_COLOR = (255, 0, 0)
MASS = 1  # Masa
ELASTIC_CONSTANT = 1  # konstanta opruge
v0 = 50 # početna brzina 
w = math.sqrt(ELASTIC_CONSTANT / MASS) # kutna brzina 
AMPLITUDE = (v0/w)*math.sqrt(2)  # amplituda titranja

#klasa za gumbe na ekranu
class Button:
    def __init__(self, x, y, width, height, text, color=(0, 255, 0), hover_color=(0,0,0), font_size=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.hovered = False

    def draw(self, screen):
        # provjerava prelazi li miš preko gumba
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.hovered = True
        else:
            self.hovered = False

        # crta gumb
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # ispisuje tekst
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def clicked(self):
        # provjerava je li gumb pritisnut
        return self.hovered and pygame.mouse.get_pressed()[0]

gumb_kreni = Button(50,120,100,50,"Start","black", (0, 0, 0),30)
gumb_stop = Button(160,120,100,50,"Reset","red", (255, 0, 0),30)
gumb_masa_plus = Button(50,220,100,50,"+","blue", (0, 0, 0),30)
gumb_masa_minus = Button(160,220,100,50,"-","blue", (0, 0, 0),30)
gumb_k_plus = Button(50,320,100,50,"+","green", (0, 0, 0),30)
gumb_k_minus = Button(160,320,100,50,"-","green", (0, 0, 0),30)
gumb_simulacija = Button(300,200,300,50,"SIMULACIJA TITRANJA","black",(0,0,0),30)
gumb_graf = Button(300,300,300,50,"GRAFOVI TITRANJA","black",(0,0,0),30)
gumb_brzina_plus = Button(50,420,100,50,"v0 +","pink",(0,0,0),30)
gumb_brzina_minus = Button(160,420,100,50,"v0 -","pink",(0,0,0),30)

# varijable
time = 0
clock = pygame.time.Clock()
simulacija = False

# liste koje spremaju podatke za grafove
displacement_data = []
velocity_data = []
acceleration_data = []

#petlja za main menu 
def main_menu():
    menu = True
    
    while menu:
        font = pygame.font.Font(None,50)
        screen.fill((255,255,255))
        text_surface = font.render(f"SIMULACIJA HARMONIJSKOG OSCILATORA", True, "black")
        screen.blit(text_surface, (85, 40)) 
        # crta gumb "SIMULACIJA TITRANJA" 
        gumb_simulacija.draw(screen)
        # crta gumb "GRAFOVI TITRANJA"
        gumb_graf.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # provjerava je li kliknut gumb da se prikažu grafovi
                if gumb_simulacija.clicked():
                    main()
                if gumb_graf:
                    grafovi()
                    draw_graphs()
        pygame.display.flip()
      
#računa položaj sustava u ovisnosti o vremenu
def calculate_position(time):
    w = math.sqrt(ELASTIC_CONSTANT / MASS)
    y = AMPLITUDE * math.sin(w * time)
    return y

#računa brzinu sustava u ovisnosti o vremenu
def calculate_velocity(time):
    w = math.sqrt(ELASTIC_CONSTANT / MASS)
    v = w * AMPLITUDE * math.cos(w * time)
    return v

#računa akceleraciju sustava u ovisnosti o vremenu
def calculate_acceleration(time):
    w = math.sqrt(ELASTIC_CONSTANT / MASS)
    a = -w ** 2 * AMPLITUDE * math.sin(w * time)
    return a

def update_graph_data():
    global time
    displacement = calculate_position(time)
    velocity = calculate_velocity(time)
    acceleration = calculate_acceleration(time)
    displacement_data.append((time, displacement))
    velocity_data.append((time, velocity))
    acceleration_data.append((time, acceleration))

def grafovi():
    prikaz = True
    while prikaz:
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    displacement_data.clear()
                    velocity_data.clear()
                    acceleration_data.clear()
                    main_menu()
        draw_graphs()
        pygame.display.flip()


def draw_graphs():
    plt.figure(figsize=(8, 6)) 
    plt.subplot(3, 1, 1)
    plt.plot(*zip(*displacement_data), color='red')
    plt.title('Displacement vs Time')
    plt.xlabel('Time')
    plt.ylabel('Displacement')

    plt.subplot(3, 1, 2)
    plt.plot(*zip(*velocity_data), color='green')
    plt.title('Velocity vs Time')
    plt.xlabel('Time')
    plt.ylabel('Velocity')

    plt.subplot(3, 1, 3)
    plt.plot(*zip(*acceleration_data), color='blue')
    plt.title('Acceleration vs Time')
    plt.xlabel('Time')
    plt.ylabel('Acceleration')

    plt.tight_layout() 
    plt.savefig('all_plots.png')  
    plt.close()  

    all_plots = pygame.image.load('all_plots.png')

    screen.blit(all_plots, (0, 0))

    pygame.display.flip()

    os.remove('all_plots.png')

# glavna petlja programa koja neprekidno provjerava i ažurira simulaciju
def main():
    global time, simulacija, MASS, ELASTIC_CONSTANT, v0, AMPLITUDE,w
    pygame.display.set_caption("Harmonijski oscilator")

    equilibrium_y = HEIGHT // 2   # pozicija ravnoteže 
    spring_y = 100  
    radijus = 20
    debljina = 2
    pocetak = "ne"

    while True:
        screen.fill(BACKGROUND_COLOR)
        gumb_kreni.draw(screen)
        gumb_stop.draw(screen)
        gumb_masa_plus.draw(screen)
        gumb_masa_minus.draw(screen)
        gumb_k_plus.draw(screen)
        gumb_k_minus.draw(screen)
        gumb_brzina_plus.draw(screen)
        gumb_brzina_minus.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    simulacija = False
                    MASS = 1  
                    AMPLITUDE = (v0/w)*math.sqrt(2)  
                    ELASTIC_CONSTANT = 1  
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gumb_brzina_plus.clicked() and pocetak == "ne":
                    if v0<100:
                        v0 += 1
                        AMPLITUDE = (v0/w)*math.sqrt(2)  
                if gumb_brzina_minus.clicked() and pocetak == "ne":
                    if v0>10:
                        v0 -= 1
                        AMPLITUDE = (v0/w)*math.sqrt(2)  
                if gumb_kreni.clicked():
                    pocetak = "da"
                    simulacija = True 
                if gumb_stop.clicked():
                    pocetak = "ne"
                    v0 = 50
                    debljina = 2
                    radijus = 20
                    ELASTIC_CONSTANT = 1 
                    MASS = 1  
                    w = math.sqrt(ELASTIC_CONSTANT/MASS)
                    AMPLITUDE = (v0/w)*math.sqrt(2) 
                    simulacija = False
                if gumb_masa_plus.clicked():
                    if MASS <100:
                        MASS += 1
                        radijus += 0.2
                if gumb_masa_minus.clicked():
                    if MASS>1:
                        MASS -= 1
                        radijus -= 0.2
                if gumb_k_plus.clicked():
                    if ELASTIC_CONSTANT <50:
                        ELASTIC_CONSTANT += 1
                        debljina += 0.2
                if gumb_k_minus.clicked():
                    if ELASTIC_CONSTANT > 1:
                        ELASTIC_CONSTANT -= 1
                        debljina -= 0.2

        # crta poziciju ravnoteže
        pygame.draw.line(screen, LINE_COLOR, (WIDTH//2-50, equilibrium_y), (WIDTH//2+50, equilibrium_y), 2)

        # crta oprugu i uteg
        displacement = calculate_position(time)
        y = equilibrium_y - displacement
        spring_end = (WIDTH // 2, spring_y)
        weight_pos = (WIDTH // 2, y)
        pygame.draw.line(screen, SPRING_COLOR, spring_end, weight_pos, int(debljina))
        pygame.draw.circle(screen, BALL_COLOR, weight_pos, radijus)

        if simulacija:
            update_graph_data()
            time += 0.1 

        # ispisuje tekst na ekranu
        font = pygame.font.Font(None,30)
        text_surface = font.render(f"MASA UTEGA: {MASS} kg", True, "blue")
        screen.blit(text_surface, (20, 20)) 
        text_surface = font.render(f"  KONSTANTA OPRUGE: {ELASTIC_CONSTANT} N/m ", True, "green")
        screen.blit(text_surface, (260, 20))
        text_surface = font.render(f" POCETNA BRZINA: {v0} m/s ", True, "pink")
        screen.blit(text_surface, (600, 20))
        text_surface = font.render(f" Klikni na tipku M za povratak na main menu ", True, "black")
        screen.blit(text_surface, (30, 550))
        

        pygame.display.flip()
        clock.tick(60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
while running:
    main_menu()
