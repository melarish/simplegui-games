# template for "Stopwatch: The Game"
import simplegui
# define global variables
time = 0
tries = 0
successes = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    pass
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():    
    timer.start()
    
def stop():  
    global time, tries, successes
    if timer.is_running():
        tries += 1      
    timer.stop()
    if time % 10 == 0:
        successes += 1

def reset():    
    global time, tries, successes
    time = tries = successes = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1


# define draw handler
def draw(canvas):
    global time, tries, successes
    canvas.draw_text((str)(time), [200, 200], 36, "Cyan")
    canvas.draw_text((str)(successes)+" /", [400, 100], 36, "Purple")
    canvas.draw_text((str)(tries), [445, 100], 36, "Purple")

    
# create frame
frame = simplegui.create_frame("Stopwatch", 500, 500)


# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)


# start frame
frame.start()


# Please remember to review the grading rubric
