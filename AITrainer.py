import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("squat1.mp4")
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
angle = 270

while True:
    success, img = cap.read()
    img = cv2.resize(img, (int(width/2), int(height/2)))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        detector.findAngle(img, 11, 23, 25)          # Left Hip
        detector.findAngle(img, 12, 24, 26)          # Right Hip

        detector.findAngle(img, 11, 13, 15)          # Left Arm
        detector.findAngle(img, 12, 14, 16)          # Right Arm

        detector.findAngle(img, 23, 11, 13)                         # Left Shoulder
        detector.findAngle(img, 24, 12, 14)                         # Right Shoulder 
        #detector.findAngle(img, 11, 12, 24, draw_angle=0)          # Upper MID
        #detector.findAngle(img, 24, 23, 11, draw_angle=0)          # Lower MID

        angle2 = detector.findAngle(img, 24, 26, 28)                         # Left Knee
        angle1 = detector.findAngle(img, 23, 25, 27)                         # Right Knee
        angle = (angle1+angle2)/2

        detector.findAngle(img, 25, 27, 31)                         # Left Heel
        detector.findAngle(img, 27, 29, 31, draw_angle=0)           # Left Foot
        detector.findAngle(img, 26, 28, 32)                         # Right Heel
        detector.findAngle(img, 28, 30, 32, draw_angle=0)           # Right Foot

        detector.findAngle(img, 14, 16, 18, draw_angle=0)          ## Right Hand
        detector.findAngle(img, 14, 16, 20, draw_angle=0)          ## Right Hand
        detector.findAngle(img, 14, 16, 22, draw_angle=0)          ## Right Hand
        detector.findAngle(img, 13, 15, 17, draw_angle=0)          ## Left Hand
        detector.findAngle(img, 13, 15, 19, draw_angle=0)          ## Left Hand
        detector.findAngle(img, 13, 15, 21, draw_angle=0)          ## Left Hand

        mid = int(height/2)
        per = np.interp(angle, (60, 170), (0, 100))
        bar = np.interp(angle, (60, 170), (mid + 130, mid - 130))

        # Check for the dumbbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        # Draw Bar
        
        cv2.rectangle(img, (int(width - 100), int(mid + 130)), (int(width - 50), int(mid - 130)), color, 3)
        cv2.rectangle(img, (int(width - 100), int(bar)), (int(width - 50), mid + 130), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (int(width - 170), mid - 145), cv2.FONT_HERSHEY_PLAIN, 4,color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)