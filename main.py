# Some Basic Imports
import random
import sys
import pygame
import os
from pygame.locals import *
from time import sleep
pygame.font.init()
# Global Variables
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 512
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUNDY = int(SCREEN_HEIGHT*0.8)
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
offset = SCREEN_HEIGHT//3
font = pygame.font.Font('freesansbold.ttf', 20)

if 'high score.txt' not in os.listdir():
    with open('high score.txt','w') as f:
        f.write('0')

#creating fuction to get random Pipe
def random_pipe():
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    
    pipeX = SCREEN_WIDTH+10
    y2 = offset + random.randrange(0, SCREEN_HEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset) 
    y1 = pipe_height - y2 + offset

    pipe = [
        {'x':pipeX,'y':-y1},#upper Pipe
        {'x':pipeX, 'y':y2}#lower Pipe
    ]
    return pipe

def is_collide(player_x,player_y,upperpipe,lowerpipe):
    if player_y>GROUNDY-25 or player_y<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperpipe:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if (pipe['y']+pipeheight>player_y and abs(player_x - pipe['x'])<GAME_SPRITES['player'].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
            
            
    
    for pipe in lowerpipe:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if (player_y+GAME_SPRITES['player'].get_height()>pipe['y'] and abs(player_x - pipe['x'])<GAME_SPRITES['player'].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    return False

def get_apple(x,y):
    SCREEN.blit(GAME_SPRITES['apple'],(x,y))
    

def get_text(x,y,text):
    text = font.render(text,True,(0,0,0))
    SCREEN.blit(text,(x,y))

# Creating welcome screen
def welcome_screen():
    player_x = int(SCREEN_WIDTH/5)
    player_y = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2)
    message_x = int((SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2)
    message_y = int(SCREEN_HEIGHT*0.13)
    base_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == K_SPACE):
                return
            
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0 ,0))
                SCREEN.blit(GAME_SPRITES['player'],(player_x,player_y ))
                SCREEN.blit(GAME_SPRITES['message'],(message_x,message_y))
                SCREEN.blit(GAME_SPRITES['base'],(base_x ,GROUNDY))
                pygame.display.update()

def main_game(score,i,life):
    player_x = int(SCREEN_WIDTH/5)
    player_y = int(SCREEN_HEIGHT/2)
    base_x = 0
    newpipe1 = random_pipe()
    newpipe2 = random_pipe()
    with open('high score.txt', 'r') as f:
        high_score = f.read()

    
    upperpipe = [
        {'x':SCREEN_WIDTH+200, 'y':newpipe1[0]['y']},
        {'x':SCREEN_WIDTH+200+(SCREEN_WIDTH//2), 'y':newpipe2[0]['y']}
    ]

    lowerpipe = [
        {'x':SCREEN_WIDTH+200, 'y':newpipe1[1]['y']},
        {'x':SCREEN_WIDTH+200+(SCREEN_WIDTH//2), 'y':newpipe2[1]['y']}
    ]

    velocity_pipe_x = -4
    velocity_player_y = -9
    max_velocity_player_y = 10
    min_velocity_player_y = -8
    accelaration_player_y = 1
    veloplayer = -8 #accelaration while flapping
    player_flapped = False
    apple_apper=False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == pygame.K_SPACE or event.key == K_UP):
                if player_y>0:
                    velocity_player_y = veloplayer
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()
        
        crash = is_collide(player_x,player_y,upperpipe,lowerpipe)#to check wether the palyer colide or not
        
        if crash:
            if life>1:
                life-=1
                main_game(score,i,life)
            return

        playermidpos = player_x + (GAME_SPRITES['player'].get_width()//2)
        for pipe in upperpipe:
            pipemidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()//2
            if pipemidpos+4<playermidpos<pipemidpos+8:
                score+=1
                GAME_SOUNDS['point'].play()
                
            
            if score > int(high_score):
                high_score = score
        
        if velocity_player_y<max_velocity_player_y and not player_flapped:
            velocity_player_y+=accelaration_player_y

        
        
        if player_flapped:
            player_flapped = False
        player_height = GAME_SPRITES['player'].get_height()
        player_y+=min(velocity_player_y , GROUNDY-player_y-player_height)

        for upper,lower in zip(upperpipe,lowerpipe):
            upper['x']+=velocity_pipe_x
            lower['x']+=velocity_pipe_x
        
        if 0<upperpipe[0]['x']<5:
            newpipe = random_pipe()
            lowerpipe.append(newpipe[1])
            upperpipe.append(newpipe[0])
        
        if upperpipe[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)

        if score==10*i:
            i+=1
            x = upperpipe[-1]['x']-GAME_SPRITES['pipe'][0].get_width()-20+150
            y = SCREEN_HEIGHT//3
            apple_apper=True


        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upper,lower in zip(upperpipe,lowerpipe):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upper['x'],upper['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lower['x'],lower['y']))
        
        SCREEN.blit(GAME_SPRITES['base'],(base_x,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(player_x,player_y))
        

        digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in digits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        offsetX = (SCREEN_WIDTH - width)//2

        for digit in digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(offsetX,int(0.12*SCREEN_HEIGHT)))
            offsetX+=GAME_SPRITES['numbers'][digit].get_width()
        
        get_text(4,GROUNDY+30,f'Hight Score {high_score}')
        get_text(SCREEN_WIDTH-70,GROUNDY+30,  f'Life {life}')
        if apple_apper:
            x+=velocity_pipe_x
            get_apple(x,y)
            if abs(player_x-x)<7 and (player_y-y)<4:
                x=-30
                if life<3:
                    life+=1
                    

        with open('high score.txt','w') as f:
            f.write(str(high_score))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Flappy Bird Game By Tarun")
    FPSCLOCK = pygame.time.Clock()

    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['apple'] = pygame.image.load('gallery/sprites/apple.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha())

    # Adding SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcome_screen()
        score=0
        i=1
        life = 1
        main_game(score,i,life)
    
