import pygame
import pymunk
import random
import math

ball_colors = {
    1 : (255, 205, 0),
    2 : (0, 0, 205),
    3 : (205, 0, 0),
    4 : (128, 0, 128),
    5 : (255, 102, 0),
    6 : (0, 128, 0),
    7 : (128, 0, 0),
    8 : (0, 0, 0),
    9 : (255, 205, 0),
    10 : (0, 0, 205),
    11 : (205, 0, 0),
    12 : (128, 0, 128),
    13 : (255, 102, 0),
    14 : (0, 128, 0),
    15 : (128, 0, 0)
}

d_width, d_height = 600, 400
t_width, t_height = 478, 232
                     
pocket_radius = 16
t_corner = pocket_radius * 1.1
t_mid = pocket_radius * 2

bezel = pocket_radius * 2

ball_radius = 7

pygame.init()
display = pygame.display.set_mode((d_width, d_height))
clock = pygame.time.Clock()
space = pymunk.Space()

font = pygame.font.SysFont('Arial', 12)

sim_speed = 1
FPS=60

# pymunk 0, 0 is in bottom left
# pygame 0, 0 is in top left
def mtog(x, y):
    return int(x), d_height - int(y)

class Ball():
    def __init__(self, x, y, color = (255, 255, 255), draw_stripe = False, draw_label = False, label = ''):
        self.body = pymunk.Body()
        self.body.position = x, y

        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 25
        self.shape.elasticity = 0.9
        self.shape.collision_type = 1

        self.shape.label = label

        self.color = color
        self.draw_stripe = draw_stripe
        self.draw_label = draw_label

        space.add(self.body, self.shape)
        self.text_surface = font.render(self.shape.label, False, (255, 255, 255))

    def draw(self):
        x, y = self.body.position

        pygame.draw.circle(display, (0, 0, 0), mtog(x, y), ball_radius + 1)
        pygame.draw.circle(display, self.color, mtog(x, y), ball_radius)
        
        if self.draw_stripe:
            pygame.draw.line(display, (255, 255, 255), mtog(x - ball_radius, y), mtog(x + ball_radius, y), 2)

        if self.draw_label:
            text_width, _ = font.size(self.shape.label)
            display.blit(self.text_surface, mtog(x - text_width//2, y + ball_radius))

class Bound():
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0

        self.x1 = x1
        self.y1 = y1

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.shape = pymunk.Segment(self.body, (x0, y0), (x1, y1), 2.5)
        self.shape.elasticity = 0.8

        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.line(display, (84, 57, 29), mtog(self.x0, self.y0), mtog(self.x1, self.y1), 5)

class Pocket():
    def __init__(self, x, y, pos):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y

        self.shape = pymunk.Circle(self.body, pocket_radius - ball_radius)
        self.shape.collision_type = 2
        self.shape.pos = pos
        self.shape.sensor = True

        space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(display, (0, 0, 0), mtog(x, y), pocket_radius)
        #pygame.draw.circle(display, (0, 255, 0), mtog(x, y), pocket_radius - ball_radius) # critical region

def collide(arbiter, space, data):
    a, b = arbiter.shapes
    print(a.label, b.pos)

    return True

def sim():
    balls = [
        Ball(
            random.randint(d_width//2 - t_width//2, d_width//2 + t_width//2),
            random.randint(d_height//2 - t_height//2, d_height//2 + t_height//2), 
            ball_colors[n],
            n > 8,
            True,
            str(n)
        ) for n in ball_colors
    ]

    p1_cue_ball = Ball(random.randint(d_width//2 - t_width//2, d_width//2 + t_width//2), random.randint(d_height//2 - t_height//2, d_height//2 + t_height//2), label='p1')
    p2_cue_ball = Ball(random.randint(d_width//2 - t_width//2, d_width//2 + t_width//2), random.randint(d_height//2 - t_height//2, d_height//2 + t_height//2), label='p2')

    #balls[0].shape.color = (0, 0, 255)

    bounds = [Bound(d_width//2 - t_width//2 + t_corner, d_height//2 + t_height//2, d_width//2 - t_mid//2, d_height//2 + t_height//2),
              Bound(d_width//2 + t_mid//2, d_height//2 + t_height//2, d_width//2 + t_width//2 - t_corner, d_height//2 + t_height//2),
              
              Bound(d_width//2 - t_width//2 + t_corner, d_height//2 - t_height//2, d_width//2 - t_mid//2, d_height//2 - t_height//2),
              Bound(d_width//2 + t_mid//2, d_height//2 - t_height//2, d_width//2 + t_width//2 - t_corner, d_height//2 - t_height//2),
              
              Bound(d_width//2 - t_width//2, d_height//2 + t_height//2 - t_corner, d_width//2 - t_width//2, d_height//2 - t_height//2 + t_corner),
              Bound(d_width//2 + t_width//2, d_height//2 + t_height//2 - t_corner, d_width//2 + t_width//2, d_height//2 - t_height//2 + t_corner)]
    
    pockets = [Pocket(d_width//2 - t_width//2, d_height//2 + t_height//2, 'Top Left'),
               Pocket(d_width//2, d_height//2 + t_height//2 + pocket_radius//2, 'Top Middle'),
               Pocket(d_width//2 + t_width//2, d_height//2 + t_height//2, 'Top Right'),
               Pocket(d_width//2 - t_width//2, d_height//2 - t_height//2, 'Bottom Left'),
               Pocket(d_width//2, d_height//2 - t_height//2 - pocket_radius//2, 'Bottom Middle'),
               Pocket(d_width//2 + t_width//2, d_height//2 - t_height//2, 'Bottom Right')]

    handler = space.add_collision_handler(1, 2)
    handler.begin = collide

    p1_cue_ball.body.apply_impulse_at_local_point((1000000,0),(0,0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        display.fill((255, 255, 255))

        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(d_width//2 - t_width//2 - bezel - 5, d_height//2 - t_height//2 - bezel - 5, t_width + bezel * 2 + 10, t_height + bezel * 2 + 10))
        pygame.draw.rect(display, (101, 67, 33), pygame.Rect(d_width//2 - t_width//2 - bezel, d_height//2 - t_height//2 - bezel, t_width + bezel * 2, t_height + bezel * 2))
        pygame.draw.rect(display, (0, 128, 0), pygame.Rect(d_width//2 - t_width//2, d_height//2 - t_height//2, t_width, t_height))

        [pocket.draw() for pocket in pockets]
        [bound.draw() for bound in bounds]
        [ball.draw() for ball in balls]

        p1_cue_ball.draw()
        p2_cue_ball.draw()

        pygame.display.update()
        clock.tick(FPS * sim_speed)

        for _ in range(sim_speed):
            for ball in [p1_cue_ball, p2_cue_ball] + balls:

                friction_force = (ball.body.mass * 9.81) * 0.8
                dir = -pymunk.Vec2d.normalized(ball.body.velocity)
                ball.body.apply_force_at_local_point((friction_force * dir.x, friction_force * dir.y), (0,0))



            space.step(1/(FPS * sim_speed))

sim()
pygame.quit()