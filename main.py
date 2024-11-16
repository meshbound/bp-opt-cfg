import pygame
import pymunk
import random
import math

BALL_COLORS = {
    1 : (255, 205, 0),
    2 : (0, 0, 205),
    3 : (205, 0, 0),
    4 : (128, 0, 128),
    5 : (255, 102, 0),
    6 : (0, 128, 0),
    7 : (128, 0, 0),
    9 : (255, 205, 0),
    10 : (0, 0, 205),
    11 : (205, 0, 0),
    12 : (128, 0, 128),
    13 : (255, 102, 0),
    14 : (0, 128, 0),
    15 : (128, 0, 0)
}

# table
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
TABLE_WIDTH, TABLE_HEIGHT = 478, 232
       
POCKET_RADIUS = 16
TABLE_CORNER = POCKET_RADIUS
TABLE_MID = POCKET_RADIUS * 2

TABLE_BEZEL = POCKET_RADIUS * 2
MARK_RADIUS = 3 
TRIM_RADIUS = 2

# ball
BALL_RADIUS = 7

P1_BOUNDS = ((BALL_RADIUS, BALL_RADIUS), (3*TABLE_WIDTH//8, TABLE_HEIGHT - BALL_RADIUS))
P2_BOUNDS = ((5*TABLE_WIDTH//8, BALL_RADIUS), (TABLE_WIDTH - BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS))

# sim
SIM_SPEED = 1
FPS=60

pygame.init()

font = pygame.font.SysFont('Arial', 12)

# pymunk 0, 0 is in bottom left
# pygame 0, 0 is in top left
def mtog(x, y): # TODO: make this take a tuple instead
    return int(x), WINDOW_HEIGHT - int(y)

def stom(pos):
    x, y = pos
    return (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + x, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + y)


class Ball():
    def __init__(self, space, pos, color = (255, 255, 255), draw_stripe = False, draw_label = False, label = ''):
        # body
        self.body = pymunk.Body()
        self.body.position = pos

        # shape
        self.shape = pymunk.Circle(self.body, BALL_RADIUS)
        self.shape.density = 25
        self.shape.elasticity = 0.9
        self.shape.collision_type = 1

        # custom
        self.shape.custom = {
            'label': label,
            'color': color,
            'draw_stripe': draw_stripe,
            'draw_label': draw_label
        }

        space.add(self.body, self.shape)

    def step(self):
        friction_force = (self.body.mass * 9.81) * 0.8
        dir = -pymunk.Vec2d.normalized(self.body.velocity)
        self.body.apply_force_at_local_point((friction_force * dir.x, friction_force * dir.y), (0,0))

    def draw(self, display):
        x, y = self.body.position

        # circle with outline
        pygame.draw.circle(display, (0, 0, 0), mtog(x, y), BALL_RADIUS + 1)
        pygame.draw.circle(display, self.shape.custom['color'], mtog(x, y), BALL_RADIUS)
        
        if self.shape.custom['draw_stripe']:
            pygame.draw.line(display, (255, 255, 255), mtog(x - BALL_RADIUS, y), mtog(x + BALL_RADIUS, y), 2)

        if self.shape.custom['draw_label']:
            text_width, _ = font.size(self.shape.custom['label'])

            text_surface = font.render(
                self.shape.custom['label'],
                False,
                (255, 255, 255)
            )

            display.blit(text_surface, mtog(x - text_width//2, y + BALL_RADIUS))

class Bound():
    def __init__(self, space, start, end):
        # body
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        # shpae
        self.shape = pymunk.Segment(self.body, start, end, TRIM_RADIUS)
        self.shape.elasticity = 0.8

        # custom
        self.shape.custom = {
            'start': start,
            'end': end
        }

        space.add(self.body, self.shape)

    def step(self):
        pass

    def draw(self, display):
        x0, y0 = self.shape.custom['start']
        x1, y1 = self.shape.custom['end']

        pygame.draw.line(display, (84, 57, 29), mtog(x0, y0), mtog(x1, y1), TRIM_RADIUS * 2)

class Pocket():
    def __init__(self, space, pos, label):
        # body
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos

        # shape
        self.shape = pymunk.Circle(self.body, POCKET_RADIUS - BALL_RADIUS)
        self.shape.collision_type = 2
        self.shape.sensor = True

        # custom
        self.shape.custom = {
            'label': label
        }

        space.add(self.body, self.shape)

    def step(self):
        pass

    def draw(self, display):
        x, y = self.body.position
        pygame.draw.circle(display, (0, 0, 0), mtog(x, y), POCKET_RADIUS)
        #pygame.draw.circle(display, (0, 255, 0), mtog(x, y), POCKET_RADIUS - BALL_RADIUS) # critical region     

class Sim():
    def __init__(self, state, draw=False):
        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()

        self.draw = draw
        if draw:
            self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.geometry = {
            "bounds": [
                Bound(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + TABLE_CORNER, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS), (WINDOW_WIDTH//2 - TABLE_MID//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 + TABLE_MID//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 - TABLE_CORNER, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + TABLE_CORNER, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS), (WINDOW_WIDTH//2 - TABLE_MID//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 + TABLE_MID//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 - TABLE_CORNER, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TRIM_RADIUS, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 - TABLE_CORNER), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TRIM_RADIUS, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + TABLE_CORNER)),
                Bound(self.space, (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TRIM_RADIUS, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 - TABLE_CORNER), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TRIM_RADIUS, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + TABLE_CORNER))
            ],
            "pockets": [
                Pocket(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2), 'Top Left'),
                Pocket(self.space, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + POCKET_RADIUS//2), 'Top Middle'),
                Pocket(self.space, (WINDOW_WIDTH//2 + TABLE_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2), 'Top Right'),
                Pocket(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2), 'Bottom Left'),
                Pocket(self.space, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - POCKET_RADIUS//2), 'Bottom Middle'),
                Pocket(self.space, (WINDOW_WIDTH//2 + TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2), 'Bottom Right')
            ],
            "balls": [
                Ball(
                    self.space,
                    stom(state[n]), 
                    BALL_COLORS[n],
                    n > 8,
                    True,
                    str(n)
                ) for n in BALL_COLORS
            ],
            "p1": [
                Ball(self.space, (random.randint(WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_WIDTH//2 + TABLE_WIDTH//2), random.randint(WINDOW_HEIGHT//2 - TABLE_HEIGHT//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2)), label='p1')
            ],
            "p2": [
                Ball(self.space, (random.randint(WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_WIDTH//2 + TABLE_WIDTH//2), random.randint(WINDOW_HEIGHT//2 - TABLE_HEIGHT//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2)), label='p2')
            ]
        }

        handler = self.space.add_collision_handler(1, 2)
        handler.begin = Sim.collide

    @staticmethod
    def collide(arbiter, space, data):
        a, b = arbiter.shapes
        print(a.custom['label'], b.custom['label'])

        return True

    def move(self):
        self.geometry["p1"][0].body.apply_impulse_at_local_point((1000000,0),(0,0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if self.draw:
                self.display.fill((255, 255, 255))
                pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL - 5, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL - 5, TABLE_WIDTH + TABLE_BEZEL * 2 + 10, TABLE_HEIGHT + TABLE_BEZEL * 2 + 10))
                pygame.draw.rect(self.display, (101, 67, 33), pygame.Rect(WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL, TABLE_WIDTH + TABLE_BEZEL * 2, TABLE_HEIGHT + TABLE_BEZEL * 2))
                pygame.draw.rect(self.display, (0, 128, 0), pygame.Rect(WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2, TABLE_WIDTH, TABLE_HEIGHT))

                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//4, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//4, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)

                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//4, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//4, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)

                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//4), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//4), MARK_RADIUS)

                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//4), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2), MARK_RADIUS)
                pygame.draw.circle(self.display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//4), MARK_RADIUS)

                for group in self.geometry:
                    for obj in self.geometry[group]:
                        obj.draw(self.display)
                        pass

                pygame.display.update()
                self.clock.tick(FPS * SIM_SPEED)

            for _ in range(SIM_SPEED):
                for group in self.geometry:
                    for obj in self.geometry[group]:
                        obj.step()
                self.space.step(1/(FPS * SIM_SPEED))


            delta = False
            for group in self.geometry:
                for obj in self.geometry[group]:
                    if obj.body.velocity.length > 0.25:
                        delta = True
                        break
                if delta:
                    break
            
            if not delta:
                break


#(random.randint(WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_WIDTH//2 + TABLE_WIDTH//2), random.randint(WINDOW_HEIGHT//2 - TABLE_HEIGHT//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2))

pos1, pos2 = P1_BOUNDS
pos3, pos4 = P2_BOUNDS

def random_pos(p1):
    (x0, y0), (x1, y1) = P1_BOUNDS if p1 else P2_BOUNDS
    return (random.randint(x0, x1), random.randint(y0, y1))

state = {
    1 : random_pos(True),
    2 : random_pos(True),
    3 : random_pos(True),
    4 : random_pos(True),
    5 : random_pos(True),
    6 : random_pos(True),
    7 : random_pos(True),
    9 : random_pos(False),
    10 : random_pos(False),
    11 : random_pos(False),
    12 : random_pos(False),
    13 : random_pos(False),
    14 : random_pos(False),
    15 : random_pos(False)
}

sim = Sim(state, draw=True)
sim.move()

pygame.quit()