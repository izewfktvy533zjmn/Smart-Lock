import paho.mqtt.client as mqtt
import struct
import ast



MQTT_BROKER_ADDR = '172.29.156.89'
MQTT_BROKER_PORT = 1883





def onConnect(publisher, user_data, flags, response_code):
	#print("response code: {0}".format(response_code))
	publisher.subscribe("SmartInoueLab2018/entrance", 0)



def onMessage(publisher, user_data, msg):
	#print("topic: " + msg.topic)
	#print("subtopic " + msg.topic)
	#print("subtopic " + msg.topic.split("/")[1])
	payload_STR = msg.payload.decode('utf-8')
	payload_DICT = ast.literal_eval(payload_STR)
	
	#print(payload_DICT['entrance']['exist'])

	if payload_DICT['entrance']['exist'] == 1:
		mqtt_publisher.publish("SmartInoueLab2018/smart_lock", "{\"smart_lock\":0}", qos=0)
	
	elif payload_DICT['entrance']['exist'] == 0:
		mqtt_publisher.publish("SmartInoueLab2018/smart_lock", "{\"smart_lock\":1}", qos=0)



if __name__ == '__main__':
	mqtt_publisher = mqtt.Client(protocol=mqtt.MQTTv31)
	mqtt_publisher.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)
	mqtt_subscriber = mqtt.Client(protocol=mqtt.MQTTv31)
	mqtt_subscriber.on_connect = onConnect
	mqtt_subscriber.on_message = onMessage
	mqtt_subscriber.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)


try:
    mqtt_subscriber.loop_forever()

except KeyboardInterrupt:
	None
