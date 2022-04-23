from curses import KEY_ENTER, window
from fractions import Fraction
from glob import glob
import sys
from tkinter import Y
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLineEdit,QTextBrowser,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QPalette,QBrush,QFont,QMouseEvent
from PyQt5.QtCore import Qt,QFileInfo
from math import sqrt,log
import numpy as np
from copy import deepcopy
from time import time


global totalTimer

totalTimer = 0

class node():
    def __init__(self,pos,parent,player) -> None:
        self.pos = pos
        self.parent = parent
        self.visit = 0
        self.score = 0
        self.children = np.array([],dtype=node)
        self.player = player

    def appendChild(self,pos,player):
        self.children = np.append(self.children,node(pos,self,player))
    
    def scoreAcu(self,score):
        self.score = self.score + score
    
    def sele(self):
        index = 0
        for ch in range(self.children.size):
            if self.children[ch].visit == 0: return self.children[ch]
            if self.ucb(ch) > self.ucb(index): index = ch
        return self.children[index]

    def ucb(self,ch):
        x1 = self.children[ch].score/self.children[ch].visit
        x2 = log(self.children[ch].visit)
        x3 = x2/self.children[ch].visit
        ans = x1 + sqrt(x3)
        return ans
            


class Game():
    def __init__(self) -> None:
        self.gameStatus = 0
        self.p1 = 0
        self.p2 = 0
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        
        self.set(1,3,3)
        self.set(1,4,4)
        self.set(-1,4,3)
        self.set(-1,3,4)

    def play(self,player:int,x:int,y:int) -> int:
        if self.reverse(player,x,y):
            self.set(player,x,y)
            return 1
        else:
            return 0

    def set(self,player:int,x:int,y:int):
        self.board[x][y] = player

    def reverse(self,player:int,x:int,y:int,istry:int = 0) ->int:
        res = 1
        if self.board[x][y] != 0:
            pass
        else:
            #down-side
            if y >= 6 or self.board[x][y+1] == player or self.board[x][y+1] == 0:
                pass
            else:
                for i in range(y+1,8):
                    if self.board[x][i] == player:
                        if istry == 0: 
                            for j in range(y+1,i):
                                self.board[x][j] = player
                        res = 0
                        break
            #up-side
            if y <= 1 or self.board[x][y-1] == player or self.board[x][y-1] == 0:
                pass
            else:
                for i in range(y-1,-1,-1):
                    if self.board[x][i] == player:
                        if istry == 0:
                            for j in range(y-1,i,-1):
                                self.board[x][j] = player
                        res = 0
                        break
            #left-side
            if x <= 1 or self.board[x-1][y] == player or self.board[x-1][y] == 0:
                pass
            else:
                for i in range(x-1,-1,-1):
                    if self.board[i][y] == player:
                        if istry == 0:
                            for j in range(x-1,i,-1):
                                self.board[j][y] = player
                        res = 0
                        break
            #right-side
            if x >= 6 or self.board[x+1][y] == player or self.board[x+1][y] == 0:
                pass
            else:
                for i in range(x+1,8):
                    if self.board[i][y] == player:
                        if istry == 0:
                            for j in range(x+1,i):
                                self.board[j][y] = player
                        res = 0
                        break
            #left-up-side
            if x <= 1 or y <= 1 or self.board[x-1][y-1] == player or self.board[x-1][y-1] == 0:
                pass
            else:
                d = 1
                while x - d >= 0 and y - d >= 0:
                    if self.board[x - d][y - d] == player:
                        if istry == 0:
                            for i in range(1,d):
                                self.board[x-i][y-i] = player
                        res = 0
                        break
                    d = d + 1
            #left-down-side
            if x <= 1 or y >= 6  or self.board[x-1][y+1] == player or self.board[x-1][y+1] == 0:
                pass
            else:
                d = 1
                while x - d >= 0 and y + d <= 7:
                    if self.board[x - d][y + d] == player:
                        if istry == 0:
                            for i in range(1,d):
                                self.board[x-i][y+i] = player
                        res = 0
                        break
                    d = d + 1
            #right-up-side
            if x >= 6 or y <= 1 or self.board[x+1][y-1] == player or self.board[x+1][y-1] == 0:
                pass
            else:
                d = 1
                while x + d <= 7 and y - d >= 0:
                    if self.board[x + d][y - d] == player:
                        if istry == 0:
                            for i in range(1,d):
                                self.board[x+i][y-i] = player
                        res = 0
                        break
                    d = d + 1
            #right-down-side
            if x >= 6 or y >= 6 or self.board[x+1][y+1] == player or self.board[x+1][y+1] == 0:
                pass
            else:
                d = 1
                while x + d <= 7 and y + d <= 7:
                    if self.board[x + d][y + d] == player:
                        if istry == 0:
                            for i in range(1,d):
                                self.board[x+i][y+i] = player
                        res = 0
                        break
                    d = d + 1
        if res == 0 and istry == 0:
            self.set(player,x,y)
            for i in range(0,8):
                for j in range(0,8):
                    if self.board[i][j] == 1: self.p1 = self.p1 + 1
                    if self.board[i][j] == -1: self.p2 = self.p2 + 1
        return res
    
    def passTest(self,player:int) ->int:
        for i in range(0,8):
            for j in range(0,8):
                if self.reverse(player,i,j,1) == 0:
                    return 1
        return 0

    def settle(self) ->int :
        if(self.p1>self.p2):
            return 1
        elif(self.p2>self.p1):
            return -1
        else:
            return 0

    def aiPlay(self,player:int,iter:int = 10000):
        root = node(np.array([-1,-1],dtype=np.uint8),node(np.array([-2,-2],dtype=np.uint8),[],0),player)
        for x in range(0,8):
            for y in range(0,8):
                if self.reverse(player,x,y,1) == 0:
                    root.appendChild(np.array([x,y]),-player)
        for i in range(0,iter): self.mcSearch(root,player)

        x,y = root.sele().pos

        self.reverse(player,x,y)
        self.set(player,x,y)

    # 对每次模拟都进行计时，在模拟强度较大时不用        
    # def timer(func):
    #     def func_wrapper(*args,**kwargs):
    #         time_start = time()
    #         result = func(*args,**kwargs)
    #         time_end = time()
    #         time_spend = time_end - time_start
    #         print("-Simulate once cost {0}s".format(time_spend))
    #         return result
    #     return func_wrapper
    # @timer
    def mcSearch(self,root:node,player):
        ptr = root
        sit = deepcopy(self)
        nowP = player
        while 1:
            if ptr.children.size == 0:
                for x in range(0,8):
                    for y in range(0,8):
                        if sit.reverse(nowP,x,y,1) == 0:
                            ptr.appendChild(np.array([x,y]),-nowP)
            if ptr.children.size == 0:
                nowP = -nowP
                continue
            ptr = ptr.sele()
            x, y = ptr.pos
            sit.reverse(nowP,x,y)
            sit.set(nowP,x,y)
            ptr.visit = ptr.visit + 1
            if sit.passTest(1) == 0 and sit.passTest(-1) == 0: break
            nowP = -nowP

        winner = sit.settle()

        while 1:
            ptr.scoreAcu(ptr.player==winner)
            if ptr.pos[0] >= 10: break
            ptr = ptr.parent


