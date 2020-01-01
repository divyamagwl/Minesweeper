import pygame
import random
import time

RED = (239,56,0)
BLUE = (0,0,173)
BLACK = (0,0,0)
LIGHTGREEN = (167,218,73)
DARKGREEN = (142,204,57)
LAWNGREEN = (124,252,0)
LIGHTBLUE = (74,192,251)
SAND = (219,185,138)
YELLOW = (245,193,13)
PURPLE = (180,56,231)
BROWN = (129,79,76)

screen_size_x = 700
screen_size_y = 800

LEFT = 1
RIGHT = 3  

MENU = -1
INSTRUCTIONS = -2
PLAY = 0
WIN = 1
LOSE = 2

EASY = 1
MEDIUM = 2
HARD = 3

pygame.init()

screen = pygame.display.set_mode((screen_size_x,screen_size_y))

pygame.display.set_caption("MineSweeper")
icon = pygame.image.load("images/golf.png")
pygame.display.set_icon(icon)

font = pygame.font.Font("freesansbold.ttf",32)

level = EASY

gameResult = MENU

(mouse_x,mouse_y) = (0,0)

mouse_click = -1


class Button():
    def clickedIn(self,x,y,width,height):
        global mouse_click, mouse_x, mouse_y
        if mouse_click == LEFT:
            if (x <= mouse_x <= (x + width)) and (y <= mouse_y <= (y + height)):
                return True

    def hovering(self,x,y,width,height):
        global mouse_click, mouse_x, mouse_y
        if mouse_click == 0:
            if (x <= mouse_x <= (x + width)) and (y <= mouse_y <= (y + height)):
                return True
    
    def clickButton(self,x,y,width,height,color,hoverColor,textFont,text,textColor):
        if not self.clickedIn(x,y,width,height) and not self.hovering(x,y,width,height):
            pygame.draw.rect(screen,color,(x,y,width,height))
        elif self.hovering(x,y,width,height):
            pygame.draw.rect(screen,hoverColor,(x,y,width,height))
            
        buttonText = textFont.render(text,True,textColor)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText,((x + width/2 - buttonText_x/2),(y + height/2 - buttonText_y/2)))

        if self.clickedIn(x,y,width,height):
            return True

button = Button()

def mainMenu():
    global gameResult, level, game
    screen.fill(LIGHTBLUE)
    background = pygame.image.load("images/bg.png")
    screen.blit(background, (0,566))

    bird1 = pygame.image.load("images/bird.png")
    
    screen.blit(bird1,(540,460))

    bird2 = pygame.image.load("images/birdrev.png")
    screen.blit(bird2,(100,280))

    heading = pygame.font.Font("fonts/Christopher Done.ttf",80)
    font = pygame.font.Font("fonts/KGSecondChancesSketch.ttf",38)

    text = heading.render("Mine",True,YELLOW)
    screen.blit(text,(124,80))
    text = heading.render("Sweeper",True,PURPLE)
    screen.blit(text,(300,80))

    if button.clickButton(250,220,200,80,YELLOW,PURPLE,font,"EASY",BLACK):
        level = EASY
        game = Game(8,8,6)
        gameResult = PLAY
    if button.clickButton(250,320,200,80,YELLOW,PURPLE,font,"MEDIUM",BLACK):
        level = MEDIUM
        game = Game(10,10,12)
        gameResult = PLAY
    if button.clickButton(250,420,200,80,YELLOW,PURPLE,font,"HARD",BLACK):
        level = HARD
        game = Game(13,13,18)
        gameResult = PLAY
    if button.clickButton(200,520,300,80,YELLOW,PURPLE,font,"INSTRUCTIONS",BLACK):
        gameResult = INSTRUCTIONS

