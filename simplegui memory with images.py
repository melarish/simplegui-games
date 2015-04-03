# implementation of card game - Memory
# http://www.codeskulptor.org/#user39_aVJwYUuTKK_2.py
# if images don't load, uncomment line 75

import simplegui
import random

# y coordinates for text and rectangles
texty = 50
recty1 = 0
recty2 = 100
card_width = 50

# Images from Fullmetal Alchemist - an awesome anime :)
images = [simplegui.load_image("https://i.imgur.com/JLDYzTu.jpg"),
          simplegui.load_image("https://i.imgur.com/0x2E4bM.jpg"),
          simplegui.load_image("https://i.imgur.com/VW7tveC.jpg"),
          simplegui.load_image("https://i.imgur.com/1W6G3MZ.jpg"),
          simplegui.load_image("https://i.imgur.com/5Foym7K.jpg"),
          simplegui.load_image("https://i.imgur.com/AM00vLv.jpg"),
          simplegui.load_image("https://i.imgur.com/XKquFME.jpg"),
          simplegui.load_image("https://i.imgur.com/bPEGXV7.jpg")]
images.extend(images)

# helper function to initialize globals
def new_game():
    global deck, exposed, turns
    deck = range(0,8)
    deck.extend(deck)
    exposed = [False]*16
    turns = 0
    label.set_text("Turns = " + str(turns))
    random.shuffle(deck)
    global state
    state = 0

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1, card2, matchfound
    global turns
    index = pos[0] // 50
    if exposed[index] != True: # If the card is already exposed, you should ignore the mouseclick
        exposed[index] = True
        if state == 0: # First card turned over
            state = 1
            card1 = index
        elif state == 1: # Second card turned over
            state = 2
            card2 = index
            turns += 1
            label.set_text("Turns = " + str(turns))
            if deck[card1] == deck[card2]:
                print "match"
                matchfound = True
            else:
                matchfound = False
        else:
            state = 1
            if not matchfound:         # Flip face down again   
                exposed[card1] = False
                exposed[card2] = False
            card1 = index
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global drawx
    drawx = 0
    for idx, card in enumerate(deck):
        if exposed[idx]:
            canvas.draw_image(images[card], (images[card].get_width() / 2, images[card].get_height() / 2), 
                              (images[card].get_width(), images[card].get_height()), (drawx+25,texty), (50, 100))
            #canvas.draw_text(str(card), [drawx+15,texty], 40, "Cyan")
        else:
            canvas.draw_polygon([[drawx,recty1], [drawx+card_width, recty1], 
                                 [drawx+card_width, recty2], [drawx, recty2]], 2, 'Black', 'Green')
        drawx+=card_width  


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric