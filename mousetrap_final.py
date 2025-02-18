import time
import wiringpi
import spidev
import json
import requests
from ch7_ClassLCD import LCD
from datetime import datetime

#define vars
closed_door = False

#number of steps needed for a full rotation
steps_per_rotation = 510
count = 0
reset = 0
status = "Armed"
status_int = 0
count_LCD = 0

#stepper motor pins
coil_pins = [9, 6, 4, 3]

#defining the pins on the ultrasonic measurement
Trig = 1
Echo = 2

#
button = 16 #pins of the button

PIN_OUT = {
    'SCLK': 14,
    'DIN': 11,
    'DC': 5,
    'CS': 15,
    'RST': 10,
    'LED': 12,
}

pin_CS_lcd = 15
relay = 0


#sequence for the stepper motor
sequence = [
    [coil_pins[0], coil_pins[1], 0, 0],
    [0, coil_pins[1], coil_pins[2], 0],
    [0, 0, coil_pins[2], coil_pins[3]],
    [coil_pins[0], 0, 0, coil_pins[3]]
]

#set the wiring  pin mode for the distance measurement
wiringpi.wiringPiSetup()
wiringpi.pinMode(Trig, wiringpi.OUTPUT)
wiringpi.pinMode(Echo, wiringpi.INPUT)

#setup of the button pins
for pin in coil_pins:
    wiringpi.pinMode(pin, 1)

wiringpi.pinMode(button, wiringpi.INPUT) #setup of button pins
wiringpi.pinMode(relay, wiringpi.OUTPUT) #setup of the relay


#ultrasonic distance measurement
def distance():
    wiringpi.digitalWrite(Trig,True) #trigger on/off
    time.sleep(0.00001)
    wiringpi.digitalWrite(Trig,False)
    
    while wiringpi.digitalRead(Echo) == False:
        pass
    Start_time = time.time()
    
    while wiringpi.digitalRead(Echo) == True:
        pass
    Stop_time = time.time()
    
    Elapsed = Stop_time - Start_time
    distance = Elapsed * 17000
    distance = round(distance, 2)
    return (distance)

#control the motor
def step_motor(steps, delay=0.002):
    for i in range(steps):
        for step in sequence:
            for pin_index, pin_value in enumerate(step):
                wiringpi.digitalWrite(coil_pins[pin_index], pin_value)
            time.sleep(delay)

#LCD code
def ActivateLCD():
    wiringpi.digitalWrite(pin_CS_lcd, 0)
    time.sleep(0.000005)

def DeactivateLCD():
    wiringpi.digitalWrite(pin_CS_lcd, 1)
    time.sleep(0.000005)

#LCD to display the current time, activateand what to ptint and where on the lCD
#deactivate when it should
def UpdateLCD():
    current_time = datetime.now().strftime("%H:%M:%S")
    ActivateLCD()
    lcd_1.clear()
    lcd_1.go_to_xy(0, 0)
    lcd_1.put_string(current_time)
    lcd_1.go_to_xy(0, 10)
    lcd_1.put_string(status)
    lcd_1.go_to_xy(0, 20)
    lcd_1.put_string(str(count_LCD))
    lcd_1.refresh()
    DeactivateLCD()

wiringpi.wiringPiSPISetupMode(1, 0, 400000, 0)
wiringpi.pinMode(pin_CS_lcd , 1)
ActivateLCD()
lcd_1 = LCD(PIN_OUT)

#ubeac credentials
url = "http://mouse00.hub.ubeac.io/iotessrae"
uid = "Rae 1"

lcd_1.clear()
lcd_1.set_backlight(1)

while True:
    closed_door = False
    reset = 0
    count = 0
    UpdateLCD()
    
    while closed_door == False:
        distance_cm = distance()
        time.sleep(0.5)
        UpdateLCD()
        if distance_cm < 10.0 or wiringpi.digitalRead(button) == 1:
            closed_door = True
            status = "Triggered"
            status_int = 1
            count_LCD +=1
    
    UpdateLCD()
    data = {
        "id": uid,
        "sensors":[{
            'id': 'Count',
            'data': count
        },
        {"id": 'Status',
            "data" : status_int
        }]
    }
    
    step_motor(steps=steps_per_rotation)
    UpdateLCD()
    
    #clean up GPIO pins
    wiringpi.digitalWrite(coil_pins[0], 0)
    wiringpi.digitalWrite(coil_pins[1], 0)
    wiringpi.digitalWrite(coil_pins[2], 0)
    wiringpi.digitalWrite(coil_pins[3], 0)
    
    #relay board setup
    while reset == 0:
        wiringpi.digitalWrite(relay, wiringpi.HIGH)
        time.sleep(1)
        wiringpi.digitalWrite(relay, wiringpi.LOW)
        time.sleep(1)
        count += 1
        UpdateLCD()
        if (count >= 3 and wiringpi.digitalRead(button) == 1):
            reset = 1
            status = "Armed"
            status_int = 0
        UpdateLCD()
        time.sleep(1.0)