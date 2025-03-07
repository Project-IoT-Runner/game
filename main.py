from machine import Pin
import utime
button_up = Pin(14, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(15, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)

class Player():
    def __init__(self):
        pass
    
    def move_up(self):
        print('Up')
    
    def move_down(self):
        print('Down')
    
    def get_collition(self) -> bool:
        pass
    
    def kill_player(self):
        pass
    
    def check_player_input(self, up, down):
        if up.value() == 1:
            self.move_up()
            utime.sleep(0.05)
        elif down.value() == 1:
            self.move_down()
            utime.sleep(0.05)

player = Player()
while True:
    player.check_player_input(button_up, button_down)
