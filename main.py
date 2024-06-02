# Biblotheken laden 
import math
import time 
import mlx90614
import dht
from machine import Pin, SoftI2C, PWM
from utime import sleep



# Initialisierung und Variabeln 
time.sleep(1)
dht11_sensor = dht.DHT11(Pin(21, Pin.IN, Pin.PULL_UP))
# led_red = Pin(13, Pin.OUT)
# led_green = Pin(1, Pin.OUT)
red = Pin(2, Pin.OUT, value=0)
green = Pin(3, Pin.OUT, value=0)
blue = Pin(4, Pin.OUT, value=0)
K1 = float(243.12)
K2 = float(17.62)
i2c = SoftI2C(scl=Pin(27), sda=Pin(26), freq=100000)
sensor = mlx90614.MLX90614(i2c)
buzzer = PWM(Pin(9))
buzzer.freq(400)
buzzer.duty_u16(0)

# Wiederholung (Endlos-Schleife)
while True:
    # Messung durchführen
    dht11_sensor.measure()
    # Werte lesen
    temp = dht11_sensor.temperature()
    temp_rounded = round(temp, 1)
    humi = dht11_sensor.humidity()
    humi_rounded = round(humi, 1)
    # Berechnung mit den Werten 
    tpunkt = K1 * ((((K2 * temp) / (K1 + temp)) + math.log(humi / 100)) / (((K2 * K1) / (K1 + temp)) - math.log(humi / 100)))
    tpunkt_rounded = round(tpunkt, 1)
    # Wert von der Wandtemperatur auslesen
    wtemp = sensor.read_object_temp()
    wtemp_rounded = round(wtemp, 1)
    # time.sleep(5) 
    # Werte vergleichen und ggf. warnen 
    if tpunkt > wtemp:
        red.on()
        green.off()
        buzzer.freq(400)
        buzzer.duty_u16(1000)
        print("Es besteht Schimmelgefahr!")
    else: 
        buzzer.duty_u16(0)
        green.on()
        red.off()
        print("Es besteht keine Schimmelgefahr.")
    # Werte ausgeben
    print('      Temperatur:', temp_rounded, '°C')
    print('Luftfeuchtigkeit:', humi_rounded, '%')
    print('        Taupunkt:', tpunkt_rounded, '°C')
    print('  Wandtemperatur:', wtemp_rounded, '°C')
    print('-----------------------------------------------')
    time.sleep(5)
