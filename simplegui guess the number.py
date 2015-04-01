# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global range
    global guesses_left
    secret_number = random.randint(0,int(range))
    if range == 100:
        guesses_left = 7
    else:
        guesses_left = 10
    print "Starting new game ( range", range,")"
    print "Please enter your guess in the text box"
    print "But integers only or we will self-detonate :)\n"


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game     
    global range
    range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range
    range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    guess = int(guess)
    print "Guess was", guess
    #print secret_number
    if guess == secret_number:
        print "Correct!\n"
    elif guess < secret_number:
        print "Higher!"
    else:
        print "Lower!"
    global guesses_left
    guesses_left -= 1
    if guesses_left == 0 and not guess == secret_number:
        print "You lose!"
        print ""
        new_game()
    elif not guess == secret_number:
        print guesses_left, "guesses left"
    else:
        new_game()
    

    
# create frame
f = simplegui.create_frame("Guess the number",300,300)

# register event handlers for control elements and start frame
f.add_input("Enter guess", input_guess, 100)
f.add_button("Range 100", range100, 100)
f.add_button("Range 1000", range1000, 100)


# call new_game 
range = 100
new_game()


# always remember to check your completed program against the grading rubric
