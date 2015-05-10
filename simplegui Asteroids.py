# can be run at http://www.codeskulptor.org/#user39_mYs3PfGiEI_26.py
# Asteroids game
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MAX_LIVES = 3                            
rock_max_speed = 1
time = 0
score = 0
lives = MAX_LIVES

def init(): # start/restart
    global started, rock_group, missile_group, explosion_group
    started = False
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    soundtrack.rewind()
    soundtrack.play()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.f2014.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.accel = [0,0] # forward vector
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(ship_image, [3*self.image_center[0],self.image_center[1]], self.image_size, 
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(ship_image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
            
    def update(self):
        self.angle += self.angle_vel # turn ship
        self.accel = angle_to_vector(self.angle)
        # move ship and warp around the screen edge
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        if self.thrust:
            ship_thrust_sound.play()
            for i in range(2): # accelerate
                self.vel[i] += 0.5*self.accel[i]        
        else:
            ship_thrust_sound.rewind()
        for i in range(2): # friction from space debris
            self.vel[i] *= 0.95
    
    def turn(self, direction):
        self.angle_vel += 0.1 * direction
        
    def stop_turn(self):
        self.angle_vel = 0
    
    # fires a missile from tip of ship cannon
    def shoot(self):
        global a_missile
        a_missile = Sprite([self.pos[0]+self.radius*self.accel[0],self.pos[1]+self.radius*self.accel[1]],
                           [self.vel[0]+8*self.accel[0],self.vel[1]+8*self.accel[1]], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated: # explosion sprites use this
            canvas.draw_image(self.image, [self.age * self.image_size[0] + self.image_center[0],self.image_center[1]], 
                                           self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        # move sprite and warp around the screen edge
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel # rotate  
        self.age += 1
        if self.age > self.lifespan: # flag to be removed
            return True
        else:
            return False

    # return True if there is a collision or False otherwise. 
    def collide(self,other_object):
        if dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius():
            return True
        else:
            return False
    
def draw(canvas):
    global time, started, lives, score, rock_max_speed
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    if group_collide(rock_group,my_ship): # rock hits ship
        lives -= 1
        if lives == 0: # game over
            timer.stop()
            init()
    if group_group_collide(rock_group,missile_group): # missile hits rock
        score += 1
        if score % 10 == 0: # speed up rocks as game progresses
            rock_max_speed += 1
    
    # draw lives and score
    canvas.draw_text("Lives: " + str(lives),[20,50],36,"Cyan")
    canvas.draw_text("Score: " + str(score),[600,50],36,"Plum")            

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
# timer handler that spawns a rock    
def rock_spawner():
    if len(rock_group) < 12:
        a_rock = Sprite([random.randint(0,WIDTH), random.randint(0,HEIGHT)], 
                    [random.randint(-rock_max_speed,rock_max_speed+1), 
                     random.randint(-rock_max_speed,rock_max_speed+1)], 
                    0, float(random.randint(-5,6))/100, asteroid_image, asteroid_info)
        # add new rock only if not too close to ship
        if not dist(a_rock.pos, my_ship.get_position()) < 2*(a_rock.radius + my_ship.get_radius()):            
            rock_group.add(a_rock)

# draws and updates a group of sprites        
def process_sprite_group(group, canvas):
    to_del = [] # remember items to be deleted
    for item in group:
        item.draw(canvas)
        if item.update(): # if sprite is past its lifespan
            to_del.append(item)
    for item in to_del: # remove expired items
        group.remove(item)
        
# checks for collisions between other_object and elements of the group 
# if there is a collision, the colliding object is removed 
def group_collide(group, other_object):
    copy = list(group) # make copy to be able to delete from original list
    for item in copy:
        if item.collide(other_object):
            group.remove(item)
            expl = Sprite(item.pos,[0,0],0,0,explosion_image,explosion_info,explosion_sound)
            explosion_group.add(expl) # flashy visual effects!
            return True
    return False

def group_group_collide(group, other_group):
    copy = list(group)
    for item in copy:
        if group_collide(other_group, item):
            group.remove(item)
            return True
    return False            
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    
# key press handlers
def keydown(key):
    if key==simplegui.KEY_MAP["left"]:
        my_ship.turn(-1)
    if key==simplegui.KEY_MAP["right"]:
        my_ship.turn(1)
    if key==simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    if key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    
def keyup(key):
    if key==simplegui.KEY_MAP["left"] or key==simplegui.KEY_MAP["right"]:
        my_ship.stop_turn()
    if key==simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
         
# mouseclick handlers that reset UI and conditions when splash image is clicked
def click(pos):
    global score, lives, started 
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True   
        score = 0
        lives = MAX_LIVES
        timer.start() # start spawning rocks

# register handlers
init()
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
frame.start()