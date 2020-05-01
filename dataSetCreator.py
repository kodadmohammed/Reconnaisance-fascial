#coding:utf-8
import cv2
import numpy as np
import sqlite3

facedetect=cv2.CascadeClassifier('fichier_predefinis_faciale.xml');
camera=cv2.VideoCapture(0);

def insertOrUpdate(Id, Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="select * from people where id="+str(Id)
    cursor=conn.execute(cmd)
    Exist=0
    for row in cursor:
        Exist=1
    if(Exist==1):
        cmd1="UPDATE people SET Name="+str(Name)+"WHERE id="+str(Id)
    else:
        cmd1="INSERT INTO people (id,name) Values ("+str(Id)+","+str(Name)+")"
    conn.execute(cmd1)
    conn.commit()
    conn.close()

id=input('entrer user id :')
Name=input('entrer votre nom :')
insertOrUpdate(id, Name)
simpleNum=0
while(True):
    ret,img=camera.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        simpleNum=simpleNum+1
        cv2.imwrite('dataSet/User.'+str(id)+"."+str(simpleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100)
    cv2.imshow("kodad",img)
    cv2.waitKey(1)
    if(simpleNum>20):
        break
camera.release()
cv2.destroyAllWindows()
