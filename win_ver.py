import keyboard, time
from drawille import Canvas

MAX_FPS = 20

def get_input(key:str) -> bool:
    if keyboard.is_pressed(key):
        return True
    else:
        return False

class Player():
    def __init__(self, Game):
        self.position = {'x': 0, 'y': 0}
        self.game = Game
    
    def update(self):
        if get_input('w'):
            self.position['y'] -= 1
        if get_input('s'):
            self.position['y'] += 1

class Game():
    def __init__(self):
        self.player = Player(self)
    
    def game(self):
        self.player.update()
        print(self.player.position)

game = Game()
while True: #game loop
    process_time_start = time.time_ns()
    game.game()
    if get_input('q'):
        break

    # end 
    process_time_end = time.time_ns()
    process_time = process_time_end - process_time_end
    time.sleep((1/MAX_FPS) - process_time) # makes sure program runs at 20 fps so speed is consistent.