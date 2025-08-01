import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import socket
import time
import random



#Webcam
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=2)

timer=0
stateResult = False
startGame = False
scores = [0,0]



while True:
    imgBG = cv.imread('Resources/BG.png')
    success, img = cap.read()

    imgScaled = cv.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]
    
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv.putText(imgBG, str(int(timer)), (605, 435), cv.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3
                    
                    randomNumber = random.randint(1, 3)
                    imgAI = cv.imread(f'Resources/{randomNumber}.png', cv.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    imgBG[234:654,795:1195] = imgScaled
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv.putText(imgBG, str(scores[0]), (410, 215), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv.putText(imgBG, str(scores[1]), (1112, 215), cv.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv.imshow('BG', imgBG)
    key = cv.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False