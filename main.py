import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
import random


cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=2)


timer = 0
stateResult = False
gameOver = False
startGame = False
scores = [0, 0] 
roundNum = 0
totalRounds = 5
initialTime = 0
countDown = 3 
lastMoveTime = 0
moveDisplayDuration = 2  
playerMove = None
randomNumber = 0


def draw_text(img, text, position, font_scale, color, thickness):
    cv.putText(img, text, position, cv.FONT_HERSHEY_PLAIN, font_scale, color, thickness)

def determine_winner(player_score, ai_score):
    if player_score > ai_score:
        return "PLAYER WINS THE GAME!"
    elif ai_score > player_score:
        return "AI WINS THE GAME!"
    else:
        return "IT'S A TIE!"

def detect_player_move(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return 1 
    elif fingers == [1, 1, 1, 1, 1]:
        return 2  
    elif fingers == [0, 1, 1, 0, 0]:
        return 3  
    return None

while True:

    imgBG = cv.imread('Resources/BG.png')
    success, img = cap.read()
    
    if not success:
        print("Failed to capture from webcam")
        break


    imgScaled = cv.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]
    

    hands, img = detector.findHands(imgScaled)


    if not gameOver:
        draw_text(imgBG, f"ROUND: {roundNum}/{totalRounds}", (530, 150), 2, (0, 0, 0), 2)
    

    if startGame and not gameOver:
        if not stateResult:
            currentTime = time.time()
            timer = currentTime - initialTime
            

            countdown_value = countDown - int(timer)
            if countdown_value > 0:
                draw_text(imgBG, str(countdown_value), (605, 435), 6, (255, 0, 255), 4)
            

            if timer > countDown:
                stateResult = True
                roundNum += 1
                lastMoveTime = time.time()
                

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    playerMove = detect_player_move(fingers)
                    

                    randomNumber = random.randint(1, 3)
                    imgAI = cv.imread(f'Resources/{randomNumber}.png', cv.IMREAD_UNCHANGED)
                    

                    if playerMove:
                        if (playerMove == 1 and randomNumber == 3) or \
                           (playerMove == 2 and randomNumber == 1) or \
                           (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1 
                            roundResult = "You Win!"
                        elif (playerMove == 3 and randomNumber == 1) or \
                             (playerMove == 1 and randomNumber == 2) or \
                             (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1 
                            roundResult = "AI Wins!"
                        else:
                            roundResult = "Tie!"
                    else:
                        randomNumber = 0 
                        roundResult = "No move detected!"
                else:
                    randomNumber = 0
                    roundResult = "No hand detected!"
                

                if roundNum >= totalRounds:
                    gameOver = True
    

    imgBG[234:654, 795:1195] = imgScaled
    

    if stateResult and randomNumber > 0:
        imgAI = cv.imread(f'Resources/{randomNumber}.png', cv.IMREAD_UNCHANGED)
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
        

        if time.time() - lastMoveTime < moveDisplayDuration:
            draw_text(imgBG, roundResult, (530, 500), 3, (0, 255, 0), 3)
        else:

            if not gameOver:
                stateResult = False
                initialTime = time.time()
    

    draw_text(imgBG, str(scores[0]), (410, 215), 4, (255, 255, 255), 6)
    draw_text(imgBG, str(scores[1]), (1112, 215), 4, (255, 255, 255), 6)
    

    if gameOver:

        overlay = imgBG.copy()
        cv.rectangle(overlay, (0, 0), (1400, 800), (0, 0, 0), -1)
        imgBG = cv.addWeighted(overlay, 0.7, imgBG, 0.3, 0)

        winner_text = determine_winner(scores[1], scores[0])
        draw_text(imgBG, winner_text, (400, 400), 3, (0, 255, 255), 4)
        draw_text(imgBG, f"Final Score: AI {scores[0]} - Player {scores[1]}", (450, 480), 2, (255, 255, 255), 2)
        draw_text(imgBG, "Press 'r' to restart game", (500, 550), 2, (255, 255, 255), 2)
    

    if not startGame:
        overlay = imgBG.copy()
        cv.rectangle(overlay, (0, 0), (1400, 800), (0, 0, 0), -1)
        imgBG = cv.addWeighted(overlay, 0.7, imgBG, 0.3, 0)
        draw_text(imgBG, "Press 's' to start the game", (400, 400), 2, (0, 0, 0), 2)
    
    cv.imshow('Rock Paper Scissors', imgBG)
    

    key = cv.waitKey(1)
    if key == ord('s') and not startGame:
        startGame = True
        initialTime = time.time()
        stateResult = False
        roundNum = 0
        scores = [0, 0]
    elif key == ord('r') and gameOver:
        gameOver = False
        startGame = False
        scores = [0, 0]
        roundNum = 0
    elif key == 27: 
        break

cap.release()
cv.destroyAllWindows()