# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
BALL_SPEED = 3
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [BALL_SPEED,BALL_SPEED]
paddle1_pos = [0 + HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
score1 = 0
score2 = 0
paddle1_vel = [0,0]
paddle2_vel = [0,0]
paddle_accel = 5

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if (direction == RIGHT):
        ball_vel[0] = BALL_SPEED
    else:
        ball_vel[0] = -BALL_SPEED
       
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]    
    
    # collide and reflect off the walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_pos[1] - HALF_PAD_HEIGHT > 0 + paddle_accel and paddle1_vel[1] < 0) or
        (paddle1_pos[1] + HALF_PAD_HEIGHT < HEIGHT - paddle_accel and paddle1_vel[1] > 0)):
        paddle1_pos[1] += paddle1_vel[1]
    if ((paddle2_pos[1] - HALF_PAD_HEIGHT > 0 + paddle_accel and paddle2_vel[1] < 0) or
        (paddle2_pos[1] + HALF_PAD_HEIGHT < HEIGHT - paddle_accel and paddle2_vel[1] > 0)):
        paddle2_pos[1] += paddle2_vel[1]
    
    # draw paddles - left and right      
    canvas.draw_line([paddle1_pos[0], paddle1_pos[1] + HALF_PAD_HEIGHT],
                     [paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "White")
    
    canvas.draw_line([paddle2_pos[0], paddle2_pos[1] + HALF_PAD_HEIGHT],
                     [paddle2_pos[0], paddle2_pos[1] - HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide  
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if (ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT and 
        ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            score2 += 1
            print "player 2 scores"
            spawn_ball(RIGHT)
            
    if (ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH):
        if (ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT and 
        ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            score1 += 1  
            print "player 1 scores"
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text((str)(score1), [10, 30], 40, 'Cyan')
    canvas.draw_text((str)(score2), [550, 30], 40, 'Cyan')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += paddle_accel
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= paddle_accel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += paddle_accel
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= paddle_accel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] -= paddle_accel
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] += paddle_accel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] -= paddle_accel
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] += paddle_accel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
