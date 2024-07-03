import pygame
import random


pygame.init()

# COLORS
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
YELLOW = [255,255,0]
RANDOM_COLOR =[random.randint(0,255),random.randint(0,255),random.randint(0,255)]

# SCREEN
WIDTH = 800
HEIGHT = 600
FPS = 30
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sara HMI")

# FONTS
font = pygame.font.Font(None, 36)

def draw_button(screen,text,x,y,width,height,color,action=None):
    pygame.draw.rect(screen,color,(x,y,width,height))
    text_surf = font.render(text,True,BLACK)
    screen.blit(text_surf,(x+10,y+10))

def send_command(command):
    print(f"Command sent: {command}")


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if 100<=x<=200 and 100<=y<=150:
                send_command("Move X")
            elif 100<=x<=200 and 200<=y<=250:
                send_command("Move Y")
            elif 100<=x<=200 and 300<=y<=350:
                send_command("Move Z")
            elif 100<=x<=200 and 400<=y<=450:
                send_command("Open Arm")
            elif 100<=x<=200 and 500<=y<=550:
                send_command("Close Arm")

    screen.fill(RANDOM_COLOR)
    draw_button(screen,"Move X",100,100,150,50,GREEN)
    draw_button(screen,"Move Y",100,200,150,50,GREEN)
    draw_button(screen,"Move Z",100,300,150,50,GREEN)
    draw_button(screen,"Open Arm",100,400,150,50,GREEN)
    draw_button(screen,"Close Arm",100,500,150,50,GREEN)


    pygame.display.flip()


    clock.tick(FPS)


pygame.quit()








