import busio, board, displayio, terminalio, time, digitalio, random, load_sprite
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
ENEMY_SPEED_MULTIPLIER = 0.003
ENEMY_AMOUNT = 4

btn_up = digitalio.DigitalInOut(KEY_UP)
btn_up.switch_to_input(pull=digitalio.Pull.UP)

btn_down = digitalio.DigitalInOut(KEY_DOWN)
btn_down.switch_to_input(pull=digitalio.Pull.UP)

player_sprite = get_sprite()['sprite']['pixels']

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

 #####        #####                    ##################
#######      #######                  ####################
#########    #########               ######################
#########    #########               ######################
#########    #########               ######################
#########    #########               ######################
#########    #########               ######################
#########    #########               ######################
#########    #########  ############ ###################### ##########    ############   ####    ####
#########    ######### ############## #################### ############  ############## ######  ######
##########  ########## ##############  ################## #############  ############## ###############
###################### ##############     ############    ######   ##### ############## ###############
###################### ##############      ##########     #####     #### ############## ###############
######################  ############       ##########     #####     ####  ############   #############
 ####################     ########         ##########     ######   #####    ########      ###########
 ####################     ########         ##########     ##############    ########      ###########
 ####################   ############       ##########     ##############  ############   #############
  ##################   ##############      ##########     #############  ############## ###############
  ##################   ##############      ##########     ############## ############## ###############
   ################    ##############      ##########     ############## ############## ###############
    ##############     ##############       ########      ###### ####### ############## ######  ######
      ##########        ############         ######        ####   #####   ############   ####    ####

screen = displayio.Group()
display.root_group = screen


def load_sprite_old(sprite, group, color):
    shader = displayio.Palette(1)
    shader[0] = color
    for y in range(len(sprite)):
        for x in range(len(sprite[y])):
            if sprite[y][x] == '#':
                group.append(displayio.TileGrid(displayio.Bitmap(1, 1, 1), pixel_shader=shader, x=x, y=y))

# This is the player
class Player():
    def __init__(self, game, start_position, size=(8,8)):
        self.position = list(start_position)
        self.size = size
        self.game = game
        self.sprite = displayio.Group()
        
    
    def update(self):
        if not btn_up.value:
            if screen[screen.index(self.sprite)].y - MOVE_SPEED >= 1:
                screen[screen.index(self.sprite)].y -= int(MOVE_SPEED)
            else: screen[screen.index(self.sprite)].y = 1
        if not btn_down.value:
            if screen[screen.index(self.sprite)].y + MOVE_SPEED <= self.game.size[1] - self.size[1]:
                screen[screen.index(self.sprite)].y += int(MOVE_SPEED)
            else: screen[screen.index(self.sprite)].y = self.game.size[1] - self.size[1]

    def main(self) -> None:
        """Handles the Player() functions that run every frame"""
        # update position based on movement
        self.update()
    
    def reset(self):
        if not game.custom_sprite:
            player_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
            player_palette = displayio.Palette(1)
            player_palette[0] = 0x0000FF
            self.sprite = displayio.TileGrid(player_bitmap, pixel_shader=player_palette, x=int(self.position[0]), y=int(self.position[1]))
        else:
            #player_bitmap_bg = displayio.Bitmap(self.size[0], self.size[1], 1)
            #player_palette_bg = displayio.Palette(1)
            #player_palette_bg[0] = 0xFF7700
            #self.sprite_bg = displayio.TileGrid(player_bitmap_bg, pixel_shader=player_palette_bg, x=0, y=0)
            #self.sprite.insert(0, self.sprite_bg)
            pass
        screen.append(self.sprite)


# These are enemies
class Obstacle():
    def __init__(self, game, player, start_position, size=(8,8), sprite=ENTITY_SPRITE):
        self.position = list(start_position)
        self.player = player
        self.size = size
        self.sprite = sprite
        self.game = game
        self.speed = MOVE_SPEED_ENEMIES
        self.reset()

    def get_on_screen(self):
        """
        RETURNS:
            Bool: True if Entity is on screen
        """
        if screen[screen.index(self.enemy_sprite)].x < (-1)*self.size[0]:
            return False
        return True
    
    def update(self):
        screen[screen.index(self.enemy_sprite)].x -= int(self.speed)
        if not self.get_on_screen():
            screen[screen.index(self.enemy_sprite)].x = self.position[0]
            screen[screen.index(self.enemy_sprite)].y = self.game.random_height()

    def is_colliding(self):
        """
        RETURNS:
            Bool: if this enemy is colliding with the player
        """
        # check for horisontal collision
        selfx = screen[screen.index(self.enemy_sprite)].x
        selfy = screen[screen.index(self.enemy_sprite)].y
        playerx = screen[screen.index(self.player.sprite)].x
        playery = screen[screen.index(self.player.sprite)].y
        
        if selfx <= playerx + self.player.size[0] and selfx + self.size[0] >= playerx:
            if selfy <= playery + self.player.size[1] and selfy + self.size[1] >= playery:
                return True
        return False
    
    def main(self):
        self.update()
        
    def reset(self):
        self.enemy_sprite = displayio.Group()
        enemy_palette = displayio.Palette(1)
        enemy_palette[0] = 0x00FF00
        self.enemy_sprite.append(displayio.TileGrid(displayio.Bitmap(8,8,1), pixel_shader=enemy_palette))
        self.enemy_sprite.x= self.position[0]
        self.enemy_sprite.y = self.position[1]
        screen.append(self.enemy_sprite)
        
        
