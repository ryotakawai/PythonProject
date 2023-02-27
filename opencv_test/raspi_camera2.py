import cv2
import datetime

dt_now = datetime.datetime.now()
file_name = dt_now.strftime('%Y_%m_%d_%H_%M_%S')

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

cv2.imwrite(file_name + '.jpg', frame)
cap.release()