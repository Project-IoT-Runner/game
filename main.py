import busio, board, displayio, terminalio, time, digitalio, random
from adafruit_display_text import label
from fourwire import FourWire

from adafruit_st7735r import ST7735R
from config import get_sprite, get_mock_sprite

# Release any resources currently in use for the displays
displayio.release_displays()

# Setup for displaying to the screen
spi = busio.SPI(board.GP2, board.GP3)
tft_cs = board.GP5
tft_dc = board.GP6

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.GP9)

display = ST7735R(display_bus, width=160, height=128, rotation=90, bgr=True)

# Game start

# Set const
MAX_FPS = 20
KEY_UP = board.GP0 # GP0
KEY_DOWN = board.GP1 # GP1
MOVE_SPEED = 3 # pixels per tick
MOVE_SPEED_ENEMIES = 1 # pixels per tick, speed starts at this value
TEXT_SEPERATOR_HEIGT = 10
ENEMY_SPEED_MULTIPLIER = 0.0025
ENEMY_AMOUNT = 1

btn_up = digitalio.DigitalInOut(KEY_UP)
btn_up.switch_to_input(pull=digitalio.Pull.UP)

btn_down = digitalio.DigitalInOut(KEY_DOWN)
btn_down.switch_to_input(pull=digitalio.Pull.UP)

PLAYER_SPRITE = get_mock_sprite()

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

def load_sprite(sprite, group):
    for y in range(len(sprite)):
        for x in range(len(ENTITY_SPRITE[y])):
            if ENTITY_SPRITE[y][x] == '#':
                group.append(displayio.TileGrid(displayio.Bitmap(1, 1, 1), pixel_shader=shader, x=x, y=y))

# This is the player
class Player():
    def __init__(self, game, screen, start_position, size=(8,8)):
        self.position = list(start_position)
        #self.position[0] += SCREEN_OFFSET
        self.size = size
        self.game = game
        self.screen = screen
        player_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
        player_palette = displayio.Palette(1)
        player_palette[0] = 0xFF0000
        self.sprite = displayio.TileGrid(player_bitmap, pixel_shader=player_palette, x=int(self.position[0]), y=int(self.position[1]))
        self.screen.append(self.sprite)
    
    def update(self):
        if not btn_up.value:
            if self.screen[self.screen.index(self.sprite)].y - MOVE_SPEED >= TEXT_SEPERATOR_HEIGT +1:
                self.screen[self.screen.index(self.sprite)].y -= int(MOVE_SPEED)
            else: self.screen[self.screen.index(self.sprite)].y = TEXT_SEPERATOR_HEIGT +1
        if not btn_down.value:
            if self.screen[self.screen.index(self.sprite)].y + MOVE_SPEED <= self.game.size[1] - self.size[1]:
                self.screen[self.screen.index(self.sprite)].y += int(MOVE_SPEED)
            else: self.screen[self.screen.index(self.sprite)].y = self.game.size[1] - self.size[1]

    def main(self) -> None:
        """Handles the Player() functions that run every frame"""
        # update position based on movement
        self.update()


# These are enemies
class Obstacle():
    def __init__(self, game, screen, player, start_position, size=(8,8), sprite=ENTITY_SPRITE):
        self.position = list(start_position)
        self.player = player
        self.size = size
        self.sprite = sprite
        self.game = game
        self.screen = self.game.screen
        self.speed = MOVE_SPEED_ENEMIES
        enemy_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
        enemy_palette = displayio.Palette(1)
        enemy_palette[0] = 0x00FF00
        self.enemy_sprite = displayio.TileGrid(enemy_bitmap, pixel_shader=enemy_palette, x=int(self.position[0]), y=int(self.position[1]))
        self.screen.append(self.enemy_sprite)

    def get_on_screen(self):
        """
        RETURNS:
            Bool: True if Entity is on screen
        """
        if self.screen[self.screen.index(self.enemy_sprite)].x < (-1)*self.size[0]:
            return False
        return True
    
    def update(self):
        self.screen[self.screen.index(self.enemy_sprite)].x -= int(self.speed)
        if not self.get_on_screen():
            self.screen[self.screen.index(self.enemy_sprite)].x = self.position[0]
            self.screen[self.screen.index(self.enemy_sprite)].y = self.game.random_height()

    def is_colliding(self):
        """
        RETURNS:
            Bool: if this enemy is colliding with the player
        """
        # check for horisontal collision
        selfx = self.screen[self.screen.index(self.enemy_sprite)].x
        selfy = self.screen[self.screen.index(self.enemy_sprite)].y
        playerx = self.screen[self.screen.index(self.player.sprite)].x
        playery = self.screen[self.screen.index(self.player.sprite)].y
        
        if selfx <= playerx + self.player.size[0] and selfx + self.size[0] >= playerx:
            if selfy <= playery + self.player.size[1] and selfy + self.size[1] >= playery:
                return True
        return False

    def render(self):
        pass
    
    def main(self):
        self.update()
        self.render()
        
        
