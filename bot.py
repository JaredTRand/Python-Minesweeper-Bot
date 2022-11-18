from time import sleep
from python_imagesearch.imagesearch import imagesearch
import pyautogui
import webbrowser
import random
import cv2
from tile import Tile
import math
import keyboard

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
    for tile in pyautogui.locateAllOnScreen("img/1.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for x in board:
            for y in x:
                if y.position == pos:
                    y.type = "1"

    for tile in pyautogui.locateAllOnScreen("img/2.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for x in board:
            for y in x:
                if y.position == pos:
                    y.type = "2"
    
    for tile in pyautogui.locateAllOnScreen("img/3.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for x in board:
            for y in x:
                if y.position == pos:
                    y.type = "3"

    for tile in pyautogui.locateAllOnScreen("img/4.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for x in board:
            for y in x:
                if y.position == pos:
                    y.type = "4"
    
    for tile in pyautogui.locateAllOnScreen("img/blank.jpg", confidence=.80, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for x in board:
            for y in x:
                if y.position == pos:
                    y.type = "Blank"
                
    for tile in pyautogui.locateAllOnScreen("img/flag.jpg", confidence=.90, grayscale=False):
        pos = tile.left+math.floor(tile.width/2), tile.top+math.floor(tile.height/2)
        for x in board:
            for y in x:
                if y.position == pos:
                    y.type = "Flag"

def left_click(tile):
    pyautogui.click(tile.position)

def right_click(tile):
    pyautogui.rightClick(tile.position)

def flag(board):
    for i in board:
        for j in i:
            if j.type is ("1" or "2" or "3" or "4"):
                if len(j.neighbor_blanks())+len(j.neighbor_flags()) == int(j.type):
                    for k in j.neighbor_blanks():
                        right_click(k)
                        k.type = "Flag"

def click_blanks_after_flags(board):
    for i in board:
        moved = False
        for j in i:                  
            if j.type is ("1" or "2" or "3" or "4"):
                if len(j.neighbor_flags()) == int(j.type):
                    for k in j.neighbor_blanks():
                        left_click(k)
                        moved = True
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

while(1):
    moved = False
    refresh(board)
    flag(board)
    refresh(board)
    moved = click_blanks_after_flags(board)

    if not moved:
        for i in board:
            for j in i:
                if j.type == "Unclicked":
                    left_click(j)
                    break
            else: 
                continue
            break
                

    






