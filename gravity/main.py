import pygame
import sys
import pymunk
import random 

# PARAMETERS
SMALLEST_R, LARGEST_R = 10, 80
HEIGHT, WIDTH = 800, 1000

def createDynamicBall(space, pos=(400, 0)):
    "Create a dynamic ball"
    # pymunk.Body(1, 100) means mass = 1, inertia = 100
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    # Create a shape for the body, 80 for the radius
    ballRadius = random.randint(SMALLEST_R, LARGEST_R)
    shape = pymunk.Circle(body, ballRadius)
    space.add(body, shape)
    # Create a randomized color for the ball
    ballColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return shape, ballColor, ballRadius

def drawDynamicBall(dynamicBalls):
    for ball, ballColor, ballRadius in dynamicBalls:
        posX = int(ball.body.position.x)
        posY = int(ball.body.position.y)
        pygame.draw.circle(surface=screen, color=ballColor, center=(posX, posY), radius=ballRadius) 

def createStaticBall(space, pos=(500, 400)):
    "Create a static ball"
    # NOTE: kinematic and static bodies have infinite mass and zero inertia, or are usually ignored
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    # Randomized radius as well
    ballRadius = random.randint(10, 60)
    shape = pymunk.Circle(body, ballRadius) # radius = 50, make sure the visual radius matches the physical radius
    space.add(body, shape)
    # Create a randomized color for the ball
    ballColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return shape, ballColor, ballRadius

def drawStaticBall(staticBalls):
    for ball, ballColor, ballRadius in staticBalls:
        posX = int(ball.body.position.x)   
        posY = int(ball.body.position.y)
        pygame.draw.circle(surface=screen, color=ballColor, center=(posX, posY), radius=ballRadius)

def createPlatform(space, pos, size):
    "Create a static platform"
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos # NOTE: position is set in the center
    shape = pymunk.Poly.create_box(body, size)
    space.add(body, shape)
    return shape

def drawPlatform(platforms):
    for platform in platforms:
        vertices = platform.get_vertices()
        vertices = [(int(v.rotated(platform.body.angle).x + platform.body.position.x),
                     int(v.rotated(platform.body.angle).y + platform.body.position.y)) for v in vertices]
        pygame.draw.polygon(screen, (0, 0, 0), vertices)


# Initialize the Game 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# Create a universe (a canvas) for the objects to exist in and be applied with physics
space = pymunk.Space()
# Defining gravity effect on x and y axis, we will just set x downward to be 100 for now
space.gravity = (0, 100)
# Intialize the objects
dynamicBalls = []

staticBalls = []
staticBalls.append(createStaticBall(space, (400, 200)))

platforms = []
# Adding these platforms as the borders to store the balls
platforms.append(createPlatform(space, (WIDTH/2, HEIGHT), (WIDTH, 5)))
platforms.append(createPlatform(space, (0, HEIGHT/2), (2, HEIGHT)))
platforms.append(createPlatform(space, (WIDTH, HEIGHT/2), (2, HEIGHT)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Create new falling based on where the mouse is clicked
            dynamicBalls.append(createDynamicBall(space, event.pos))
    
    print('Number of balls: ',len(dynamicBalls))
    screen.fill((217, 217, 217)) # White background
    drawDynamicBall(dynamicBalls)
    drawStaticBall(staticBalls)
    drawPlatform(platforms=platforms)
    # Physics simulation loop
    space.step(1/100) # 0.01
    pygame.display.update()
    clock.tick(120)
