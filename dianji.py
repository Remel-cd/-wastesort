import RPi.GPIO as GPIO
import  time

def dian(a):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(18,GPIO.OUT)
	p=GPIO.PWM(18,800)
	p.start(50)
	if a ==2: #su liao
		time.sleep(2.282)
	elif a ==1: 
		time.sleep(2.282*2)
	elif a ==0:
		time.sleep(0)
	p.stop()
	GPIO.cleanup()


