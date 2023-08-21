# chrome://dino/

import mss
import numpy as np
import cv2 as cv
import pyautogui as pag
import time

lookAheadDist = 350

screenshotViewport = {
    "top": 600,
    "left": 225,
    "width": 1000,
    "height": 100
}

high = np.array([190])
low = np.array([50])

runCount = 0

def getScreenshotHSV():
    with mss.mss() as sct:
        img = sct.grab(screenshotViewport)
        img = np.array(img)
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        return img
    
def startGame():
    pag.moveTo(x = screenshotViewport.get("left"), y = screenshotViewport.get("top"))
    pag.click()

def jump():
    pag.keyDown("up")
    time.sleep(0.1)
    pag.keyUp("up")

def isGameOver(mask):
    return mask[0,690] == 255 and mask[0,775] == 255 and mask[0,735] == 0
    
startGame()

while True:
    img = getScreenshotHSV()
    mask = cv.inRange(img, low, high)

    if np.any(mask[:, lookAheadDist - 250: lookAheadDist] == 255):
        jump()

    runCount += 1
    if runCount % 500 == 0:
        lookAheadDist += 50

    if isGameOver(mask) or cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
