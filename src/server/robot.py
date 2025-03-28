# python 3.11
#sudo ../rasptank/bin/python3 -m src.server.robot
import random
import os
from paho.mqtt import client as mqtt_client
from src.server import move, infra, detectLine
from src.server.LED import LED
import RPi.GPIO as GPIO
from src.rasptank import InfraLib
import uuid
from threading import Thread
import time

broker = 'broker.emqx.io' #''192.168.0.125
tankID = hex(uuid.getnode())

port = 1883
topics = ["python/ctrlrobot", 
          f"tanks/{tankID}/init", 
          f"tanks/{tankID}/shots/in", 
          f"tanks/{tankID}/shots/out", 
          f"tanks/{tankID}/flag",
          f"tanks/{tankID}/qr_code"
          ]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

led = LED()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def set_receive_infra(client):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    IR_RECEIVER = 15
    GPIO.setup(IR_RECEIVER, GPIO.IN)
    while True:
        shooter = InfraLib.getSignal(IR_RECEIVER)
        if shooter:
            #shooter = "0x" + str(shooter)[4:]
            print(f"Sent `SHOT_BY {shooter} to tanks/{tankID}/shots topic")
            client.publish(f'tanks/{tankID}/shots', f'SHOT_BY {shooter}')

def set_motor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    move.motorStop()


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global led
        message = msg.payload.decode("utf-8")
        print(f"Received `{message}` from `{msg.topic}` topic")
        if msg.topic == "python/ctrlrobot":
            if "start" in message:
                move.start()
            if "left" in message:
                move.left()
            if "right" in message:
                move.right()
            if "back" in message:
                move.back()
            if "stop" in message:
                move.stop()
            if "tir" in message:
                print(f"On a tiré : {tankID} ")
                led.blink(r=255, g=0, b=0, time_sec=1)
                infra.shoot()
                led = LED()
            if "INIT" in message:
                result = client.publish("init", f"INIT {tankID}")
                status = result[0]
                if status == 0:
                    print(f"Send INIT {tankID} to topic init")
        if msg.topic == f"tanks/{tankID}/init":
            if "TEAM BLUE" in message:
                led.blink(r=0, g=0, b=255, time_sec=1)
            if "TEAM RED" in msg.payload.decode():
                led.blink(r=255, g=0, b=0, time_sec=1)
        if msg.topic == f"tanks/{tankID}/shots/in":
            if "SHOT" in message:
                led.blink_shot()
        if msg.topic == f"tanks/{tankID}/shots/out":
            if "FRIENDLY_FIRE" in message:
                led.blink(0.5)
            if "SHOT" in message:
                led.blink(r=0,g=255,b=0, time_sec=1)
        if msg.topic == f"tanks/{tankID}/flag":
            #TODO: fill in the blanks
            if "START_CATCHING" in message:
                led.blink(r=255,g=255,b=0, time_sec=1)
            if "FLAG_CATCHED" in message:
                led.blink(r=0,g=255,b=0, time_sec=1)
            if "ABORT_CATCHING_EXIT" in message:
                led.blink(r=255,g=255,b=0, time_sec=0.5)
            if "ABORT_CATCHING_SHOT" in message:
                led.blink_shot()
            if "FLAG_LOST" in  message:
                led.blink(r=255, g=0, b=0, time_sec=1)
            if "WIN_BLUE" in message:
                pass
            if "WIN_RED" in message:
                pass
        if msg.topic == f"tanks/{tankID}/qr_code" :
            if "SCAN_SUCCESSFUL" in message:
                pass
            if "SCAN_FAILED" in message:
                pass
            if "FLAG_DEPOSITED" in message:
                pass
            if "NO_FLAG" in message:
                pass
        

    for topic in topics:
        client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    t1 = Thread(target=set_receive_infra, args=(client,))
    #TODO fix multithreading
    t2 = Thread(target=detectLine.detect_zone_capture, args=(client,))
    t1.start()
    t2.start()
    #set_motor()
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        move.destroy()
        led.colorWipe(0, 0, 0)
