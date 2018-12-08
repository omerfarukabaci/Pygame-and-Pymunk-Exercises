#Project Name: Simple Robot Arm Simulation
#Last Encountered Issue: have to add pins & joints

import pygame
import pymunk
import pymunk.pygame_util
from math import cos,sin
    
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Robot Arm v0.1")
clock = pygame.time.Clock()

draw_options = pymunk.pygame_util.DrawOptions(screen)

gravity = -900.0

space = pymunk.Space()

space.gravity = (0,gravity)

position_pymunk = (200,100)

rad = 8
ball_elasticity = 0.8
friction = 1.0

def create_circle(position):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Circle(body,rad)
    shape.elasticity = ball_elasticity
    shape.friction = friction
    space.add(body,shape)
    
    return shape

circle = create_circle((200,200))

def create_block(position):
    mass = 10.0
    size = 100
    inertia = pymunk.moment_for_box(mass, (size,size))
    body = pymunk.Body(mass, inertia)
    body.position = position
    shape = pymunk.Poly.create_box(body, (size,size))
    shape.elasticity = 0.0
    shape.friction = 2
    space.add(body,shape)

    return shape

def create_line(p1,p2):
    
    static_body = space.static_body
    static_body.position = (400, 600)
    line_shape = pymunk.Segment(static_body, p1, p2, 15)
    line_shape.elasticity = 1.0
    line_shape.color = (23, 150, 78)
    space.add(line_shape)

    return line_shape

line = create_line((-400, -550), (400, -550))
create_line((400,-550),(400,0))
create_line((-400,-550),(-400,0))

block = create_block(position_pymunk)

running = True

def rotate_point(angle,pt):
    
    px,py = pt
    ca = cos(angle)
    sa = sin(angle)
    qx =  ca * px + sa * py
    qy = -sa * px + ca * py
    
    return (qx,qy)

jointState = False
waitState = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((60,60,60))
    #background color
    
    originalMousePos = pygame.mouse.get_pos()
    #getting mouse position
    
    realPos = pymunk.pygame_util.to_pygame(originalMousePos, screen)
    #converting pymunk positions to pygame positions
    
    circle.body.position = realPos
    #setting pymunk circle's position
 
    if int(block.body.position[1] + 58) == circle.body.position[1] and (circle.body.position[0] >= block.body.position[0] - 58 and circle.body.position[0] <= block.body.position[0] + 58):

        if not jointState and not waitState:
            stickPos = (realPos[0] - block.body.position[0], block.body.position[1]-realPos[1]+100)
            joint = pymunk.PivotJoint(block.body, circle.body, stickPos, (0,0))
            joint.collide_bodies = False
            joint.distance = 0
            space.add(joint)
            joint.error_bias = pow(0,60.0)
            jointState = True
            waitState = True

        if not waitState and jointState:
            space.remove(joint)
            waitState = True
            jointState = False


    if circle.body.position[1] > 150:
        waitState = False  
    
        


    #---Robot Arm Grabbing Part Ends---#
        

    #---Pygame Drawing Part Starts---#

    circlePosition = int(circle.body.position.x), 600-int(circle.body.position.y)
    position_pygame = int(block.body.position.x), 600-int(block.body.position.y) 
    #converting pymunk positions to pygame positions
    
    pygame.draw.circle(screen, (35, 88, 150), circlePosition, int(circle.radius), 0)
    #drawing the circle

    points = [(-50,50),(-50,-50),(50,-50),(50,50)]
    points = [ rotate_point(block.body.angle,p) for p in points  ]
    points = [(x+position_pygame[0],y + position_pygame[1]) for (x,y) in points]
    pygame.draw.polygon(screen, (78,78,200), points)
    #drawing the polygon

    pygame.mouse.set_visible(False)
    pygame.draw.line(screen, line.color,(0,550),(800, 550), 30)
    pygame.draw.line(screen, line.color,(0,550),(0,0),30)
    pygame.draw.line(screen, line.color,(800,550),(800,0),30)
    #drawing the borders
    
    #---Pygame Drawing Part Ends---#
    

    #---Pygame & Pymunk FPS and Other Settings Starts---#
    space.debug_draw(draw_options)
    space.step(1/20.0)
    pygame.display.update()
    clock.tick(60)
    #---Pygame & Pymunk FPS and Other Settings Ends ---#


pygame.quit()
