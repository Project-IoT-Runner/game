import keyboard, time, random
from drawille import Canvas

MAX_FPS = 5
KEY_UP = 'w'
KEY_DOWN = 's'
MOVE_SPEED = 5 # pixels per tick
MOVE_SPEED_ENEMIES = 2 # pixels per tick, speed starts at this value
SCREEN_OFFSET = 8 # this makes sure that the enemies don't push the screen arround
TEXT_SEPERATOR_HEIGT = 10

ENTITY_SPRITE = [
                '#OO##OO#',
                'O######O',
                'O#O##O#O',
                '########',
                '###OO###',
                'O#O##O#O',
                'O######O',
                '#OO##OO#'
                ]

def get_input(key:str) -> bool:
    if keyboard.is_pressed(key):
        return True
    else:
        return False
    
class Obstacle():
    def __init__(self, game, player, start_position, size=(8,8), sprite=ENTITY_SPRITE):
        self.position = list(start_position)
        self.position[0] += SCREEN_OFFSET
        self.player = player
        self.size = size
        self.sprite = sprite
        self.game = game

    def get_on_screen(self):
        """
        RETURNS:
            Bool: True if Entity is on screen
        """
        if self.position[0] <=1:
            return False
        return True
    
    def update(self):
        self.position[0] -= MOVE_SPEED_ENEMIES
        if self.get_on_screen() == False:
            self.position[0] = self.game.size[0]+SCREEN_OFFSET - 1 # minus one to account for the border
            self.position[1] = random.randrange(0+TEXT_SEPERATOR_HEIGT + 1, self.game.size[1] - 1) # plus and minus one to account for the border

    def is_colliding(self):
        """
        RETURNS:
            Bool: if this enemy is colliding with the player
        """
        if self.position[0] <= self.player.position[0] + self.player.size[0] and self.position[0] + self.size[0] >= self.player.position[0]:
            print('test')

    def render(self):
        s_x = self.position[0]
        s_y = self.position[1]
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.sprite[y][x] == '#':
                    self.game.screen.set((s_x+x),(s_y+y))
    
    def main(self):
        self.update()
        self.render()
        self.is_colliding()


class Player():
    def __init__(self, game, start_position, size=(8,8)):
        self.position = list(start_position)
        self.position[0] += SCREEN_OFFSET
        self.size = size
        self.game = game
    
    def update(self):
        if get_input(KEY_UP):
            if self.position[1] - MOVE_SPEED >= 11:
                self.position[1] -= MOVE_SPEED
            else: self.position[1] = 11
        if get_input(KEY_DOWN):
            if self.position[1] + MOVE_SPEED <= self.game.size[1] - self.size[1]:
                self.position[1] += MOVE_SPEED
            else: self.position[1] = self.game.size[1] - self.size[1]

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
        self.enemy1 = Obstacle(self, self.player, (70, 50))
        self.screen = screen
        self.score = 0

    def draw_border(self):
        # Draw full border
        for x in range(SCREEN_OFFSET, self.size[0]+SCREEN_OFFSET): # Draw top row
            self.screen.set(x, 0)
        for x in range(SCREEN_OFFSET, self.size[0]+SCREEN_OFFSET): # Draw bottom row
            self.screen.set(x, self.size[1])
        for y in range(self.size[1]): # Draw left column
            self.screen.set(SCREEN_OFFSET, y)
        for y in range(self.size[1]): # Draw right column
            self.screen.set(self.size[0]+SCREEN_OFFSET, y)
        
        for x in range(SCREEN_OFFSET, self.size[0]+SCREEN_OFFSET): # Draw text seperation
            self.screen.set(x, TEXT_SEPERATOR_HEIGT)

    def draw_score(self):
        self.screen.set_text(5+SCREEN_OFFSET, 5, f'SCORE: {self.score}')

    def clear_pixels_offscreen(self):
        for y in range(self.size[1]):
            for x in range(SCREEN_OFFSET):
                self.screen.unset(x,y)
                self.screen.unset(x+self.size[0]+SCREEN_OFFSET + 1, y) # plus one to account for the border
    
    def update(self):
        print(self.screen.frame())

    def game(self): # Code the game here
        # clear last frame
        self.screen.clear()
        self.draw_border()

        # update all entities
        self.player.main()
        self.enemy1.main()

        # end of frame
        self.clear_pixels_offscreen()
        self.score += 1
        self.draw_score()

    

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