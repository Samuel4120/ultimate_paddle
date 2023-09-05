import sys, pygame, time, random

#ConstantS
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
CENTER_FIELD_X = 500
CENTER_FIELD_Y = 350
WIDTH_PADDLE = 15
LENGTH_PADDLE = 120
PADDLE_Y = CENTER_FIELD_Y - (LENGTH_PADDLE/2) 
SCORE1_X = CENTER_FIELD_X - 125
SCORE2_X = CENTER_FIELD_X + 100
SCORE_Y = 45
SCORE_TO_WIN = 5
UPPER_LIMIT = 5
LOWER_LIMIT = 695
MAX_SPEED = 15

#Game intialization
pygame.init()
FPS = 60
gameOver = True
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

#Window 
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Ultimate Paddle")

#Text
fontScore = pygame.font.Font('freesansbold.ttf', 40)
fontGameOver = pygame.font.Font('freesansbold.ttf', 72)
fontKeys = pygame.font.Font('freesansbold.ttf', 12)

#Score
Score1 = 0
Score2 = 0

#Paddle
lenght_pad = LENGTH_PADDLE
P1_posY = PADDLE_Y
P2_posY = PADDLE_Y
P1_changeY = 0
P2_changeY = 0

#Ball
Ball_changeX = 5
Ball_changeY = 5
Ball_posX = CENTER_FIELD_X
Ball_posY = CENTER_FIELD_Y


def drawField():
    pygame.draw.line(screen, WHITE, (0, 25), (1000, 25), 3)
    pygame.draw.line(screen, WHITE, (0, 675), (1000, 675), 3)
    pygame.draw.line(screen, WHITE, (500, 25), (500, 675))
    pygame.draw.circle(screen, WHITE, (CENTER_FIELD_X, CENTER_FIELD_Y), 50, 1)

def drawControlKeys():
    keys1_text = fontKeys.render("Control Keys:", True, WHITE)
    keys2_text = fontKeys.render("Player1 (W and S)", True, WHITE)
    keys3_text = fontKeys.render("Player2 (Up and Down)", True, WHITE)

    screen.blit(keys1_text, (25, 50))
    screen.blit(keys2_text, (25, 75))
    screen.blit(keys3_text, (25, 95))

def displayStartScreen():
    drawControlKeys()
    start_text = fontScore.render("PRESS SPACE TO START", True, WHITE)
    screen.blit(start_text, (CENTER_FIELD_X - 250, CENTER_FIELD_Y - 150))
    """ UNCOMMENT FOR BLINKING TEXT
    pygame.display.update()
    time.sleep(0.5)
    start_text = fontScore.render("PRESS SPACE TO START", True, BLACK)
    screen.blit(start_text, (CENTER_FIELD_X - 250, CENTER_FIELD_Y - 150))
    pygame.display.update()
    time.sleep(0.5)
    """

def isHit(Player_posY, Ball_posY):
    return Ball_posY >= Player_posY and Ball_posY <= Player_posY + lenght_pad

def drawScore(score, x, y):
    score_txt = fontScore.render(str(score), True, WHITE)
    screen.blit(score_txt, (x, y))

def displayGameOverScreen(score1, score2):
    if score1 > score2:
        game_over_txt = fontGameOver.render("Player 1 Wins!", True, WHITE)
    else:
        game_over_txt = fontGameOver.render("Player 2 Wins!", True, WHITE)
    screen.blit(game_over_txt, (CENTER_FIELD_X - 240, CENTER_FIELD_Y - 225))
    pygame.display.update()


while True:
    FPSCLOCK = pygame.time.Clock()
    screen.fill(BLACK)
    drawField()

    if gameOver:
        displayStartScreen()
        P1_changeY = 0
        P2_changeY = 0
        Ball_changeX = 0
        Ball_changeY = 0
    
    for event in pygame.event.get():
        #Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Start Game
        if gameOver and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gameOver = False
                Ball_changeX = -5
                Ball_changeY = 5

        #Player movement
        if not gameOver and event.type == pygame.KEYDOWN:
            #PLayer 1
            if event.key == pygame.K_w:
                P1_changeY = -10
            if event.key == pygame.K_s:
                P1_changeY = 10
            #PLayer 2
            if event.key == pygame.K_UP:
                P2_changeY = -10
            if event.key == pygame.K_DOWN:
                P2_changeY = 10
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: #or pygame.K_s:
                P1_changeY = 0
            if event.key == pygame.K_s:
                P1_changeY = 0
            if event.key == pygame.K_UP: #or pygame.K_DOWN:
                P2_changeY = 0
            if event.key == pygame.K_DOWN:
                P2_changeY = 0

    
    #Player movment
    if P1_posY < UPPER_LIMIT:
        P1_changeY = 0
        P1_posY = UPPER_LIMIT
    elif P1_posY > LOWER_LIMIT - lenght_pad:
        P1_changeY = 0
        P1_posY = LOWER_LIMIT - lenght_pad

    if P2_posY < UPPER_LIMIT:
        P2_changeY = 0
        P2_posY = UPPER_LIMIT
    elif P2_posY > LOWER_LIMIT - lenght_pad:
        P2_changeY = 0
        P2_posY = LOWER_LIMIT - lenght_pad

    P1_posY += P1_changeY
    P2_posY += P2_changeY

    #Hit
    if(Ball_posX in range(905, 921) and isHit(P2_posY, Ball_posY)):
        Ball_changeX = max(-abs(Ball_changeX) - 1, -MAX_SPEED)
        lenght_pad -= 1
        Ball_changeY = random.randint(-10, 10)
    elif(Ball_posX in range(65, 81) and isHit(P1_posY, Ball_posY)):
        Ball_changeX =  min(abs(Ball_changeX) + 1, MAX_SPEED)
        lenght_pad -= 1
        Ball_changeY = random.randint(-8, 8)
    
    #Ball movement
    if(Ball_changeY >= 0 and Ball_posY > 650):
        Ball_changeY = -Ball_changeY
    elif(Ball_changeY <= 0 and Ball_posY < 50):
        Ball_changeY = -Ball_changeY 
    
    Ball_posX += Ball_changeX
    Ball_posY += Ball_changeY

    #Scored
    if(Ball_changeX >= 0 and Ball_posX > 1000):
        Ball_changeX = -5
        Ball_posX = CENTER_FIELD_X
        Ball_posY = CENTER_FIELD_Y
        Score1 += 1
        lenght_pad = LENGTH_PADDLE
    elif(Ball_changeX <= 0 and Ball_posX < 0):
        Ball_changeX = 5
        Ball_posX = CENTER_FIELD_X
        Ball_posY = CENTER_FIELD_Y
        Score2 += 1
        lenght_pad = LENGTH_PADDLE
    
    pygame.draw.rect(screen, WHITE, (50, P1_posY, WIDTH_PADDLE, lenght_pad))
    pygame.draw.rect(screen, WHITE, (920, P2_posY, WIDTH_PADDLE, lenght_pad))
    pygame.draw.circle(screen, WHITE, (Ball_posX, Ball_posY), 15)
    
    drawScore(Score1, SCORE1_X, SCORE_Y)
    drawScore(Score2, SCORE2_X, SCORE_Y)

    if Score1 == SCORE_TO_WIN or Score2 == SCORE_TO_WIN:
        displayGameOverScreen(Score1, Score2)
        time.sleep(3)
        gameOver = True
        Score1 = 0
        Score2 = 0
        P1_posY = PADDLE_Y
        P2_posY = PADDLE_Y

    pygame.display.update()
    FPSCLOCK.tick(FPS)
