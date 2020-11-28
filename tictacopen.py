from array import *
import pygame
import random
import timeit

pygame.init()
lev = 3
wincondition = 3
deplim = 5
starttime = 0
stoptime = 0

Xres = 1280
Yres = 720
borderwidth = int(Xres/20)
borderheight = int(Yres/20)
blockwidth = int((Xres-2*borderwidth)/lev)
blockheight = int((Yres-3*borderheight)/lev)
player = ['X', 'O']

win = pygame.display.set_mode((Xres, Yres))  # ,    pygame.FULLSCREEN)
pygame.display.set_caption("Tic Tac Toe")


class block():
    def __init__(self, x, y, width, height, val):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.val = val

    def reset(self, x, y, width, height, val):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.val = val

    def draw(self, win):
        font = pygame.font.SysFont('chiller', int(600/lev))
        text = font.render(self.val, 1, (255, 255, 255))
        win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                        self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos, val):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if self.val == '':
                    self.val = val
                    return True
                else:
                    return False

    def __str__(self):
        return self.val


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None, fontsize=25, text_font='chiller'):
        # Call this method to draw the button on the screen
        outline = (
            abs(self.color[0] - 255), abs(self.color[1] - 255), abs(self.color[2] - 255))
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                                            2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(text_font, fontsize)
            text = font.render(self.text.upper(), 1, (abs(
                self.color[0] - 255), abs(self.color[1] - 255), abs(self.color[2] - 255)))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.color = (0, 0, 0)
                return True

        self.color = (255, 255, 255)
        return False


class textblock():
    def __init__(self, posx, posy, width, height, placeholder='Input Box', text='', isactive=False):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.text = text
        self.isactive = isactive

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.posx and pos[0] < self.posx + self.width:
            if pos[1] > self.posy and pos[1] < self.posy + self.height:
                self.isactive = True
                return True

        self.isactive = False
        return False

    def draw(self, win, outline=(255, 255, 255), fontsize=25, text_font='chiller'):
        # Call this method to draw the button on the screen
        pygame.draw.rect(win, outline, (self.posx-5, self.posy -
                                        5, self.width+10, self.height+10), 0)
        pygame.draw.rect(win, (0, 0, 0), (self.posx-2, self.posy -
                                          2, self.width+4, self.height+4), 0)

        font = pygame.font.SysFont(text_font, fontsize)
        if self.isactive == False and self.text == '':
            text = font.render(self.placeholder, 1, (255, 255, 255))
        else:
            if self.isactive:
                text = font.render(self.text+'|', 1, (255, 255, 255))
            else:
                text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.posx + (self.width/2 - text.get_width()/2),
                        self.posy + (self.height/2 - text.get_height()/2)))

    def Addtext(self, input):
        self.text = input


blocks = [[block(borderwidth+(i*blockwidth), borderheight + (j*blockheight), blockwidth, blockheight, '')
           for i in range(lev)] for j in range(lev)]

menubutton = button((255, 255, 255), Xres/5, Yres -
                    Yres/20, Xres/5, Yres/40, 'MENU')
resetbutton = button((255, 255, 255), 3*Xres/5, Yres -
                     Yres/20, Xres/5, Yres/40, 'RESET')
startbutton = button((255, 255, 255), 3*Xres/5 + Xres/10, Yres/5 - Yres/10,
                     Xres/5, Yres/5, 'START GAME')
quitbutton = button((255, 255, 255), 3*Xres/5 + Xres/10, 3*Yres/5,
                    Xres/5, Yres/5, 'QUIT GAME')
minimaxbutton = button((255, 255, 255), Xres/20, Yres/5 + 2*Yres/10,
                       Xres/2, Yres/20, 'Basic Miximax')
abpruningbutton = button((255, 255, 255), Xres/20, Yres/5 + 3*Yres/10,
                         Xres/2, Yres/20, 'Alpha Beta Pruning')
depthlimbutton = button((255, 255, 255), Xres/20, Yres/5 + 4*Yres/10,
                        Xres/2, Yres/20, 'Minimax with Depth Limit')
dl_abpruningbutton = button((255, 255, 255), Xres/20, Yres/5 + 5*Yres/10,
                            Xres/2, Yres/20, 'Minimax with Depth Limit and Alpha Beta Pruning')
experimentalbutton = button((255, 255, 255), Xres/20, Yres/5 + 6*Yres/10,
                            Xres/2, Yres/20, 'Experimental Minimax')