def gameDetails():
    global gameResult,game

    pygame.draw.rect(screen,(0,150,0),(0,0,screen_size_x,100))
    font = pygame.font.Font("fonts/KGSecondChancesSketch.ttf",32)

    if gameResult == LOSE:
        lostfont = pygame.font.Font("fonts/INFECTED.ttf",70)
        text = lostfont.render("You Lost",True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((350 - (text_x / 2)),(50 - (text_y / 2))))
    elif gameResult == WIN:
        wonfont = pygame.font.Font("fonts/KeeponTruckin.ttf",55)
        text = wonfont.render("You Won",True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((350 - (text_x / 2)),(50 - (text_y / 2))))
    elif gameResult == PLAY:
        detailsfont = pygame.font.Font("fonts/Shourtcut.ttf",32)
        text = detailsfont.render("MINES- " + str(game.num_mines),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((200 - (text_x / 2)),(50 - (text_y / 2))))
        text = detailsfont.render("FLAGS- " + str(game.num_flag),True,BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text,((410 - (text_x / 2)),(50 - (text_y / 2))))

    if gameResult == PLAY:
        if button.clickButton(540,22,130,50,YELLOW,SAND,font,"RESET",BLACK):
            gameResult = MENU
    elif gameResult == LOSE:
        if button.clickButton(540,22,130,50,RED,SAND,font,"RESET",BLACK):
            gameResult = MENU
    elif gameResult == WIN:
        if button.clickButton(540,22,130,50,LIGHTGREEN,SAND,font,"RESET",BLACK):
            gameResult = MENU

def instructions():
    global gameResult
    heading = pygame.font.Font("fonts/Christopher Done.ttf",80)
    text = heading.render("Instructions",True,(0,0,80))
    text_x = text.get_rect().width
    text_y = text.get_rect().height
    screen.blit(text,((350 - text_x/2),(80 - text_y/2)))

    font = pygame.font.Font("fonts/coolvetica rg.ttf",33)

    multitext = [["You are presented with a board of squares. Some", 
                "squares contain mines (holes), others don't."],
                ["If you click on a square containing a mine,you lose.",
                "If you manage to click all the squares (without",
                "clicking on any mine) you win."],
                ["Clicking a square which doesn't have a mine",
                "reveals the no. of neighbouring squares containing",
                "mines. Use this information plus some guess work",
                "to avoid the mines."],
                ["To open a square, point at the square and click on", 
                "it. To mark a square you think is a mine, point and",
                "right-click."]]
            
    for i in range(len(multitext)):
        for j in range(len(multitext[i])):
            text = font.render(multitext[i][j],True,(0,51,102))
            text_y = text.get_rect().height
            if len(multitext[i-1]) == 2:
                screen.blit(text,((5),(170 - text_y/2 + 100*i + 40*j)))
            elif len(multitext[i-1]) == 4:
                screen.blit(text,((5),(170 - text_y/2 + 140*i + 40*j)))
            else:
                screen.blit(text,((5),(170 - text_y/2 + 120*i + 40*j)))

    if button.clickButton(280,710,140,60,YELLOW,PURPLE,font,"BACK",BLACK):
        gameResult = MENU

