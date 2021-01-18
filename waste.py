import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt
import threading
import json
import requests
import base64
import RPi.GPIO as GPIO
import  time
import signal
import atexit

while True:
	cap = cv2.VideoCapture(0) #读取摄像头
	x1,x2,y1,y2=150,500,100,450    #定义检测边缘
	def mean_gray(gray, x1,x2,y1,y2):    #计算区域内的灰度平均值
		count=0
		for x in range(x1+1, x2):
			for y in range(y1+1,y2):
				count+= gray[y][x]
		count=count/((x2-x1)*(y2-y1))
		print (count)
		return count

	countold= 150#事先定义原来区域内的灰度平均值
	detect=False
	def jiance(gray_frame,mean_gray,x1,x2,y1,y2):    #检测现区域灰度和原灰度的差值，判断是否有画面改变
		global detect
		countnew=mean_gray(gray_frame,x1,x2,y1,y2)
		countcha=countnew-countold
		if abs(countcha)>8:
			detect=True

	flag=0  #用于设置20帧检测一次

	while True:
		ret,frame = cap.read()  #读取摄像头
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #转化为灰度值

		if flag==20:    #1秒检测一次
			flag=0
			t=threading.Thread(target=jiance,args=(gray_frame,mean_gray,x1,x2,y1,y2))    #线程运行检测函数
			t.start()

    # 画出检测的区域（也不是必要的）
    #bule=(255,0,0)
    #cv2.line(frame,(x1,y1),(x1,y2),bule,5)
   #cv2.line(frame,(x1,y1),(x2,y1),bule,5)
    #cv2.line(frame,(x2,y1),(x2,y2),bule,5)
    #cv2.line(frame,(x1,y2),(x2,y2),bule,5)
    #cv2.imshow('farme',frame) 

		flag+=1
		if detect is True: #如果区域颜色有改变拍照保存
			img=cv2.imwrite('image.jpg',frame)
			break
    

    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

# 释放窗口
	cap.release()
#cv2.destroyAllWindoqws()

#

 
# client_id 为官网获取的AK， client_secret 为官网获取的SK
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=fsmUeDGw0mryglTPB4AnDgkk' \
       '&client_secret=gfyCN9hkfVvlOchwStxgX0mpcu5VPEHQ'
	response = requests.get(host)
	content = response.json()
	access_token = content["access_token"]
 
	image = open('image.jpg', 'rb').read()
	data = {'image': base64.b64encode(image).decode()}
 
	request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/yiliaolaji"+"?access_token=" + access_token
	response = requests.post(request_url, data=json.dumps(data))
	content = response.json()
	print(content['results'][0])

	if content['results'][0]['name']=='shabu':
		a=1
	elif content['results'][0]['name']=='yaoping':
		a=2
	elif content['results'][0]['name']=='shuyeguan':
		a=3

#
	def dian(a):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(18,GPIO.OUT)
		p=GPIO.PWM(18,800)
		p.start(50)
		if a ==1: #su liao
			time.sleep(2.282)
		elif a ==2: 
			time.sleep(2.282*2)
		elif a ==3:
			time.sleep(0)
		p.stop()
		GPIO.cleanup()

	dian(a) #yun xing jian ji

	#yun xing duo ji

	atexit.register(	GPIO.cleanup)

	servopin = 16
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(servopin,GPIO.OUT,initial=False)
	p=GPIO.PWM(servopin,50)
	p.start(0)


	for i in range(0,181,10):
		p.ChangeDutyCycle(12.5)
		time.sleep(0.02)	
		p.ChangeDutyCycle(0)
		time.sleep(0.02)
	time.sleep(1)
	for i in range(181,0,-10):
		p.ChangeDutyCycle(2.5)
		time.sleep(0.02)
		p.ChangeDutyCycle(0)
		time.sleep(0.02)
		
		#zhuan hui dian ji wei zhi
		
