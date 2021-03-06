import numpy as np
import cv2
import scipy
from scipy import ndimage
import datetime
import imutils
import time

# cap = cv2.VideoCapture('/home/sasidhy1/Desktop/eds_azzzist/SAMPLES/ambient.mp4')
# cap = cv2.VideoCapture('/home/sasidhy1/Desktop/eds_azzzist/SAMPLES/sleep.mp4')
# cap = cv2.VideoCapture('/home/sasidhy1/Desktop/eds_azzzist/SAMPLES/relax.mp4')
# cap = cv2.VideoCapture('/home/sasidhy1/Desktop/eds_azzzist/SAMPLES/study.mp4')
cap = cv2.VideoCapture('/home/sasidhy1/Desktop/eds_azzzist/SAMPLES/reading.mp4')

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi',fourcc, 25.0, (640,360))

start_time = time.time()

while(True):
    elapsed_time = time.time() - start_time
    elap = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    onset = time.time()

    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,360))
    


    roi = frame[70:360, 300:640]
    orig = roi.copy()

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)

    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(4,4))
    hist = clahe.apply(gray)
    blur = cv2.bilateralFilter(hist,9,75,75)
    edges = cv2.Canny(blur,200,220)

    status = "eyes closed"

    contours1 =  cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
    for c in contours1:
        if cv2.contourArea(c) > 9:
            status = "eyes OPEN"
            death = time.time()
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.drawContours(gray, [c], -1, 0, 2)
            cv2.circle(gray, (cX, cY), 7, 0, -1)

            contours2 =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
            for c in contours2:
                cv2.drawContours(roi, [c], -1, (255,255,255), -1)

    new = roi[cY:360-70, 0:640-360]

    cv2.putText(img = frame,
        text = 'elapsed time: {}'.format(elap),
        org = (10,20),
        fontFace = cv2.FONT_HERSHEY_DUPLEX,
        fontScale = 0.5,
        color = (0, 255, 0))

    cv2.putText(img = frame,
        text = 'status: {}'.format(status),
        org = (10,40),
        fontFace = cv2.FONT_HERSHEY_DUPLEX,
        fontScale = 0.5,
        color = (0, 255, 0))

    wake = onset - death

    if wake > 1:
        cv2.putText(img = frame,
            text = 'subject is ASLEEP',
            org = (10,60),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 0.5,
            color = (0, 0, 255))
    else:
        cv2.putText(img = frame,
            text = 'subject is awake',
            org = (10,60),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 0.5,
            color = (0, 255, 0))

    # out.write(frame)
    cv2.imshow("frame", frame)
    # cv2.imshow("orig", orig)
    # cv2.imshow("gray", gray)
    # cv2.imshow("roi", roi)
    # cv2.imshow("clahe", edges)
    # cv2.imshow("images", np.hstack([edges, gray]))

    key = cv2.waitKey(1) & 0xff
    if key == ord('p'):
        while(True):
            key2 = cv2.waitKey(1) or 0xff
            if key2 == ord('s'):
                cv2.imwrite("orig.jpg", orig)
                cv2.imwrite("edges.jpg", edges)
                cv2.imwrite("gray.jpg", gray)
                cv2.imwrite("roi.jpg", roi)
                # cv2.imwrite("images.jpg", np.hstack([edges, gray]))
            if key2 == ord('p'):
                break
    if key == ord('q'):
        break


cap.release()
# out.release()
cv2.destroyAllWindows()