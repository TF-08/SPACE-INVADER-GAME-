import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
backgroundimg = pygame.image.load('freepik__upload__66794.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('arcade-game.png')
playerx = 370
playery = 480
playerx_change = 0

# Bullet
bulletimg = pygame.image.load('bullet.png')
bullety = 480
bulletx = 0
bullety_change = 10
bulletstate = "ready"

# Enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
numofenemies = 6

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
gameoverfont = pygame.font.Font('freesansbold.ttf', 64)
playagain_font = pygame.font.Font('freesansbold.ttf', 24)

def reset_game():
    global score, playerx, playery, bulletx, bullety, bulletstate, playerx_change
    global enemyx, enemyy, enemyx_change, enemyy_change

    score = 0
    playerx = 370
    playery = 480
    bulletx = 0
    bullety = 480
    bulletstate = "ready"
    playerx_change = 0

    enemyx = []
    enemyy = []
    enemyx_change = []
    enemyy_change = []

    for i in range(numofenemies):
        enemyimg.append(pygame.image.load('play.png'))
        enemyx.append(random.randint(0, 735))
        enemyy.append(random.randint(50, 250))
        enemyx_change.append(4)
        enemyy_change.append(40)

def gameovertext():
    overtext = gameoverfont.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))
    again_text = playagain_font.render("Press any key to play again or ESC to quit.", True, (255, 255, 255))
    screen.blit(again_text, (150, 350))

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def player(x, y):
    screen.blit(playerimg, (x, y))

def firebullet(x, y):
    global bulletstate
    bulletstate = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    return distance < 27

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# Initialize the game
reset_game()

# Game Loop
game_running = True
while game_running:
    running = True

    while running:
        screen.fill((0, 0, 0))
        screen.blit(backgroundimg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerx_change = -5
                if event.key == pygame.K_RIGHT:
                    playerx_change = 5
                if event.key == pygame.K_SPACE:
                    if bulletstate == 'ready':
                        mixer.Sound("laser.wav").play()
                        bulletx = playerx
                        firebullet(bulletx, bullety)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    playerx_change = 0

        # Player Movement
        playerx += playerx_change
        playerx = max(0, min(playerx, 736))

        # Bullet Movement
        if bulletstate == "fire":
            firebullet(bulletx, bullety)
            bullety -= bullety_change
        if bullety <= 0:
            bullety = 480
            bulletstate = "ready"

        # Enemy Movement
        game_over = False
        for i in range(numofenemies):
            if enemyy[i] > 440:
                game_over = True
                break

            enemyx[i] += enemyx_change[i]
            if enemyx[i] <= 0:
                enemyx_change[i] = 6
                enemyy[i] += enemyy_change[i]
            elif enemyx[i] >= 736:
                enemyx_change[i] = -4
                enemyy[i] += enemyy_change[i]

            if collision(enemyx[i], enemyy[i], bulletx, bullety):
                mixer.Sound("explosion.wav").play()
                bullety = 480
                bulletstate = "ready"
                score += 1
                enemyx[i] = random.randint(0, 735)
                enemyy[i] = random.randint(50, 150)

            enemy(enemyx[i], enemyy[i], i)

        if game_over:
            for i in range(numofenemies):
                enemyy[i] = 2000
            gameovertext()
            pygame.display.update()

            pygame.event.clear()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                        game_running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
                            running = False
                            game_running = False
                        else:
                            reset_game()
                            waiting = False

        player(playerx, playery)
        show_score(textX, textY)
        pygame.display.update()

pygame.quit()
    

# Game Over text

