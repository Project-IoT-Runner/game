import displayio

title = [
'  wwwwwwwww    wwwwwwwww               wwwwwwwwwwwwwwwwwwwwww                                               ',
' ww@@@@@@@ww  ww@@@@@@@ww             ww@@@@@@@@@@@@@@@@@@@@ww                                              ',
'ww@@#####@@w  w@@#####@@ww           ww@@##################@@ww                                             ',
'w@@#######@w  w@#######@@w           w@@####################@@w                                             ',
'w@########@w  w@########@w           w@######################@w                                             ',
'w@########@w  w@########@w           w@######################@w                                             ',
'w@########@w  w@########@w           w@######################@w                                             ',
'w@########@wwww@########@w           w@######################@w                                             ',
'w@########@@ww@@########@wwwwwwwwwwwww@######################@wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   ',
'w@#########@ww@#########@@@@@@@@@@@@@@@######################@@@@@@@@@@@@ww@@@@@@@@@@@@@@w@@@@@@ww@@@@@@ww  ',
'w@#########@ww@#########@@############@######################@##########@@@@############@@@####@@@@####@@ww ',
'w@@########@@@@########@@##############@####################@############@@##############@######@@######@@w ',
'ww@#########@@#########@@##############@@##################@#############@@##############@###############@w ',
' w@@##################@@@##############@@@@@############@@@@######@@@#####@##############@###############@w ',
' ww@##################@w@@############@@www@@##########@@ww@#####@@w@@####@@############@@###############@w ',
'  w@##################@w@@@@########@@@ww ww@##########@www@#####@@w@@####@@@@########@@@@@#############@@w ',
'  w@##################@w@ww@########@www   w@##########@w w@######@@@#####@ww@########@www@@###########@@ww ',
'  w@@################@@wwww@########@www   w@##########@w w@##############@ww@########@www@@###########@@ww ',
'  ww@################@www@@@########@@@ww  w@##########@w w@##############@@@@########@@@@@#############@@w ',
'   w@@##############@@ww@@############@@w  w@##########@w w@#############@@@############@@###############@w ',
'   ww@@############@@www@##############@w  w@##########@w w@##############@##############@###############@w ',
'    ww@@##########@@wwww@##############@w  w@##########@w w@##############@##############@###############@w ',
'     ww@@########@@ww ww@##############@w  w@@########@@w w@######@#######@##############@######@@######@@w ',
'      ww@@@####@@@ww   w@@############@@w  ww@@######@@ww w@@####@@@#####@@@############@@@####@@@@####@@ww ',
'       www@@@@@@www    ww@@@@@@@@@@@@@@ww   ww@@@@@@@@ww  ww@@@@@@w@@@@@@@w@@@@@@@@@@@@@@w@@@@@@ww@@@@@@ww  ',
'        wwwwwwwww       wwwwwwwwwwwwwwww     wwwwwwwwww    wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww   ']

title_outline = []
for row in title:
    line = ''
    for pixel in row:
        if pixel == ' ':
            line += pixel
        else:
            line += '#'
    title_outline.append(line)

def prep_sprite(sprite:list):
    result = []
    row = ''
    for i in range(len(sprite)):
        if sprite[i]:
            row += '#'
        else:
            row += ' '
        if len(row) == 8:
            result.append(row)
            row = ''
    return result

def part_sprite_hor(sprite,char:list) -> list:
    char = char[0]
    result = []
    true_counter = 0
    for row in sprite:
        counter = 0
        last_pixel = '/'
        result.append('/')
        for pixel in row:
            if pixel == last_pixel:
                counter += 1
            else:
                result.append(counter+1)
                counter = 0
                result.append(pixel in char)
                if pixel in char:
                    true_counter += 1
            last_pixel = pixel
    result.insert(0, true_counter)
    print(true_counter)
    return result

def load_sprite_hor(parted_sprite, color) -> displayio.Group():
    sprite = displayio.Group()
    
    palette = displayio.Palette(1)
    palette[0] = color
    
    start = False
    write = False
    row = -1
    for item in parted_sprite:
        if type(item) == type(False):
            write = item
        elif item == '/':
            start = True
            row += 1
            pos = 0
        elif start:
            if write:
                sprite.append(displayio.TileGrid(displayio.Bitmap(item, 1, 1), pixel_shader=palette, x=pos, y=row))
                pos += item
            else:
                pos += item
    return sprite

def load_title():
    title_group = displayio.Group()
    parted_sprite = part_sprite_hor(title, ['#'])
    parted_outline = part_sprite_hor(title_outline, ['#'])
    title_group.append(load_sprite_hor(parted_outline, 0xFF7700))
    title_group.append(load_sprite_hor(parted_sprite, 0x0000FF))
    return title_group
