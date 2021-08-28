import cv2
from time import sleep
cap = cv2.VideoCapture('test.py')


human_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cap = cv2.VideoCapture("in_crowd.avi")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    humans = human_cascade.detectMultiScale(gray, 1.9, 1)
    
    # Display the resulting frame
    for (x,y,w,h) in humans:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
         
         

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) in [ord('q'),27,13]:
        break
    sleep(1/10)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

