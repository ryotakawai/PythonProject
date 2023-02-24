# OpenCV をインポート
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

def detect_face(img):

    # 読み込んだ顔の画像をまずcopy()で複製する
    face_img = img.copy()

    # detectMultiScale()を使って顔検出を行う
    face_rects = face_cascade.detectMultiScale(face_img)

    for (x,y,w,h) in face_rects:
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (0,255,0), 10)

    return face_img

def detect_eyes(img):
    
    face_img = img.copy()
  
    eyes = eye_cascade.detectMultiScale(face_img) 
    
    
    for (x,y,w,h) in eyes: 
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 10) 
        
    return face_img

random_code = random.randint(0,1000000000)

face1 = cv2.imread('images/input.jpg', 0)
face2 = cv2.imread('images/show-face1.jpg', 0)

# # テキストを描画する
# cv2.putText(face1,
#             text='sample text',
#             org=(100, 300),
#             fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#             fontScale=1.0,
#             color=(0, 255, 0),
#             thickness=2,
#             lineType=cv2.LINE_4)

result1 = detect_face(face1)
cv2.imwrite("results/" + str(random_code) + "write1.jpg",result1) 
plt.imshow(result1, cmap="gray")
plt.show()

# result2 = detect_eyes(face2)
# cv2.imwrite("results/" + str(random_code) + "write2.jpg",result2) 
# plt.imshow(result2, cmap="gray")
# plt.show()


print("成功")