# this is the main game
class Game():
    def __init__(self, size=(160, 128)):
        self.size = size
        self.screen = displayio.Group()
        display.root_group = self.screen
        self.player = Player(self, self.screen, (10, self.size[1]/2))
        self.score = 0
        self.enemies = [Obstacle(self, self.screen, self.player, (160, self.random_height())) for i in range(ENEMY_AMOUNT)]
        self.colliding = False
        self.TIME_DIFF_ENEMIES = round((self.size[0]/self.enemies[0].speed) / len(self.enemies))
        
        # create the background
        bg_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000

        bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
        self.screen.insert(0, bg_sprite)
        
        # create the text divider
        divider_bitmap = displayio.Bitmap(self.size[0], 1, 1)
        divider_palette = displayio.Palette(1)
        divider_palette[0] = 0xFFFFFF
        
        divider_sprite = displayio.TileGrid(divider_bitmap, pixel_shader=divider_palette, x=0, y=TEXT_SEPERATOR_HEIGT)
        self.screen.insert(1, divider_sprite)
        
        # create perm text
        text_group = displayio.Group(scale=1, x=1, y=5)
        text = "SCORE:          LVL:"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_group.append(text_area)  # Subgroup for text scaling
        self.screen.append(text_group)
        
        # create numbers
        number_group_score = displayio.Group(scale=1, x=40, y=5)
        score_number = f'{self.score}'
        self.score_label = label.Label(terminalio.FONT, text=score_number, color=0xFFFFFF)
        number_group_score.append(self.score_label)  # Subgroup for text scaling
        self.screen.append(number_group_score)
        
        # {int(self.enemies[0].speed)-1}
        number_group_lvl = displayio.Group(scale=1, x=125, y=5)
        lvl_number = f'{int(self.enemies[0].speed)-1}'
        self.lvl_label = label.Label(terminalio.FONT, text=lvl_number, color=0xFFFFFF)
        number_area_lvl = self.lvl_label
        number_group_lvl.append(number_area_lvl)  # Subgroup for text scaling
        self.screen.append(number_group_lvl)
        
    def add_to_splash(self, sprite):
        self.splash_list.append(sprite)
    
    def random_height(self) -> int:
        """
        RETURNS:
            int: A valid random height
        """
        # plus and minus one to account for the border
        value = random.randrange(0+TEXT_SEPERATOR_HEIGT, self.size[1]-len(ENTITY_SPRITE))
        return value
    
    def clear_screen(self):
        self.splash_list = []
        self.splash = displayio.Group()
        
    def draw_text(self):
        pass
    
    def replace_player_sprite(self):
        pass

    def game(self) -> None: # Code the game here
        enemy_timer = 0
        while True: #game loop
            # Set up for dtime
            process_time_start = time.monotonic_ns() # starts timer in nanoseconds

            # Game starts here
            
            self.draw_text()
            
            # update all entities
            enemy_timer += 1/self.TIME_DIFF_ENEMIES
            if int(enemy_timer) < len(self.enemies):
                for enemy_i in range(int(enemy_timer)):
                    self.enemies[enemy_i].main()
                    # check for collisions
                    if self.enemies[enemy_i].is_colliding():
                        self.colliding = True
            else:
                for enemy in self.enemies:
                    enemy.main()
                    enemy.speed += ENEMY_SPEED_MULTIPLIER
                    # check for collisions
                    if enemy.is_colliding():
                        self.colliding = True

            if self.colliding == True:
                self.colliding = False
                print('Test')
            
            self.player.main()
            
            # end of frame
            self.score += 1

            # check whether a collision has been detected this frame
            #if self.colliding:
            #    self.colliding = False
            #    break # returns to main menu


            # End of loop
            process_time_end = time.monotonic_ns() # End the timer
            # Calculate how long the program took to run in nanoseconds
            process_time = process_time_end - process_time_start
            process_time = process_time / 1000000000 # convert to seconds
            if process_time <= 1/MAX_FPS:
                time.sleep(float(1/MAX_FPS) - process_time) # Sleep for long enough that the loop runs at MAX_FPS
            

    def reset(self):
        self.player.position = self.size[1]/2

game = Game()

while True:
    game.score = 0
    game.reset()
    game.game()
    