class Tile():
    def __init__(self, x, y, columns, rows):
        self.columns = columns
        self.rows = rows
        self.cell_width = (screen_size_x / self.columns)
        self.cell_height = ((screen_size_y-100)/self.rows)
        self.x = x * self.cell_width
        self.y = (y * self.cell_height) + 100
        self.mine = False
        self.neighbours = 0
        self.visible = False
        self.flag = False

    def updateTile(self):
        global gameResult

        if gameResult == PLAY:
            if mouse_click == LEFT:
                if (self.x <= mouse_x <= (self.x + self.cell_width)) and (self.y <= mouse_y <= (self.y + self.cell_height)):
                    self.visible = True
                    self.flag = False
            
            elif mouse_click == RIGHT:
                if (self.x <= mouse_x <= (self.x + self.cell_width)) and (self.y <= mouse_y <= (self.y + self.cell_height)):
                    if self.flag == False:
                        self.flag = True
                    elif self.flag == True:
                        self.flag = False

            if self.visible == True and self.mine == True:
                gameResult = LOSE 

    def displayTile(self,alternate=0):

        if self.flag == True:
            pygame.draw.rect(screen,SAND,(self.x,self.y,self.cell_width,self.cell_height))
            if level == EASY:
                flagimg = pygame.image.load("images/flag64.png")
                screen.blit(flagimg,(self.x + self.cell_width/2 -32 , self.y + self.cell_height/2 -32)) 
            elif level == MEDIUM:
                flagimg = pygame.image.load("images/flag32.png")
                screen.blit(flagimg,(self.x + self.cell_width/2 -16 , self.y + self.cell_height/2 -16)) 
            elif level == HARD:
                flagimg = pygame.image.load("images/flag24.png")
                screen.blit(flagimg,(self.x + self.cell_width/2 -12 , self.y + self.cell_height/2 -12))

        if self.visible == True:
            if self.mine == False:
                pygame.draw.rect(screen, LAWNGREEN,(self.x,self.y,self.cell_width,self.cell_height))
                if self.neighbours > 0:
                    font = pygame.font.Font("freesansbold.ttf",40)
                    if self.neighbours == 1:
                        text_num = font.render(str(self.neighbours), True, BLUE)
                    elif self.neighbours == 2:
                        text_num = font.render(str(self.neighbours), True, BROWN)
                    elif self.neighbours == 3:
                        text_num = font.render(str(self.neighbours), True, RED)
                    else:
                        text_num = font.render(str(self.neighbours), True, PURPLE)
                    text_size_x = text_num.get_rect().width 
                    text_size_y = text_num.get_rect().height 
                    screen.blit(text_num, (self.x + (self.cell_width/2) - (text_size_x/2), self.y + (self.cell_height/2) - (text_size_y/2)))
            elif self.mine == True:
                pygame.draw.rect(screen, RED,(self.x,self.y,self.cell_width,self.cell_height))
                if level == EASY:
                    holeimg = pygame.image.load("images/hole64.png")
                    screen.blit(holeimg,(self.x + self.cell_width/2 -32 , self.y + self.cell_height/2 -32)) 
                elif level == MEDIUM:
                    holeimg = pygame.image.load("images/hole32.png")
                    screen.blit(holeimg,(self.x + self.cell_width/2 -16 , self.y + self.cell_height/2 -16)) 
                elif level == HARD:
                    holeimg = pygame.image.load("images/hole24.png")
                    screen.blit(holeimg,(self.x + self.cell_width/2 -12 , self.y + self.cell_height/2 -12))

        elif self.visible == False and self.flag == False:
            if alternate == 0:
                pygame.draw.rect(screen, LIGHTGREEN,(self.x,self.y,self.cell_width,self.cell_height))
            elif alternate == 1:
                pygame.draw.rect(screen, DARKGREEN,(self.x,self.y,self.cell_width,self.cell_height))

        if gameResult == WIN:
            if self.mine == True:
                if alternate == 0:
                    if level == EASY:
                        flowerimg = pygame.image.load("images/flower64.png")
                        screen.blit(flowerimg,(self.x + self.cell_width/2 -32 , self.y + self.cell_height/2 -32)) 
                    elif level == MEDIUM:
                        flowerimg = pygame.image.load("images/flower32.png")
                        screen.blit(flowerimg,(self.x + self.cell_width/2 -16 , self.y + self.cell_height/2 -16)) 
                    elif level == HARD:
                        flowerimg = pygame.image.load("images/flower24.png")
                        screen.blit(flowerimg,(self.x + self.cell_width/2 -12 , self.y + self.cell_height/2 -12))
                elif alternate == 1:
                    if level == EASY:
                        flowerimg = pygame.image.load("images/sunflower64.png")
                        screen.blit(flowerimg,(self.x + self.cell_width/2 -32 , self.y + self.cell_height/2 -32)) 
                    elif level == MEDIUM:
                        flowerimg = pygame.image.load("images/sunflower32.png")
                        screen.blit(flowerimg,(self.x + self.cell_width/2 -16 , self.y + self.cell_height/2 -16)) 
                    elif level == HARD:
                        flowerimg = pygame.image.load("images/sunflower24.png")
                        screen.blit(flowerimg,(self.x + self.cell_width/2 -12 , self.y + self.cell_height/2 -12))
            
        pygame.draw.rect(screen, (0,120,0),(self.x,self.y,self.cell_width,self.cell_height), 2)


