'''
Ilker Kilincarslan 1600002148
Fall-2020 Analysis of Algorithms Term Project
Topic : Hangman Game using Brute Force Algorithm #line90
Actual code starts at #line406
'''
import pygame, sys
from pygame.locals import *
import random

from pygame.mixer import stop

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)
YELLOW = (255,255,0)

hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

pygame.init()
pygame.display.set_caption('CSE0416-TermProject(Hangman Game with Brute Force Algorithm)FALL-2020')

winHeight = 480
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))

click = False
bgColor = (128,255,0)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
settingTxtFont = pygame.font.SysFont('comicsans', 30)

word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

correctSound = pygame.mixer.Sound('correct.wav')
wrongSound = pygame.mixer.Sound('wrong.wav')
failSound = pygame.mixer.Sound('fail.wav')
applauseSound = pygame.mixer.Sound('applause.wav')
clickSound = pygame.mixer.Sound('click.wav')
music = pygame.mixer.music.load('music.wav')
musicPlay = True

pygame.mixer.music.play(-1)

limbs = 0
atGame = False
circleColor = LIGHT_BLUE

def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    global circleColor
    win.fill(bgColor)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:            
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, circleColor, (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()

def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]

def hang(guess):
    global word
    
    i = 0
    while i < len(word):                    #start Brute Force
        if word[i].lower() != guess.lower():# search entire string one by one
            i += 1                          # like in the Brute Force
        else:
            correctSound.play()
            pygame.time.delay(100)
            return False                    
    wrongSound.play()    
    pygame.time.delay(100)
    return True                             # end Brute Force

def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(bgColor)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()

def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

def settings():
    global musicPlay
    if  not musicPlay:        
        pygame.mixer.music.stop()
    global click
    global bgColor
    global circleColor
    running = True    
    while running:
        win.fill(bgColor)
        
        text1 = settingTxtFont.render('Choose Background Color',1,WHITE)
        text2 = settingTxtFont.render('Choose Circle Color',1,WHITE)
        text3 = settingTxtFont.render('Music',1,WHITE)
        text4 = settingTxtFont.render('ON',1,WHITE)
        text5 = settingTxtFont.render('OFF',1,WHITE)
        
        win.blit(text1,(10,10))
        win.blit(text2,(10,160))
        win.blit(text3,(10,290))
        win.blit(text4,(10,330))
        win.blit(text5,(70,330))
        
        x,y = pygame.mouse.get_pos()
            
        button_1 = pygame.Rect(10, 50, 50, 50)
        button_2 = pygame.Rect(70, 50, 50, 50)
        button_3 = pygame.Rect(130, 50, 50, 50)
        button_4 = pygame.Rect(190, 50, 50, 50)
        button_5 = pygame.Rect(250, 50, 50, 50)
        button_6 = pygame.Rect(310, 50, 50, 50)
        button_15 = pygame.Rect(370, 50, 50, 50)
        
        button_7 = pygame.Rect(10, 200, 50, 50)
        button_8 = pygame.Rect(70, 200, 50, 50)
        button_9 = pygame.Rect(130, 200, 50, 50)
        button_10 = pygame.Rect(190, 200, 50, 50)
        button_11 = pygame.Rect(250, 200, 50, 50)
        button_12 = pygame.Rect(310, 200, 50, 50)
        button_16 = pygame.Rect(370, 200, 50, 50)
        
        button_13 = pygame.Rect(10, 350, 30, 30)
        button_14 = pygame.Rect(70, 350, 30, 30)
        
        if button_1.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = RED                
        if button_2.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = WHITE
        if button_3.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = BLUE                
        if button_4.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = GREEN
        if button_5.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = LIGHT_BLUE                
        if button_6.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = BLACK
        if button_15.collidepoint((x, y)):
            if click:
                clickSound.play()
                bgColor = YELLOW
                
        if button_7.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = RED                
        if button_8.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = WHITE
        if button_9.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = BLUE                
        if button_10.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = GREEN
        if button_11.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = LIGHT_BLUE                
        if button_12.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = BLACK
        if button_16.collidepoint((x, y)):
            if click:
                clickSound.play()
                circleColor = YELLOW
                
        if button_13.collidepoint((x, y)):
            if click:
                clickSound.play()
                musicPlay = True
                pygame.mixer.music.play(-1)
        if button_14.collidepoint((x, y)):
            if click:
                clickSound.play()
                musicPlay = False
                pygame.mixer.music.stop()
        
        
        pygame.draw.rect(win, RED, button_1)
        pygame.draw.rect(win, WHITE, button_2)
        pygame.draw.rect(win, BLUE, button_3)
        pygame.draw.rect(win, GREEN, button_4)
        pygame.draw.rect(win, LIGHT_BLUE, button_5)
        pygame.draw.rect(win, BLACK, button_6)
        pygame.draw.rect(win, RED, button_7)
        pygame.draw.rect(win, WHITE, button_8)
        pygame.draw.rect(win, BLUE, button_9)
        pygame.draw.rect(win, GREEN, button_10)
        pygame.draw.rect(win, LIGHT_BLUE, button_11)
        pygame.draw.rect(win, BLACK, button_12)     
        pygame.draw.rect(win, BLACK, button_13)     
        pygame.draw.rect(win, BLACK, button_14)     
        pygame.draw.rect(win, YELLOW, button_15) 
        pygame.draw.rect(win, YELLOW, button_16) 
        
        click = False
        
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if atGame:
                            game()
                        else:
                            running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clickSound.play()
                        click = True
                        
        pygame.display.update()
    
