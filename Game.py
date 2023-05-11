import pygame
import random
import math
from pygame import mixer

pygame.init()

#                                  w   h
screen = pygame.display.set_mode((800,600))

#Title of the game 
pygame.display.set_caption("Space Invader")

#Background image 
bckimg = pygame.image.load('png/bckimg.jpg')
def bck():
    screen.blit(bckimg,(0,0))

#background music
mixer.music.load('Musicfont/bckmusic.mp3')
mixer.music.play(-1)


#logo of the game
icon = pygame.image.load('png/icon.png')
pygame.display.set_icon(icon)

#setting up the score 
score = 0
#setting up the level 
level = 1
#setting up the highscore
highscore =[0,1,10,60]


#Setting up the player
playerimg = pygame.image.load("png/playerjet.png")
x = 375
y = 530
cx = 0
cy = 0
def player(x,y):
    screen.blit(playerimg,(x,y))



#Setting up the enemy
enemyimg = []
enemy_x = []
enemy_y = []
change_x = []
change_y = []
for i in range(6):
    enemyimg.append(pygame.image.load("png/enemy.png"))
    enemy_x.append(random.randint(55,800))
    enemy_y.append(-5)
    change_x.append(0.7)
    change_y.append(0)
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))


#setting up the asteroids
asteroidimg = []
as_x = []
as_y = []
chas_y = []
for z in range(4): 
    asteroidimg.append(pygame.image.load('png/asteroid.png'))
    as_x.append(random.randint(40,750))#as_x = asteroid x
    as_y.append(-10)
    chas_y.append(0.9) #chas_y = change as_y 
def asteroid(a,b,z):
    screen.blit(asteroidimg[z],(a,b)) 




#Setting up the bullet 
bulletimg = pygame.image.load('png/bullet.png')
bull_x = 0
bull_y = 530
bull_cy = 3.5 #cy = change y
status = "ready"
def bullet(x,y):
    global status
    status = "Fire"
    screen.blit(bulletimg,(x+2,y))


#setting up the collision 
def collision(x1,y1,x2,y2):
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if distance<27:
        return True
    else:
        return False

#drawing the score board
def rect():
    x = 0
    y = 0
    width = 310
    height = 130
    pygame.draw.rect(screen,(16,78,139),(x,y,width,height))

#drawing a border line
def line():
    st_x = 0
    st_y = 490
    en_x = 800
    en_y = 490
    wid = 5
    color =(16,78,139)
    pygame.draw.line(screen,color,(st_x,st_y),(en_x,en_y),wid)

#set up the text
scorefont = pygame.font.Font('Musicfont/SPACEBOY.TTF',28)
Gameoverfont = pygame.font.Font('Musicfont/SPACEBOY.TTF',65)
Levelfont = pygame.font.Font('Musicfont/SPACEBOY.TTF',28)

def show_score():
    scoreimg = scorefont.render('Score:'+str(score),True,(255,255,255))
    screen.blit(scoreimg,(9,10))

def show_level():
    levimg = Levelfont.render('Level:'+str(level),True,(255,255,255))
    screen.blit(levimg,(9,45))

def show_gameover():
    goimg = Gameoverfont.render("GAME OVER",True,(255,255,255))
    screen.blit(goimg,(120,250))

def show_highscore():
    highscoreimg = scorefont.render('HighScore:'+str(max(highscore)),True,(255,255,255))
    screen.blit(highscoreimg,(9,75))





run = True

while run:
#                r g b   
    screen.fill((0,0,0))
    bck()
    rect()
    line()
    show_score()
    show_level()
    show_highscore()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                 cx = -0.9 #cx = change x
            if event.key == pygame.K_RIGHT:
                 cx = 0.9 #cx = change X
            if event.key == pygame.K_UP:
                cy = -0.2 #cy = change y
            if event.key == pygame.K_DOWN:
                cy = 0.2 #cy = change y 
            if event.key == pygame.K_SPACE:
                if status == "ready":
                    bulmusic = mixer.Sound('Musicfont/fire.wav')
                    bulmusic.play()
                    bull_x = x
                    bullet(bull_x,bull_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 cx = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                 cy = 0

    x += cx 
    y += cy
    
    
    # setting the players boundaries
    if x<=0:
        x = 0
    elif x>=736:
        x = 736
    if y<=500:
        y = 500
    elif y>=528:
        y = 528
    player(x,y)


    #setting the enemy's boundaries
    for i in range(6):
        #gameover
        if enemy_y[i]>=470:
            for r in range(4):
                as_y[r] = 2000
                for j in range(6):
                    enemy_y[j] = 2000
            show_gameover()
            break
        
        
        enemy_x[i] += change_x[i]
        if enemy_x[i]<=10:
            change_x[i] = 0.7
            change_y[i] = 0.1
        elif enemy_x[i]>=720:
            change_x[i] = -0.7
            change_y[i] = 0.1

        enemy_y[i] += change_y[i]
        if enemy_y[i] >=520:
            enemy_y[i] = 520
    
    #bullet movement
    if status == "Fire":
        bullet(bull_x,bull_y)
        bull_y -= bull_cy      
    if bull_y <=0:
        bull_y = 530
        status = "ready"
    
    #checking for collision for enemy
    for i in range(6):
        if collision(bull_x,bull_y,enemy_x[i],enemy_y[i]):
            bl_sound = mixer.Sound('Musicfont/blast.wav')
            bl_sound.play()
            enemy_x[i] = random.randint(55,800)
            enemy_y[i] = -5
            score += 1
    #drawing the enemy 
        enemy(enemy_x[i],enemy_y[i],i)
     
        
    #drawing the asteroid
    for z in range(4):
        if collision(x,y,as_x[z],as_y[z]):
            for l in range(6):
                enemy_y[l] = 2000
                for k in range(4):
                    as_y[k] = 2000
            show_gameover()
            break
        

        as_y[z] += chas_y[z]
        asteroid(as_x[z],as_y[z],z)
        if as_y[z]>=750:
            as_x[z] = random.randint(10,575)
            as_y[z] = -10
    
    #shooting the asteroid
    for z in range(4):
        if collision(bull_x,bull_y,as_x[z],as_y[z]):
            score +=2
            as_x[z] = random.randint(10,575)
            as_y[z] = -10
   
    #setting up the level and speed 
    for i in range(6):
        if score == 15:
            level = 2
            change_x[i] = 1

    highscore.append(score)


    #updates everything
    pygame.display.update()
    