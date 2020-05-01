#coding:utf-8
import cv2
import numpy as np
import sqlite3

facedetect=cv2.CascadeClassifier('fichier_predefinis_faciale.xml');

rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainingData.yml")


def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People where id="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
camera=cv2.VideoCapture(0);
id=0
while(True):
    ret,img=camera.read();
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getProfile(id)
        if(profile!= None):
            cv2.putText(img,str(profile[1]),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
            cv2.putText(img,profile[2],(x,y+h+30),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        

    cv2.imshow("kodad",img)
    if(cv2.waitKey(1)==ord('a')):
        break;
camera.release()
cv2.destroyAllWindows()
