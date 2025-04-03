import keyboard, time
from drawille import Canvas

MAX_FPS = 20
KEY_UP = 'w'
KEY_DOWN = 's'
MOVE_SPEED = 10

def get_input(key:str) -> bool:
    if keyboard.is_pressed(key):
        return True
    else:
        return False

class Player():
    def __init__(self, game, start_position, size=(8,8)):
        self.position = list(start_position)
        self.size = size
        self.game = game
    
    def update(self):
        if get_input(KEY_UP):
            self.position[1] -= MOVE_SPEED
        if get_input(KEY_DOWN):
            self.position[1] += MOVE_SPEED

    def render(self):
        s_x = self.position[0]
        s_y = self.position[1]
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.game.screen.set(s_x + x, s_y + y)

    
    def main(self):
        self.update()
        self.render()


class Game():
    def __init__(self, screen=Canvas(), size=(160, 128)):
        self.size = (size[0]+2, size[1]+2)
        self.player = Player(self, (10, self.size[1]/2))
        self.screen = screen

    def draw_border(self):
        for x in range(self.size[0]): # Draw top row
            self.screen.set(x, 0)
        for x in range(self.size[0]): # Draw bottom row
            self.screen.set(x, self.size[1])
        for y in range(self.size[1]): # Draw left column
            self.screen.set(0, y)
        for y in range(self.size[1]): # Draw right column
            self.screen.set(self.size[0], y)
        
    def setup(self):
        self.screen.clear()
        self.draw_border()

    def update(self):
        print(self.screen.frame())

    def game(self): # Code the game here
        self.setup()
        self.player.main()
    

game = Game()
while True: #game loop
    # Set up for dtime
    process_time_start = time.time_ns()
    # Stop if q is pressed
    if get_input('q'):
        break

    # Game starts here
    game.game()


    # End of loop
    game.update() # Show screen in terminal
    process_time_end = time.time_ns() # End the timer
    process_time = process_time_end - process_time_end # Calculate how long the program took to run
    time.sleep((1/MAX_FPS) - process_time) # Sleep for long enough that the loop runs at MAX_FPS
    #break