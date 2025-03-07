from machine import Pin
import utime
button = Pin(14, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)

class Player():
    def __init__(self):
        pass
    
    def move_up(self):
        pass
    
    def move_down(self):
        pass
    
    def get_collition(self) -> bool:
        pass
    
    def kill_player(self):
        pass
    
while True:
    if button.value() == 1:
        led.value(1)
        utime.sleep(.2)
    else:
        led.value(0)