levelinput = textblock(Xres/20, Yres/5 - Yres/10, Xres/3 + Xres/6, Yres /
                       20, "Enter Size of Grid,Default:3")
winconditioninp = textblock(Xres/20, Yres/5, Xres/3 + Xres/6, Yres /
                            20, "Winning Condition,Default:3")


def resetgame():
    global blockheight
    global blockwidth
    global blocks

    menubutton.color = (255, 255, 255)
    resetbutton.color = (255, 255, 255)
    startbutton.color = (255, 255, 255)
    quitbutton.color = (255, 255, 255)
    minimaxbutton.color = (255, 255, 255)
    abpruningbutton.color = (255, 255, 255)
    depthlimbutton.color = (255, 255, 255)
    dl_abpruningbutton.color = (255, 255, 255)
    experimentalbutton.color = (255, 255, 255)

    blockwidth = int((Xres-2*borderwidth)/lev)
    blockheight = int((Yres-3*borderheight)/lev)

    del blocks

    blocks = [[block(borderwidth+(i*blockwidth), borderheight + (j*blockheight), blockwidth, blockheight, '')
               for i in range(lev)] for j in range(lev)]


def drawelements(screen, winner='', errmsg=''):

    pygame.display.flip()
    win.fill((0, 0, 0))

    # for MENU screen
    if screen == 0:
        levelinput.draw(win)
        winconditioninp.draw(win)
        startbutton.draw(win, 60)
        quitbutton.draw(win, 60)

        font = pygame.font.SysFont('arial', 30)
        text = font.render(
            "CHOOSE PREFERRED ALGORITHM:(DEFAULT IS RANDOM MOVE)", 1, (255, 255, 255))
        win.blit(text, (Xres/20, Yres/5 + 1*Yres/10))

        minimaxbutton.draw(win)
        abpruningbutton.draw(win)
        depthlimbutton.draw(win)
        dl_abpruningbutton.draw(win)
        experimentalbutton.draw(win)

    # for GAME SCREEN
    elif screen == 1:
        flagw = blockwidth
        flagh = blockheight

        for i in range(lev-1):
            pygame.draw.line(win, (255, 255, 255), (flagw+borderwidth, borderheight),
                             (flagw+borderwidth, Yres-2*borderheight), 1)
            flagw += blockwidth
            pygame.draw.line(win, (255, 255, 255), (borderwidth, flagh+borderheight),
                             (Xres - borderwidth, flagh+borderheight), 1)
            flagh += blockheight

        for i in range(lev):
            for j in range(lev):
                blocks[i][j].draw(win)

        menubutton.draw(win)
        resetbutton.draw(win)
    # for CONGRATS SCREEN
    elif screen == 2:
        font = pygame.font.SysFont('chiller', 50)
        if winner == 'tie':
            text = font.render("THE MATCH IS A TIE", 1, (255, 255, 255))
            win.blit(text, (Xres/2-text.get_width() /
                            2, Yres/2-text.get_width()/2))
        if winner == 'X':
            text = font.render("X WINS THE MATCH!", 1, (255, 255, 255))
            win.blit(text, (Xres/2-text.get_width() /
                            2, Yres/2-text.get_width()/2))
        if winner == 'O':
            text = font.render("O WINS THE MATCH", 1, (255, 255, 255))
            win.blit(text, (Xres/2-text.get_width() /
                            2, Yres/2-text.get_width()/2))
        menubutton.draw(win)
        resetbutton.draw(win)
    elif screen == 3:
        font = pygame.font.SysFont('chiller', 50)
        text = font.render(errmsg, 1, (255, 255, 255))
        win.blit(text, (Xres/2-text.get_width() /
                        2, Yres/2-text.get_width()/2))

        menubutton.draw(win)
        resetbutton.draw(win)


def checkwinner():
    result = ''
    count = 1
    for i in range(lev):
        for j in range(lev-1):
            if blocks[i][j].val == blocks[i][j+1].val:
                result = blocks[i][j].val
                count += 1
            else:
                result = ''
                count = 1
            if result != '' and count == wincondition:
                return result
        count = 1

    for i in range(lev):
        for j in range(lev-1):
            if blocks[j][i].val == blocks[j+1][i].val:
                result = blocks[j][i].val
                count += 1
            else:
                result = ''
                count = 1
            if result != '' and count == wincondition:
                return result
        count = 1

    count = 1
    for i in range(lev-1):
        if blocks[i][i].val == blocks[i+1][i+1].val:
            result = blocks[i][i].val
            count += 1
        else:
            result = ''
            count = 1
        if result != '' and count == wincondition:
            return result

    count = 1
    for i in range(lev-1):
        if blocks[i][lev-i-1].val == blocks[i+1][lev-i-2].val:
            result = blocks[i][lev-i-1].val
            count += 1
        else:
            result = ''
            count = 1
        if result != '' and count == wincondition:
            return result

    for i in range(lev):
        for j in range(lev):
            if blocks[i][j].val == '':
                return ''

    return 'tie'


