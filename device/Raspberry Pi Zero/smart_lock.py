import paho.mqtt.client as mqtt
import struct
import ast
import RPi.GPIO as GPIO
import time



MQTT_BROKER_ADDR = '172.29.156.89'
MQTT_BROKER_PORT = 1883

# GPIO番号指定モードの設定
GPIO.setmode(GPIO.BCM) # GPIO番号
#GPIO.setmode(GPIO.BOARD) # ボードピン番号
GPIO.setup(4, GPIO.OUT)

is_locked = True



def onConnect(publisher, user_data, flags, response_code):
	#print("response code: {0}".format(response_code))
	publisher.subscribe("SmartInoueLab2018/smart_lock", 0)



def onMessage(publisher, user_data, msg):
	global is_locked 


	try:
		if msg.topic.split("/")[1] == "smart_lock":
			payload_DICT = ast.literal_eval(msg.payload.decode('utf-8'))

			if is_locked and payload_DICT['smart_lock'] == 0:
				#print("unlocked")
				is_locked = False
				# Unlocked the door
				servo = GPIO.PWM(4, 50)
				servo.start(0)
				servo.ChangeDutyCycle(3.0)
				time.sleep(0.5)
				servo.stop()

		
			elif not is_locked and payload_DICT['smart_lock'] == 1:
				#print("locked")
				is_locked = True
				# Locked the door
				servo = GPIO.PWM(4, 50)
				servo.start(0)
				servo.ChangeDutyCycle(7.35)
				servo.ChangeDutyCycle(7.5)
				time.sleep(0.5)
				servo.stop()


	except Exception:
		None





if __name__ == '__main__':
	mqtt_subscriber = mqtt.Client(protocol=mqtt.MQTTv31)
	mqtt_subscriber.on_connect = onConnect
	mqtt_subscriber.on_message = onMessage
	mqtt_subscriber.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)


try:
	mqtt_subscriber.loop_forever()

except KeyboardInterrupt:
	GPIO.cleanup()
	None

except Exception:
	GPIO.cleanup()
	None
	


