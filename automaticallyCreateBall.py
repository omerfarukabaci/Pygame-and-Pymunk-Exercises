#Project Name: Simple Robot Arm Simulation

import pygame, pymunk, pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Robot Arm v0.1")
clock = pygame.time.Clock()

##draw_options = pymunk.pygame_util.DrawOptions(screen)

gravity = -900.0

space = pymunk.Space()

space.gravity = (0,gravity)

position_pymunk=(200,100)

rad = 5
ball_elasticity = 0.8
friction = 1.0
circles = []

def create_circle(position):
    mass = 1
    inertia = pymunk.moment_for_circle(mass, 0, rad)
    body = pymunk.Body(mass, inertia)
    body.position = position
    shape = pymunk.Circle(body,rad)
    shape.elasticity = ball_elasticity
    shape.friction = friction
    space.add(body,shape)

    return shape

def create_block(position):
    mass = 10.0
    size = 100
    inertia = pymunk.moment_for_box(mass, (size,size))
    body = pymunk.Body(mass,inertia)
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

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            originalMousePos = pygame.mouse.get_pos()
            realPos = pymunk.pygame_util.to_pygame(originalMousePos, screen)
            newCircle = create_circle(realPos)
            circles.append(newCircle)
            print(len(circles))

    screen.fill((60,60,60))

    for circle in circles:
        circlePosition = int(circle.body.position.x), 600-int(circle.body.position.y)
        pygame.draw.circle(screen, (35, 88, 150), circlePosition, int(circle.radius), 0)

    position_pygame= int(block.body.position.x), 600-int(block.body.position.y)
    pygame.draw.rect(screen, (78,78,200), (position_pygame[0]-50, position_pygame[1]-50, 100, 100))

    pygame.draw.line(screen, line.color,(0,550),(800, 550), 30)
    pygame.draw.line(screen, line.color,(0,550),(0,0),30)
    pygame.draw.line(screen, line.color,(800,550),(800,0),30)

    # space.debug_draw(draw_options)
    space.step(1/60.0)
    pygame.display.update()


pygame.quit()


