import cv2
import socket
from time import sleep
from handController import HandTrackingModule as htm

def sendSocket(status):
    HOST = "192.168.1.78" # Esp Internal IP
    PORT = 9999 # Port Used

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        if status == True:
            s.sendall(b'1')
            sleep(0.05)
        
        if status == False:
            s.sendall(b'0')
            sleep(0.05)

def startHandTracking():
    
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(detectionCon=0.75)

    status = False

    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw = False)

        tipsIDs = [8, 12, 16, 20]
        firstTime = True
        lmList = detector.findPosition(img, draw = False)
        if len(lmList) != 0:
            fingers = []

            for id in range(0, 4):
                if lmList[tipsIDs[id]][2] < lmList[tipsIDs[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            
            if totalFingers == 4 and status == True:
                print("Enviar Request de Desligar")
                sendSocket(status)
                status = False
            elif totalFingers == 0 and status == False:
                print("Enviar Request para Ligar")
                sendSocket(status)
                status = True
            else:
                pass

        #sleep(1)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

def main():
    startHandTracking()    

if __name__ == "__main__":
    main()    

#Project by rafawastaken
