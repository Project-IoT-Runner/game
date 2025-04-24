import busio
import board
import displayio
import terminalio
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
    
def draw_pixel(x_pos, y_pos):
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(1, 1, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xFFFFFF  # White
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=x_pos, y=y_pos)
    splash.append(inner_sprite)

# game start
