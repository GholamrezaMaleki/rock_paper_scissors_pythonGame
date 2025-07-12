import cv2
import mediapipe as mp
import time
import threading

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
clock = 0
winner = ""
p1_move = p2_move = None
gameText = ""

success = True


def findHandMoves(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i + 3].y for i in range(5, 18, 4)]):
        return "rock"
    elif landmarks[8].y < landmarks[5].y and landmarks[12] < landmarks[9] and all(
            [landmarks[i].y < landmarks[i + 3].y for i in range(13, 18, 4)]):
        return "scissors"
    elif all([landmarks[i].y > landmarks[i + 3].y for i in range(5, 18, 4)]):
        return "paper"
    else:
        return "not right shape"


while True:
    ret, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if 0 <= clock < 20:
        success = True
        gameText = "Are You Ready?"
    elif clock < 30:
        gameText = "3..."
    elif clock < 40:
        gameText = "2..."
    elif clock < 50:
        gameText = "1..."
    elif clock < 60:
        gameText = "Go!!"
    elif clock == 60:
        hls = results.multi_hand_landmarks
        if hls:
            if len(hls) == 2:
                print("two hands detected")
            else:
                success = False
    elif clock < 100:
        if (success):
            pass
        else:
            gameText = "didn't play properly"
    if not ret:
        break
    cv2.putText(img, f"clock : {clock}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, gameText, (50, 80), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2, cv2.LINE_AA)
    clock = (clock + 0.5) % 100
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