# Player 1,-1 --- Turnflag 0,1


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()
        self.boardCh = [[QLabel(self) for _ in range(8)] for _ in range(8)]

    def initUI(self):
        self.resize(1920,1080)
        self.move(100,100)
        self.setWindowTitle("Reversi")
        root_O = QFileInfo(__file__).absolutePath()
        root = ""
        for i in root_O:
            if(i == "\\"):
                root = root + "/"
            else:
                root = root + i
        self.setWindowIcon(QIcon(root + './assets/icon.png'))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./assets/gameboard.png")))
        self.setPalette(palette)

        self.cmdInput = QLineEdit(self)
        self.cmdInput.move(1099,1020)
        self.cmdInput.resize(807,39)
        self.cmdInput.setFont(QFont("Arial",15))

        self.echoOut = QTextBrowser(self)
        self.echoOut.setGeometry(1099,234,807,767)

        self.startButton = QPushButton(self)
        self.startButton.setDefault(True)
        self.startButton.setText("START/RESET")
        self.startButton.clicked.connect(lambda: self.buttonEvent(1))
        self.startButton.setGeometry(1099,40,350,150)

        self.AiButton = QPushButton(self)
        self.AiButton.setDefault(True)
        self.AiButton.setText("AI Step")
        self.AiButton.clicked.connect(lambda: self.buttonEvent(2))
        self.AiButton.setGeometry(1549,40,350,150)

        self.turnFlag = 0
        self.gameFlag = 0

    def timer(func):
        def func_wrapper(*args,**kwargs):
            global totalTimer
            time_start = time()
            result = func(*args,**kwargs)
            time_end = time()
            time_spend = time_end - time_start            
            totalTimer = totalTimer + time_spend            
            print("{0} func cost {1:.3f}s, totally {2:.3f}s".format(func.__name__,time_spend,totalTimer))
            return result
        return func_wrapper

    @timer
    def buttonEvent(self,btnid):
        global totalTimer
        if btnid == 1:
            self.startGame()
            totalTimer = 0
        elif btnid == 2:
           self.game.aiPlay(self.turnFlag)
           self.turn()
        if self.gameFlag: self.boardUpdate()

    def keyPressEvent(self, e):
        if self.cmdInput.text().__len__() and (e.key() ==  Qt.Key_Enter or Qt.Key_Return):
            cmdArgs = self.cmdInput.text().split()
            if cmdArgs[0] == "Debug":
                self.echoOut.append("Debug")
            elif cmdArgs[0] == "Start": self.startGame()
            elif cmdArgs[0] == "Set" and len(cmdArgs) >= 3 and int(cmdArgs[1]) <= 8 and int(cmdArgs[2]) <= 8 and int(cmdArgs[1]) > 0 and int(cmdArgs[2]) > 0:
                if self.gameFlag:
                    self.game.set(self.turnFlag,int(cmdArgs[1])-1,int(cmdArgs[2])-1)
            elif cmdArgs[0] == "ai":
                self.game.aiPlay(self.turnFlag)
                self.turn()
            else:
                self.echoOut.append("<Player " + (self.turnFlag).__str__() +  ">: "+self.cmdInput.text())
            if self.gameFlag: self.boardUpdate()
            self.cmdInput.clear()

    def startGame(self):
        self.game = Game()
        self.gameFlag = 1   
        self.turnFlag = 1
    
    def turn(self):
        self.boardUpdate()
        self.turnFlag = -self.turnFlag
        if self.game.passTest(self.turnFlag) == 0:
            self.echoOut.append("Player " + (self.turnFlag).__str__() + " pass this turn.")
            self.turnFlag = -self.turnFlag
            if self.game.passTest(self.turnFlag) == 0:
                gameResult = self.game.settle()
                if gameResult == 0:
                    self.echoOut.append("Game is drawn")
                else: self.echoOut.append("Player " + gameResult.__str__() + " won this game.")  

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.gameFlag == 0: return super().mousePressEvent(a0)
        Xpos = (a0.x()/135).__int__()
        Ypos = (a0.y()/135).__int__()
        if Xpos < 8 and Ypos < 8: 
            state = self.game.reverse(self.turnFlag,Xpos,Ypos)
        else: state = 2
        if state == 0:
            self.echoOut.append("Player " + (self.turnFlag).__str__() + " put a chessman at (" + Xpos.__str__() + "," + Ypos.__str__() + ").")
            self.turn()
        elif state == 1:
            self.echoOut.append("Invalid operation!")
        elif state == 2:
            pass
        return super().mousePressEvent(a0)

    def boardUpdate(self):
        for x in range(8):  #Warning! Hard code here
            for y in range(8):
                if self.game.board[x][y] == 0:
                    self.boardCh[x][y].setPixmap(QPixmap())
                elif self.game.board[x][y] == 1:
                    self.boardCh[x][y].setPixmap(QPixmap('./assets/chBlack.png'))
                    self.boardCh[x][y].setGeometry(135*x+7,135*y+7,120,120)
                elif self.game.board[x][y] == -1:
                    self.boardCh[x][y].setPixmap(QPixmap('./assets/chWhite.png'))
                    self.boardCh[x][y].setGeometry(135*x+7,135*y+7,120,120)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    

    windows = MainWindow()

    windows.show()
    sys.exit(app.exec_())