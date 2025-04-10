from __future__ import print_function
import keyboard, time, random
from drawille import Canvas # this is what's used to draw

MAX_FPS = 10
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
    
# This is the player
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

    def main(self) -> None:
        """Handles the Player() functions that run every frame"""
        # update position based on movement
        self.update()
        # write pixels to frame
        self.render()


# These are enemies
class Obstacle():
    def __init__(self, game, player, start_position, size=(8,8), sprite=ENTITY_SPRITE):
        self.position = list(start_position)
        self.position[0] += SCREEN_OFFSET
        self.player = player
        self.size = size
        self.sprite = sprite
        self.game = game
        self.speed = MOVE_SPEED_ENEMIES

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
            self.position[1] = self.game.random_height()

    def is_colliding(self):
        """
        RETURNS:
            Bool: if this enemy is colliding with the player
        """
        # check for horisontal collision
        if self.position[0] <= self.player.position[0] + self.player.size[0] and self.position[0] + self.size[0] >= self.player.position[0]:
            if self.position[1] <= self.player.position[1] + self.player.size[1] and self.position[1] + self.size[1] >= self.player.position[1]:
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



# this is the main game
class Game():
    def __init__(self, screen=Canvas(), size=(160, 128)):
        self.size = (size[0]+2, size[1]+2)
        # create the player
        self.player = Player(self, (10, self.size[1]/2))
        # create all enemies
        self.enemies = [
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height())),
            Obstacle(self, self.player, (self.size[0], self.random_height()))
            ]
        self.screen = screen
        self.score = 0
        # the amount of ticks that should be between the enmies starting
        self.TIME_DIFF_ENEMIES = round((self.size[0]/self.enemies[0].speed) / len(self.enemies))

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
    
    def random_height(self) -> int:
        """
        RETURNS:
            int: A valid random height
        """
        # plus and minus one to account for the border
        value = random.randrange(0+TEXT_SEPERATOR_HEIGT + 1, self.size[1]-len(ENTITY_SPRITE) - 1)
        return value

    def update(self):
        print(self.screen.frame())

    def game(self) -> None: # Code the game here
        enemy_timer = 0
        while True: #game loop
            # Set up for dtime
            process_time_start = time.time_ns() # starts timer in nanoseconds

            # Stop if q is pressed
            if get_input('q'):
                break

            # Game starts here
            # clear last frame
            self.screen.clear()
            self.draw_border()

            # update all entities
            enemy_timer += 1/self.TIME_DIFF_ENEMIES
            if int(enemy_timer) < len(self.enemies):
                for enemy_i in range(int(enemy_timer)):
                    self.enemies[enemy_i].main()
            else:
                for enemy in self.enemies:
                    enemy.main()
            self.player.main()

            # end of frame
            self.clear_pixels_offscreen()
            self.score += 1
            self.draw_score()


            # End of loop
            game.update() # Show screen in terminal
            process_time_end = time.time_ns() # End the timer
            # Calculate how long the program took to run in nanoseconds
            process_time = process_time_end - process_time_start
            process_time = process_time / 1000000000 # convert to seconds
            if process_time <= 1/MAX_FPS:
                time.sleep(float(1/MAX_FPS) - process_time) # Sleep for long enough that the loop runs at MAX_FPS
            #break
        

    

game = Game()
game.game()