# this is the main game
class Game():
    def __init__(self, size=(160, 128)):
        self.custom_sprite = False
        self.enemy_timer = 0
        self.size = size
        self.player = Player(self, [10,80])
        self.score = 0
        self.enemies = [Obstacle(self, self.player, (160, self.random_height())) for i in range(ENEMY_AMOUNT)]
        self.colliding = False
        self.TIME_DIFF_ENEMIES = round((self.size[0]/self.enemies[0].speed) / len(self.enemies))
        
    def add_to_splash(self, sprite):
        self.splash_list.append(sprite)
    
    def random_height(self) -> int:
        """
        RETURNS:
            int: A valid random height
        """
        # plus and minus one to account for the border
        value = random.randrange(1+TEXT_SEPERATOR_HEIGT, self.size[1]-len(ENTITY_SPRITE))
        return value
    
    def clear_screen(self):
        self.splash_list = []
        self.splash = displayio.Group()      

    def game(self) -> None: # Code the game here
        self.enemy_timer = 0
        running = True
        while running: #game loop
            # Set up for dtime
            process_time_start = time.monotonic_ns() # starts timer in nanoseconds

            # Game starts here
            
            # update all entities
            self.enemy_timer += 1/self.TIME_DIFF_ENEMIES
            if int(self.enemy_timer) < len(self.enemies):
                for enemy_i in range(int(self.enemy_timer)):
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
            
            self.player.main()
            
            # end of frame
            self.score += 1
            
            if self.colliding == True:
                self.colliding = False
                print(self.score)
                break
                

            # End of loop
            process_time_end = time.monotonic_ns() # End the timer
            # Calculate how long the program took to run in nanoseconds
            process_time = process_time_end - process_time_start
            process_time = process_time / 1000000000 # convert to seconds
            if process_time <= 1/MAX_FPS:
                time.sleep(float(1/MAX_FPS) - process_time) # Sleep for long enough that the loop runs at MAX_FPS
            

    def reset(self):
        for i in range(len(screen)):
            screen.pop(0)
            
            
        self.score = 0
        self.enemy_timer = 0
        self.player.position = [10, int(self.size[1]/2)]
        for enemy in self.enemies:
            enemy.enemy_sprite.x = 160
            enemy.enemy_sprite.y = self.random_height()
            enemy.speed = MOVE_SPEED_ENEMIES
            enemy.reset()
        # create the background
        bg_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
        bg_palette = displayio.Palette(1)
        bg_palette[0] = 0x000000

        bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
        screen.insert(0, bg_sprite)    
        
        self.player.reset()
        
        self.game()



class MainMenu():
    def __init__(self, score, size=(160, 128)):
        self.size = list(size)
        self.sprite_updated = False
        self.score=str(score)
        
    def reset(self):
        self.sprite_updated = False
        
        for i in range(len(screen)):
            screen.pop(0)
        
        menu_bg_bitmap = displayio.Bitmap(self.size[0], self.size[1], 1)
        menu_bg_palette = displayio.Palette(1)
        menu_bg_palette[0] = 0x333333

        menu_bg_sprite = displayio.TileGrid(menu_bg_bitmap, pixel_shader=menu_bg_palette, x=0, y=0)
        screen.insert(0, menu_bg_sprite)
        
        title = load_sprite.load_title()
        title.x = 25
        title.y = 20
        screen.append(title)
        
        text_group = displayio.Group(x=0, y=70)
        text = f"   PRESS A OR B TO START\n    YOUR LAST SCORE WAS\n{(' '*(15-len(str(game.score))))+str(game.score)}!"
        text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
        text_group.append(text_area)
        
        screen.append(text_group)
        
        
        self.main()
    
    def main(self):
        ticks_down_button_held = 0
        ticks_up_button_held = 0
        while True:
            process_time_start = time.monotonic_ns()
            
            if not btn_down.value:
                ticks_down_button_held += 1
            else:
                ticks_down_button_held = 0
                
            if not btn_up.value:
                ticks_up_button_held += 1
            else:
                ticks_up_button_held = 0
            
            button_time = [ticks_down_button_held, ticks_up_button_held]
            button_time.sort()
            
            if button_time[1]-button_time[0] > 1*MAX_FPS:
                break
            
            if not self.sprite_updated and ticks_down_button_held > 3*MAX_FPS:
                self.update_sprite()
            
            process_time_end = time.monotonic_ns() # End the timer
            # Calculate how long the program took to run in nanoseconds
            process_time = process_time_end - process_time_start
            process_time = process_time / 1000000000 # convert to seconds
            if process_time <= 1/MAX_FPS:
                time.sleep(float(1/MAX_FPS) - process_time) # Sleep for long enough that the loop runs at MAX_FPS
                
    def update_sprite(self):        
        player_sprite = load_sprite.prep_sprite(get_sprite()['sprite']['pixels'])
        load_sprite_old(player_sprite, game.player.sprite, 0xFF7700)
        game.player.sprite.x = game.player.position[0]
        game.player.sprite.y = game.player.position[1]
        
        print('updated')
        game.custom_sprite = True
        self.sprite_updated = True
        


game = Game()
menu = MainMenu(game.score)

while True:
    menu.reset()
    game.reset()
