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
    elif (landmarks[8].y < landmarks[5].y) and (landmarks[12].y < landmarks[9].y) and all(
            [landmarks[i].y < landmarks[i + 3].y for i in range(13, 18, 4)]):
        return "scissors"
    elif all([landmarks[i].y > landmarks[i + 3].y for i in range(5, 18, 4)]):
        return "paper"
    else:
        return "-1"


while True:
    ret, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    img = cv2.flip(img, 1)
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
                x1 = hls[1].landmark[0].x
                x2 = hls[0].landmark[0].x

                if x1 < x2:
                    p1_move = findHandMoves(hls[0])
                    p2_move = findHandMoves(hls[1])
                else:
                    p1_move = findHandMoves(hls[1])
                    p2_move = findHandMoves(hls[0])

            else:
                success = False
        else:
            success = False
    elif clock < 100:
        if (success and p1_move != "-1" and p2_move != "-1"):
            gameText = f"        {p1_move}             {p2_move}"
            if p1_move == p2_move:
                winner = "Game is tied"
            elif p1_move == "paper" and p2_move == "rock":
                winner = "player 1 wins"
            elif p1_move == "rock" and p2_move == "scissors":
                winner = "player 1 wins"
            elif p1_move == "scissors" and p2_move == "paper":
                winner = "player 1 wins"
            else:
                winner = "player 2 wins"
        else:
            winner = ""
            gameText = "didn't play properly"
    if not ret:
        break
    cv2.line(img, (320, 0), (320, 470), (0, 0, 255), 3, cv2.LINE_AA)
    cv2.putText(img, f"player 1        player 2", (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv2.LINE_AA)
    if winner == "player 1 wins":
        cv2.putText(img, "Winner", (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2, cv2.LINE_AA)
    elif winner == "player 2 wins":
        cv2.putText(img, "Winner", (400, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2, cv2.LINE_AA)
    # elif winner == "Game is tied":
    #     cv2.putText(img, "Winner", (50, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2, cv2.LINE_AA)
    #     cv2.putText(img, "Winner", (400, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2, cv2.LINE_AA)

    # cv2.putText(img, f"clock : {clock}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, gameText, (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (150, 30, 255), 2, cv2.LINE_AA)
    cv2.putText(img, winner, (50, 130), cv2.FONT_HERSHEY_PLAIN, 2, (150, 30, 255), 2, cv2.LINE_AA)
    clock = (clock + 1) % 100
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
