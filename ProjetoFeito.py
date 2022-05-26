from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
import utime


# global toggle button variable
measure_on = False

# debounce for button
def debounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed)

# if button pressed, toggle measure_on
def on_pressed(timer):
    global measure_on
    measure_on = not measure_on
    print("apertei!")

# Init button
button = Pin(16, Pin.IN, Pin.PULL_DOWN)
timer = Timer()
button.irq(debounce, Pin.IRQ_RISING)

# Init Display
i2c = I2C(0,sda=Pin(0),scl=Pin(1),freq=40000)
oled = SSD1306_I2C(128,32,i2c)
oled.fill(0)
oled.text("Aperte para",22,8)
oled.text("iniciar!",22,16)
oled.show()


# Init HC-SR04 pins
trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)


def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print("The distance from object is ",distance,"cm")
    oled.fill(0)
    oled.text("Distancia:",22,8)
    oled.text(str(distance) + " cm",22,16)
    oled.show()
    return distance
while True:
    if measure_on:
       ultra()
       utime.sleep(1)
#     else:
#         oled.fill(0)
#         oled.text("Aperte o botâo para inicar a medição!")
#         oled.show()
    



# try:
#     while True:
#         oled.fill(0)
#         if measure_on:
#             result = ultra()
#             oled.text("Distance:",0,0)
#             oled.text(str(result) + " cm",0,10)
#         oled.show()
#         utime.sleep(1)            
# except KeyboardInterrupt:
#     pass