class Game():
    def __init__(self, columns, rows, num_mines):
        self.columns = columns
        self.rows = rows
        self.num_mines = num_mines
        self.board = []
        self.mines = []
        self.mine_num = len(self.mines)
        self.num_neighb = 0
        self.num_flag = 0
        self.num_visible = 0

        for j in range(self.rows):
            self.board.append([])
            for i in range(self.columns):
                self.board[j].append(Tile(i,j,self.columns,self.rows))

        while self.mine_num < self.num_mines:
            self.mine_loc_x = random.randrange(self.rows)
            self.mine_loc_y = random.randrange(self.columns)
            
            if self.board[self.mine_loc_x][self.mine_loc_y].mine == False:
                self.mines.append([self.mine_loc_x, self.mine_loc_y])
                self.board[self.mine_loc_x][self.mine_loc_y].mine = True
            
            self.mine_num = len(self.mines)

        for i in range(self.rows):
            for j in range(self.columns):
                self.num_neighb = 0

                if j > 0:
                    if self.board[i][j-1].mine == True:
                        self.num_neighb += 1
                if i > 0:
                    if self.board[i-1][j].mine == True:
                        self.num_neighb += 1
                if i > 0 and j > 0:
                    if self.board[i-1][j-1].mine == True:
                        self.num_neighb += 1
                if j < (self.columns - 1):
                    if self.board[i][j+1].mine == True:
                        self.num_neighb += 1
                if i < (self.rows - 1):
                    if self.board[i+1][j].mine == True:
                        self.num_neighb += 1
                if j < (self.columns - 1) and i < (self.rows - 1):
                    if self.board[i+1][j+1].mine == True:
                        self.num_neighb += 1
                if i > 0 and j < (self.columns-1):
                    if self.board[i-1][j+1].mine == True:
                        self.num_neighb += 1
                if j > 0 and i < (self.rows-1):
                    if self.board[i+1][j-1].mine == True:
                        self.num_neighb += 1
                self.board[i][j].neighbours = self.num_neighb

    def update(self):
        global gameResult
        self.num_flag = 0
        self.num_visible = 0

        for i in range(self.rows):
            for j in range(self.columns):
                self.board[i][j].updateTile()

                if gameResult == PLAY:
                    if self.board[i][j].neighbours == 0 and self.board[i][j].visible == True:
                        if j > 0:
                            self.board[i][j-1].visible = True
                            self.board[i][j-1].flag = False
                        if i > 0:
                            self.board[i-1][j].visible = True
                            self.board[i-1][j].flag = False
                        if i > 0 and j > 0:
                            self.board[i-1][j-1].visible = True
                            self.board[i-1][j-1].flag = False
                        if j < (self.columns - 1):
                            self.board[i][j+1].visible = True
                            self.board[i][j+1].flag = False
                        if i < (self.rows - 1):
                            self.board[i+1][j].visible = True
                            self.board[i+1][j].flag = False
                        if j < (self.columns - 1) and i < (self.rows - 1):
                            self.board[i+1][j+1].visible = True
                            self.board[i+1][j+1].flag = False
                        if i > 0 and j < (self.columns - 1):
                            self.board[i-1][j+1].visible = True
                            self.board[i-1][j+1].flag = False
                        if j > 0 and i < (self.rows - 1):
                            self.board[i+1][j-1].visible = True
                            self.board[i+1][j-1].flag = False
                    if self.board[i][j].flag == True:
                        self.num_flag += 1
                    if self.board[i][j].visible == True:
                        self.num_visible += 1

        if gameResult == LOSE:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.board[i][j].visible = True
                    self.board[i][j].flag = False

        if self.num_visible == ((self.rows * self.columns) - self.num_mines):
            gameResult = WIN

            for i in range(self.rows):
                for j in range(self.columns):
                    self.board[i][j].flag = False

    def render(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if (i%2 == 0 and j%2 != 0) or (j%2 == 0 and i%2 != 0):
                    self.board[i][j].displayTile(0)
                else:
                    self.board[i][j].displayTile(1)

game = Game(0,0,0)

running = True
while running:

    screen.fill(LIGHTBLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_pos(mouse_x, mouse_y + 1)
            if event.button == 1:
                mouse_click = LEFT
            if event.button == 3:
                mouse_click = RIGHT
        else:
            mouse_click = 0

    (mouse_x,mouse_y) = pygame.mouse.get_pos()

    if gameResult == MENU:
        mainMenu()

    elif gameResult == INSTRUCTIONS:
        instructions()

    elif gameResult == PLAY or gameResult == WIN or gameResult == LOSE:
        gameDetails()
        game.update()
        game.render()

    pygame.display.update()
pygame.quit()