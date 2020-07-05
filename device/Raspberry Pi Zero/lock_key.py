import RPi.GPIO as GPIO
import time



# GPIO番号指定モードの設定
GPIO.setmode(GPIO.BCM) # GPIO番号
#GPIO.setmode(GPIO.BOARD) # ボードピン番号

GPIO.setup(4, GPIO.OUT)

servo = GPIO.PWM(4, 50)
servo.start(0)

# Close the door
servo.ChangeDutyCycle(7.25)
#servo.ChangeDutyCycle(7.35)
time.sleep(1)

servo.stop()

GPIO.cleanup()
