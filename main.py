import busio, board, displayio, terminalio, time
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

splash = displayio.Group() # define splash

def clear_screen():
    # clear the screen
    display.root_group = splash

    color_bitmap = displayio.Bitmap(160, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x000000  # Black

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    
def draw_player(x_pos, y_pos, last_x_pos = None, last_y_pos = None):
    # Set Const
    INNER_PALETTE = displayio.Palette(1)
    INNER_PALETTE[0] = 0xFFFFFF  # White
    
    # Clear memory
    #if not last_x_pos == None:
    #    for item in splash:
    #        inner_sprite = displayio.TileGrid(displayio.Bitmap(8, 8, 1), pixel_shader=INNER_PALETTE, x=last_x_pos, y=last_y_pos)
    #        if item == inner_sprite:
    #            splash.remove(item)
    
    # Draw a smaller inner rectangle
    inner_sprite = displayio.TileGrid(displayio.Bitmap(8, 8, 1), pixel_shader=INNER_PALETTE, x=x_pos, y=y_pos)
    if inner_sprite in splash:
        splash.remove(inner_sprite)
    splash.append(inner_sprite)
    #splash.remove(inner_sprite)

# Game start
# Set const

MAX_FPS = 10
KEY_UP = 0 # GP0
KEY_DOWN = 1 # GP1
MOVE_SPEED = 5 # pixels per tick
MOVE_SPEED_ENEMIES = 2 # pixels per tick, speed starts at this value
TEXT_SEPERATOR_HEIGT = 10
ENEMY_SPEED_MULTIPLIER = 0.005

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

pos = [10,10]
clear_screen()
draw_player(10,10)
while True:
    process_time_start = time.monotonic_ns()
    
    for item in splash:
        splash.remove(item)
    
    clear_screen()
    draw_player(10,10)
    
    process_time_end = time.monotonic_ns()
    process_time = process_time_end - process_time_start
    process_time = process_time / 1000000000 # convert to seconds
    if process_time <= 1/MAX_FPS:
        time.sleep(float(1/MAX_FPS) - process_time)
    

