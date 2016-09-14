#version of Memory using the Tile class

   

import simplegui
import random
import math

# globals
TILE_WIDTH = 100
TILE_HEIGHT = 100
DISTINCT_TILES = 16
ALL_TILES = DISTINCT_TILES*2
def get_num_of_row(tiles):
    for i in range(int(math.sqrt(tiles)),tiles):
        if tiles%i == 0:
            return i
num_of_row = get_num_of_row(ALL_TILES)
num_of_columns = ALL_TILES/num_of_row
print(num_of_row,num_of_columns)


# helper function to initialize globals
def new_game():
    global my_tiles, state, turns

    tile_numbers = range(DISTINCT_TILES) * 2
    random.shuffle(tile_numbers)
    print tile_numbers
    my_tiles = [Tile(tile_numbers[i], False, [TILE_WIDTH * (i%num_of_columns), TILE_HEIGHT * (i//num_of_columns + 1)]) for i in range(2 * DISTINCT_TILES)]
    
    state = 0
    turns = 0
    label.set_text("Turns = "+str(turns))  

# definition of a Tile class
class Tile:
    
    # definition of intializer
    def __init__(self, num, exp, loc):
        self.number = num
        self.exposed = exp
        self.location = loc
        
    # definition of getter for number
    def get_number(self):
        return self.number
    
    # check whether tile is exposed
    def is_exposed(self):
        return self.exposed
    
    # expose the tile
    def expose_tile(self):
        self.exposed = True
    
    # hide the tile       
    def hide_tile(self):
        self.exposed = False
        
    # string method for tiles    
    def __str__(self):
        return "Number is " + str(self.number) + ", exposed is " + str(self.exposed)    

    # draw method for tiles
    def draw_tile(self, canvas):
        loc = self.location
        if self.exposed:
            text_location = [loc[0] + 0.2 * TILE_WIDTH, loc[1] - 0.3 * TILE_HEIGHT]
            canvas.draw_text(str(self.number), text_location, TILE_WIDTH/2, "White")
        else:
            tile_corners = (loc, [loc[0] + TILE_WIDTH, loc[1]], [loc[0] + TILE_WIDTH, loc[1] - TILE_HEIGHT], [loc[0], loc[1] - TILE_HEIGHT])
            canvas.draw_polygon(tile_corners, 1, "Red", "Green")

    # selection method for tiles
    def is_selected(self, pos):
        inside_hor = self.location[0] <= pos[0] < self.location[0] + TILE_WIDTH
        inside_vert = self.location[1] - TILE_HEIGHT <= pos[1] <= self.location[1]
        return  inside_hor and inside_vert     
        

# event handlers
def mouseclick(pos):
    global state, turns, turn1_tile, turn2_tile
    
    for tile in my_tiles:
        if tile.is_selected(pos):
            clicked_tile = tile
            
    if clicked_tile.is_exposed():
        return
    
    clicked_tile.expose_tile()
    
    if state == 0:
        state = 1
        turn1_tile = clicked_tile
    elif state == 1:
        state = 2
        turn2_tile = clicked_tile
        turns += 1
        label.set_text("Turns = " + str(turns)) 
    else:
        if turn1_tile.get_number() != turn2_tile.get_number():               
            turn1_tile.hide_tile()
            turn2_tile.hide_tile()
        state = 1
        turn1_tile = clicked_tile
            
# draw handler
def draw(canvas):
    for tile in my_tiles:
        tile.draw_tile(canvas)
        print tile.location
    
#frame and a button and labels
frame = simplegui.create_frame("Memory", num_of_columns * TILE_WIDTH, num_of_row * TILE_HEIGHT)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)



new_game()
frame.start()
    

