import RPi.GPIO as GPIO
import  time
import signal
import atexit

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
