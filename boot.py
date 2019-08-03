import ujson
import network
import ubinascii as u
from time import sleep
from machine import Pin, unique_id
from umqtt.simple import MQTTClient

# client config
ip = "157.230.30.178"
ids = unique_id()
mac = u.hexlify(ids)
mac = mac.decode('utf-8')
client_d = "Gen_monitoring-" + mac
print(client_d)
c = MQTTClient(client_id=client_d, server=ip)

# pin config
sensPin = Pin(4)


def pub(msg):
    topic = b"tele/engine/STATE"
    print(topic, msg)
    c.connect(clean_session=False)
    c.publish(topic, msg)
    c.disconnect()


def beat():
    topic = "tele/all/STATE"
    msg = {'type': 'engine', 'status': 1}
    msg = ujson.dumps(msg)
    print(topic, msg)
    c.connect()
    c.publish(topic, msg)
    c.disconnect()


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        f = open("config.json", "r")
        configs = f.read()
        j = ujson.loads(configs)
        print(j)
        f.close()
        print('connecting to network...')
        wlan.connect(j['network_name'], j['network_password'])
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def main():
    # do_connect()
    value_array = []
    for i in range(10):
        data = sensPin.value()
        value_array.append(data)
        sleep(.3)
    count = value_array.count(1)
    if count >= 5:
        data = {"Engine": "ON", "Uptime": ""}
        data = ujson.dumps(data)
        pub(data)
    else:
        data = {"Engine": "OFF", "Uptime": ""}
        data = ujson.dumps(data)
        pub(data)


if __name__ == '__main__':
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while True:
        if wlan.isconnected():
            beat()
            main()
        elif not wlan.isconnected():
            do_connect()
        else:
            do_connect()
            # reset()
