from time import sleep
from python_imagesearch.imagesearch import imagesearch
import pyautogui
import webbrowser
import random
import cv2
from tile import Tile
import math
import keyboard

#doesnt get last line of squares
#doest quite get all neighbors to flag or click
#try selenium

class mylist (list):
    def __getitem__(self, n):
        if n < 0:
            raise IndexError("...")
        return list.__getitem__(self, n)

def get_board():
    row = mylist()
    board = mylist()
    leftSide = 0
    count = 0
    for tile in pyautogui.locateAllOnScreen("img/unclicked_square.jpg", confidence=.95):
        if(count == 0):
            leftSide = tile.left
        if(tile.left <= leftSide):
            board.append(row)
            row = mylist()
            count = 0
        
        pos = tile.left+(tile.width/2), tile.top+(tile.height/2)
        name = "Tile_{}_{}".format(len(board), count)
        newTile = Tile("Unclicked", pos, name)

        row.append(newTile)
        count += 1
    return board

def designate_neighbors(board):
    for i in board:
        rownum = board.index(i)
        for j in i:
            currentposition = i.index(j)

            try:
                topleft = board[rownum-1][currentposition-1]
            except IndexError:
                topleft = edge
            try:
                topmiddle = board[rownum-1][currentposition]
            except IndexError:
                topmiddle = edge
            try:
                topright = board[rownum-1][currentposition+1]
            except IndexError:
                topright = edge

            try:
                middleleft = i[currentposition-1]
            except IndexError:
                middleleft = edge
            try:
                middleright = i[currentposition+1]
            except IndexError:
                middleright = edge
            
            try:
                bottomleft = board[rownum+1][currentposition-1]
            except IndexError:
                bottomleft = edge
            try:
                bottommiddle = board[rownum+1][currentposition]
            except IndexError:
                bottommiddle = edge
            try:
                bottomright = board[rownum+1][currentposition+1]
            except IndexError:
                bottomright = edge
            
            j.neighbors = [topleft, topmiddle, topright, middleleft, middleright, bottomleft, bottommiddle, bottomright]

def refresh(board): 
    flatBoard = flatten(board)
    for tile in pyautogui.locateAllOnScreen("img/1.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            y.neighbor_flags()
            y.neighbor_blanks()
            if y.position == pos:
                y.type = "1"

    for tile in pyautogui.locateAllOnScreen("img/2.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            if y.position == pos:
                y.type = "2"
    
    for tile in pyautogui.locateAllOnScreen("img/3.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            if y.position == pos:
                y.type = "3"

    for tile in pyautogui.locateAllOnScreen("img/4.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            if y.position == pos:
                y.type = "4"
    
    for tile in pyautogui.locateAllOnScreen("img/5.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            if y.position == pos:
                y.type = "5"
    
    for tile in pyautogui.locateAllOnScreen("img/blank.jpg", confidence=.80, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            if y.position == pos:
                y.type = "Blank"
                
    for tile in pyautogui.locateAllOnScreen("img/flag.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for y in flatBoard:
            if y.position == pos:
                y.type = "Flag"

    if pyautogui.locateOnScreen("img/bomb.jpg", confidence=.90, grayscale=False) is not None:
        print("oops!")
        exit()

def left_click(tile):
    pyautogui.click(tile.position)

def right_click(tile):
    pyautogui.rightClick(tile.position)

def flatten(l):
    return [item for sublist in l for item in sublist]

def flag(board):    #if number of blanks+flags == tile number, flag || if number of blanks == tile number, flag
    flatBoard = flatten(board)
    for j in flatBoard:
        if j.type == ('1' or '2' or '3' or '4' or '5'):
            if (len(j.neighbor_blanks())+len(j.neighbor_flags()) == int(j.type)): 
                for k in j.neighbor_blanks():                                           
                    right_click(k)
                    k.type = "Flag"

def click_blanks_after_flags(board):
    moved = False
    flatBoard = flatten(board)
    for j in flatBoard:                  
        if j.type is ("1" or "2" or "3" or "4"):
            if len(j.neighbor_flags()) == int(j.type):
                for k in j.neighbor_blanks():
                    left_click(k)
                    moved = True
    if(moved):
        refresh(board)
        click_blanks_after_flags(board)
    refresh(board)
    return moved

webbrowser.open("https://minesweeperonline.com/", new = 0, autoraise = True)
pyautogui.moveTo(5,5)
sleep(5)

board = mylist(get_board())
edge = Tile("Edge", [5, 5], "Edge")
designate_neighbors(board)

corners =   [
            board[1][0], 
            board[len(board)-1][0],
            board[1][len(board[1])-1],
            board[len(board)-1][len(board[1])-1]
            ]
pyautogui.click(random.choice(corners).position) #click a random corner (supposedly best first move)

while(True):
    flag(board)
    click_blanks_after_flags(board)

    pyautogui.keyDown('alt')
    sleep(.2)
    pyautogui.press('tab')
    sleep(.2)
    pyautogui.keyUp('alt')
    sleep(1)