def randmove():

    count = 0
    for b in blocks:
        for c in b:
            if c.val == '':
                count += 1

    if count < 2:
        return

    if checkwinner == 'tie':
        return
    while True:
        i = random.randint(0, lev-1)
        j = random.randint(0, lev-1)

        if blocks[i][j].val == '':
            break

    blocks[i][j].val = 'O'


def exp_minimax(depth, isMaximizingPlayer, alpha, beta):

    if (timeit.default_timer() - starttime) > 5:
        start(screen=3)

    winner = checkwinner()

    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif winner == 'tie':
        return 0

    if depth > deplim:
        if(isMaximizingPlayer):
            return 1
        else:
            return -1

    if isMaximizingPlayer:
        bestVal = -100
        for b in blocks:
            for c in b:
                if c.val == '':
                    c.val = 'O'
                    value = exp_minimax(depth+1, False, alpha, beta)
                    c.val = ''
                    if(value == 1):
                        return 1
                    bestVal = max(bestVal, value)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
        return bestVal
    else:
        bestVal = 100
        for b in blocks:
            for c in b:
                if c.val == '':
                    c.val = 'X'
                    value = dl_abpruning(depth+1, True, alpha, beta)
                    c.val = ''
                    bestVal = min(bestVal, value)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        break
        return bestVal


def DepthLimit(depth, is_turn):

    if (timeit.default_timer() - starttime) > 5:
        start(screen=3)

    flag = checkwinner()
    if flag == 'X':
        return -1
    elif flag == 'O':
        return 1
    elif flag == 'tie':
        return 0

    if depth > deplim:
        if(is_turn):
            return 1
        else:
            return -1

    if(is_turn):
        bestscore = -2
        for i in range(lev):
            for j in range(lev):
                if(blocks[i][j].val == ''):
                    blocks[i][j].val = 'O'
                    score = DepthLimit(depth+1, False)
                    blocks[i][j].val = ''
                    if(score > bestscore):
                        bestscore = score
        return bestscore
    else:
        bestscore = 2
        for i in range(lev):
            for j in range(lev):
                if(blocks[i][j].val == ''):
                    blocks[i][j].val = 'X'
                    score = DepthLimit(depth+1, True)
                    blocks[i][j].val = ''
                    if(score < bestscore):
                        bestscore = score
        return bestscore


def dl_abpruning(depth, isMaximizingPlayer, alpha, beta):

    if (timeit.default_timer() - starttime) > 5:
        start(screen=3)

    winner = checkwinner()

    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif winner == 'tie':
        return 0

    if depth > deplim:
        if(isMaximizingPlayer):
            return 1
        else:
            return -1

    if isMaximizingPlayer:
        bestVal = -100
        for b in blocks:
            for c in b:
                if c.val == '':
                    c.val = 'O'
                    value = dl_abpruning(depth+1, False, alpha, beta)
                    c.val = ''
                    bestVal = max(bestVal, value)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
        return bestVal
    else:
        bestVal = 100
        for b in blocks:
            for c in b:
                if c.val == '':
                    c.val = 'X'
                    value = dl_abpruning(depth+1, True, alpha, beta)
                    c.val = ''
                    bestVal = min(bestVal, value)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        break
        return bestVal


def AlphaBetaPruning(depth, isMaximizingPlayer, alpha, beta):

    if (timeit.default_timer() - starttime) > 5:
        start(screen=3)

    winner = checkwinner()

    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif winner == 'tie':
        return 0

    if isMaximizingPlayer:
        bestVal = -100
        for b in blocks:
            for c in b:
                if c.val == '':
                    c.val = 'O'
                    value = AlphaBetaPruning(depth+1, False, alpha, beta)
                    c.val = ''
                    bestVal = max(bestVal, value)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
        return bestVal
    else:
        bestVal = 100
        for b in blocks:
            for c in b:
                if c.val == '':
                    c.val = 'X'
                    value = AlphaBetaPruning(depth+1, True, alpha, beta)
                    c.val = ''
                    bestVal = min(bestVal, value)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        break
        return bestVal


