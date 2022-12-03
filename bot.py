from time import sleep
import pyautogui
import random
import cv2
from tile import Tile
import math
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_board():
    squares = driver.find_elements(By.CLASS_NAME, "square")
    board = {}
    for i in squares:
        element = i
        type = i.get_attribute('class')
        name = i.get_attribute('id')
        tile = Tile(type, name, element)
        board[name] = tile
        
    return board

def designate_neighbors(board):
    for i in board:
        tile = board.get(i)
        i.neighbors = [topleft, topmiddle, topright, middleleft, middleright, bottomleft, bottommiddle, bottomright]

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

driver = webdriver.Firefox()
driver.get("https://minesweeperonline.com/")


pyautogui.moveTo(5,5)
sleep(5)

board = get_board()
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