def game():
    if  not musicPlay:        
        pygame.mixer.music.stop()
    global limbs
    while True:        
        redraw_game_window()
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainMenu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                letter = buttonHit(clickPos[0], clickPos[1])
                if letter != None:
                    clickSound.play()
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if hang(chr(letter)):
                        if limbs != 5:
                            limbs += 1
                        else:
                            limbs += 1                            
                            failSound.play()
                            pygame.time.delay(1000)
                            end()
                    else:
                        print(spacedOut(word, guessed))
                        if spacedOut(word, guessed).count('_') == 0:
                            applauseSound.play()
                            end(True)

def mainMenu():
    if  not musicPlay:        
        pygame.mixer.music.stop()   
    global click 
    global atGame
    while True:
        win.fill(bgColor)
        
        text1 = settingTxtFont.render('PLAY',1,WHITE)
        text2 = settingTxtFont.render('SETTINGS',1,WHITE)
        text3 = settingTxtFont.render('QUIT',1,WHITE)
        
        win.blit(text1,(((winWidth/2)-(text1.get_width()/2)),((winHeight/2-60)-(text1.get_height()/2))))
        win.blit(text2,(((winWidth/2)-(text1.get_width())),((winHeight/2+15)-(text1.get_height()/2))))
        win.blit(text3,(((winWidth/2)-(text1.get_width()/2)),((winHeight/2+90)-(text1.get_height()/2))))        
        
        x,y = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(winWidth/2-100, winHeight/2-50, 200, 50)
        button_2 = pygame.Rect(winWidth/2-100, winHeight/2+25, 200, 50)
        button_3 = pygame.Rect(winWidth/2-100, winHeight/2+100, 200, 50)       
        
        if button_1.collidepoint((x, y)):
            if click:
                atGame = True
                game()                
        if button_2.collidepoint((x, y)):
            if click:
               click = False 
               settings()                                         
        if button_3.collidepoint((x,y)):
            if click:
                pygame.quit()
               
        pygame.draw.rect(win, RED, button_1)
        pygame.draw.rect(win, RED, button_2)
        pygame.draw.rect(win, RED, button_3)
        
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clickSound.play()
                    click = True
        
        pygame.display.update()

#MAINLINE

# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])    
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = randomWord()
               
mainMenu()