def minimax(depth, is_turn):  # simple Minimax2

    if (timeit.default_timer() - starttime) > 5:
        start(screen=3)

    flag = checkwinner()

    if flag == 'X':
        return -1
    elif flag == 'O':
        return 1
    elif flag == 'tie':
        return 0

    if(is_turn):
        bestscore = -100000
        for i in range(lev):
            for j in range(lev):
                if(blocks[i][j].val == ''):
                    blocks[i][j].val = 'O'
                    score = minimax(depth+1, False)
                    blocks[i][j].val = ''
                    # if(score == 1):
                    #     return 1
                    if(score > bestscore):
                        bestscore = score
        return bestscore
    else:
        bestscore = 100000
        for i in range(lev):
            for j in range(lev):
                if(blocks[i][j].val == ''):
                    blocks[i][j].val = 'X'
                    score = minimax(depth+1, True)
                    blocks[i][j].val = ''
                    # if(score == -1):
                    #     return -1
                    if(score < bestscore):
                        bestscore = score
        return bestscore


def AImove(choice):
    global blocks
    bestscore = -100000
    bestmove = (None, None)
    flag = 0

    flag1 = checkwinner()
    if flag1 == 'X':
        return -1
    elif flag1 == 'O':
        return 1
    elif flag1 == 'tie':
        return 0

    if choice == 0:
        print("using random Move")
        randmove()
    elif choice == 1:
        print("using basic minimax")
        for i in range(lev):
            for j in range(lev):
                if blocks[i][j].val == '':
                    blocks[i][j].val = 'O'
                    score = minimax(0, False)
                    blocks[i][j].val = ''
                    if score > bestscore:
                        bestscore = score
                        bestmove = (i, j)
        i = bestmove[0]
        j = bestmove[1]

        if i != None and j != None:
            blocks[i][j].val = 'O'
        else:
            drawelements(2, 'tie')
    elif choice == 2:
        print("using abpruning minimax")
        alpha = -100
        beta = +100
        for i in range(lev):
            for j in range(lev):
                if blocks[i][j].val == '':
                    blocks[i][j].val = 'O'
                    value = AlphaBetaPruning(1, False, alpha, beta)
                    blocks[i][j].val = ''
                    if value > bestscore:
                        bestscore = value
                        bestmove = (i, j)
                    alpha = max(alpha, bestscore)
                    if beta <= alpha:
                        break
        i = bestmove[0]
        j = bestmove[1]

        if i != None and j != None:
            blocks[i][j].val = 'O'
        else:
            drawelements(2, 'tie')
    elif choice == 3:
        print("using depth Limit")
        for i in range(lev):
            for j in range(lev):
                if blocks[i][j].val == '':
                    blocks[i][j].val = 'O'
                    score = DepthLimit(1, False)
                    blocks[i][j].val = ''
                    if score > bestscore:
                        bestscore = score
                        bestmove = (i, j)
        i = bestmove[0]
        j = bestmove[1]

        if i != None and j != None:
            blocks[i][j].val = 'O'
        else:
            drawelements(2, 'tie')
    elif choice == 4:
        print("using abpruning and depth limit minimax")
        alpha = -100
        beta = +100
        for i in range(lev):
            for j in range(lev):
                if blocks[i][j].val == '':
                    blocks[i][j].val = 'O'
                    value = dl_abpruning(1, False, alpha, beta)
                    blocks[i][j].val = ''
                    if value > bestscore:
                        bestscore = value
                        bestmove = (i, j)
                    alpha = max(alpha, bestscore)
                    if beta <= alpha:
                        break
        i = bestmove[0]
        j = bestmove[1]

        if i != None and j != None:
            blocks[i][j].val = 'O'
        else:
            drawelements(2, 'tie')
    elif choice == 5:
        print("using Experimental minimax")
        alpha = -100
        beta = +100
        for i in range(lev):
            for j in range(lev):
                if blocks[i][j].val == '':
                    blocks[i][j].val = 'O'
                    value = exp_minimax(1, False, alpha, beta)
                    blocks[i][j].val = ''
                    if value == 1:
                        blocks[i][j].val = 'O'
                        return
                    if value > bestscore:
                        bestscore = value
                        bestmove = (i, j)
                    alpha = max(alpha, bestscore)
                    if beta <= alpha:
                        break
        i = bestmove[0]
        j = bestmove[1]

        if i != None and j != None:
            blocks[i][j].val = 'O'
        else:
            drawelements(2, 'tie')


