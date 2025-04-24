import busio, board, displayio, terminalio, time, digitalio, random
from adafruit_display_text import label
from fourwire import FourWire

from adafruit_st7735r import ST7735R

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
MOVE_SPEED = 5 # pixels per tick
MOVE_SPEED_ENEMIES = 2 # pixels per tick, speed starts at this value
TEXT_SEPERATOR_HEIGT = 10
ENEMY_SPEED_MULTIPLIER = 0.005

btn_up = digitalio.DigitalInOut(KEY_UP)
btn_up.switch_to_input(pull=digitalio.Pull.UP)

btn_down = digitalio.DigitalInOut(KEY_DOWN)
btn_down.switch_to_input(pull=digitalio.Pull.UP)

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
        player_palette[0] = 0xFFFFFF
        self.sprite = displayio.TileGrid(player_bitmap, pixel_shader=player_palette, x=int(self.position[0]), y=int(self.position[1]))
        self.screen.append(self.sprite)
    
    def update(self):
        if not btn_up.value:
            if self.screen[self.screen.index(self.sprite)].y - MOVE_SPEED >= 0:
                self.screen[self.screen.index(self.sprite)].y -= int(MOVE_SPEED)
            else: self.screen[self.screen.index(self.sprite)].y = 0
        if not btn_down.value:
            if self.screen[self.screen.index(self.sprite)].y + MOVE_SPEED <= self.game.size[1] - self.size[1]:
                self.screen[self.screen.index(self.sprite)].y += int(MOVE_SPEED)
            else: self.screen[self.screen.index(self.sprite)].y = self.game.size[1] - self.size[1]

    def main(self) -> None:
        """Handles the Player() functions that run every frame"""
        # update position based on movement
        self.update()



# this is the main game
class Game():
    def __init__(self, size=(160, 128)):
        self.size = (size[0]+2, size[1]+2)
        self.screen = displayio.Group()
        display.root_group = self.screen
        # create the player
        self.player = Player(self, self.screen, (10, self.size[1]/2))
        self.score = 0
        
        self.colliding = False
        color_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x000000  # Bright Green

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.screen.insert(0, bg_sprite)
        
    def add_to_splash(self, sprite):
        self.splash_list.append(sprite)
    
    def random_height(self) -> int:
        """
        RETURNS:
            int: A valid random height
        """
        # plus and minus one to account for the border
        value = random.randrange(0+TEXT_SEPERATOR_HEIGT + 1, self.size[1]-len(ENTITY_SPRITE) - 1)
        return value
    
    def clear_screen(self):
        self.splash_list = []
        self.splash = displayio.Group()

    def game(self) -> None: # Code the game here
        enemy_timer = 0
        while True: #game loop
            # Set up for dtime
            process_time_start = time.monotonic_ns() # starts timer in nanoseconds

            # Game starts here
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