def start(screen=0):
    global lev
    global wincondition
    global starttime
    global stoptime
    choice = 0
    currplayer = 'X'
    winner = ''

    while True:
        if screen != 3:
            drawelements(screen, winner)
        else:
            drawelements(3, errmsg="Not feasible With this algorithm")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # for screen 0
                    if screen == 0:
                        if(winconditioninp.isOver(pos)):
                            pass
                        if(levelinput.isOver(pos)):
                            pass
                        if(startbutton.isOver(pos)):
                            screen = 1
                            if levelinput.text != '':
                                lev = int(levelinput.text)
                                levelinput.text = ''
                                levelinput.isactive = False
                            if winconditioninp.text != '':
                                wincondition = int(winconditioninp.text)
                                winconditioninp.text = ''
                                winconditioninp.isactive = False
                            resetgame()
                        if(quitbutton.isOver(pos)):
                            pygame.quit()
                        if(minimaxbutton.isOver(pos)):
                            choice = 1
                        if(abpruningbutton.isOver(pos)):
                            choice = 2
                        if(depthlimbutton.isOver(pos)):
                            choice = 3
                        if(dl_abpruningbutton.isOver(pos)):
                            choice = 4
                        if(experimentalbutton.isOver(pos)):
                            choice = 5
                    elif screen == 1:
                        if(menubutton.isOver(pos)):
                            resetgame()
                            screen = 0
                        if(resetbutton.isOver(pos)):
                            resetgame()
                        for i in range(lev):
                            for j in range(lev):
                                if blocks[i][j].isOver(pos, currplayer):
                                    if currplayer == 'X':
                                        currplayer = 'O'
                                    starttime = timeit.default_timer()
                                    AImove(choice)
                                    stoptime = timeit.default_timer()
                                    print('Time:', stoptime-starttime)
                                    currplayer = 'X'
                        winner = checkwinner()
                        if winner != '':
                            screen = 2
                    elif screen == 2:
                        if(menubutton.isOver(pos)):
                            resetgame()
                            screen = 0
                        if(resetbutton.isOver(pos)):
                            resetgame()
                            screen = 1
                    elif screen == 3:
                        if(menubutton.isOver(pos)):
                            resetgame()
                            screen = 0
                        if(resetbutton.isOver(pos)):
                            resetgame()
                elif event.type == pygame.KEYDOWN and levelinput.isactive == True:
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        levelinput.text = levelinput.text + '0'
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        levelinput.text = levelinput.text + '1'
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        levelinput.text = levelinput.text + '2'
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        levelinput.text = levelinput.text + '3'
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        levelinput.text = levelinput.text + '4'
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        levelinput.text = levelinput.text + '5'
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        levelinput.text = levelinput.text + '6'
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        levelinput.text = levelinput.text + '7'
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        levelinput.text = levelinput.text + '8'
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        levelinput.text = levelinput.text + '9'
                    if event.key == pygame.K_BACKSPACE:
                        levelinput.text = levelinput.text[:-1]
                    if event.key == pygame.K_RETURN:
                        screen = 1
                        if levelinput.text != '':
                            lev = int(levelinput.text)
                            levelinput.text = ''
                        resetgame()
                elif event.type == pygame.KEYDOWN and winconditioninp.isactive == True:
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        winconditioninp.text = winconditioninp.text + '0'
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        winconditioninp.text = winconditioninp.text + '1'
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        winconditioninp.text = winconditioninp.text + '2'
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        winconditioninp.text = winconditioninp.text + '3'
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        winconditioninp.text = winconditioninp.text + '4'
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        winconditioninp.text = winconditioninp.text + '5'
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        winconditioninp.text = winconditioninp.text + '6'
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        winconditioninp.text = winconditioninp.text + '7'
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        winconditioninp.text = winconditioninp.text + '8'
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        winconditioninp.text = winconditioninp.text + '9'
                    if event.key == pygame.K_BACKSPACE:
                        winconditioninp.text = winconditioninp.text[:-1]
                    if event.key == pygame.K_RETURN:
                        screen = 1
                        if winconditioninp.text != '':
                            wincondition = int(winconditioninp.text)
                            winconditioninp.text = ''
                        resetgame()


start()
