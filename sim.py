import pygame
import pymunk
import random
import numpy as np

BALL_COLORS = {
    '1' : (255, 205, 0),
    '2' : (0, 0, 205),
    '3' : (205, 0, 0),
    '4' : (128, 0, 128),
    '5' : (255, 102, 0),
    '6' : (0, 128, 0),
    '7' : (128, 0, 0),
    '9' : (255, 205, 0),
    '10' : (0, 0, 205),
    '11' : (205, 0, 0),
    '12' : (128, 0, 128),
    '13' : (255, 102, 0),
    '14' : (0, 128, 0),
    '15' : (128, 0, 0)
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

def pretty_print_state(state):
    out = ''
    for label in state:
        out += label + '\n'
        for key in state[label]:
            val = state[label][key]
            out += '\t' + key + '\t: ' + str(val) + '\n'
    print(out)
        
# pymunk 0, 0 is in bottom left
# pygame 0, 0 is in top left
def mtog(x, y):
    return int(x), WINDOW_HEIGHT - int(y)

def stom(pos):
    x, y = pos
    return (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + x, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + y)

class Ball():
    def __init__(self, space, pos, color = (255, 255, 255), draw_stripe = False, draw_label = False, label = '', sunk = None):
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
            'draw_label': draw_label,
            'sunk': sunk
        }

        space.add(self.body, self.shape)

    def step(self):
        friction_force = (self.body.mass * 9.81) * 0.8
        dir = -pymunk.Vec2d.normalized(self.body.velocity)
        self.body.apply_force_at_local_point((friction_force * dir.x, friction_force * dir.y), (0,0))

    def draw(self, display):
        if self.shape.custom['sunk']:
            return

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
            'bounds': [
                Bound(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + TABLE_CORNER, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS), (WINDOW_WIDTH//2 - TABLE_MID//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 + TABLE_MID//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 - TABLE_CORNER, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + TABLE_CORNER, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS), (WINDOW_WIDTH//2 - TABLE_MID//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 + TABLE_MID//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 - TABLE_CORNER, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)),
                Bound(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TRIM_RADIUS, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 - TABLE_CORNER), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TRIM_RADIUS, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + TABLE_CORNER)),
                Bound(self.space, (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TRIM_RADIUS, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 - TABLE_CORNER), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TRIM_RADIUS, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + TABLE_CORNER))
            ],
            'pockets': [
                Pocket(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2), 'Top Left'),
                Pocket(self.space, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + POCKET_RADIUS//2), 'Top Middle'),
                Pocket(self.space, (WINDOW_WIDTH//2 + TABLE_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2), 'Top Right'),
                Pocket(self.space, (WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2), 'Bottom Left'),
                Pocket(self.space, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - POCKET_RADIUS//2), 'Bottom Middle'),
                Pocket(self.space, (WINDOW_WIDTH//2 + TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2), 'Bottom Right')
            ],
            'balls': [
                Ball(self.space, stom(state['p1']['pos']), label='p1', sunk=state['p1']['sunk']),
                Ball(self.space, stom(state['p2']['pos']), label='p2', sunk=state['p2']['sunk']),

                Ball(self.space, stom(state['1']['pos']), BALL_COLORS['1'], False, True, label='1', sunk=state['1']['sunk']),
                Ball(self.space, stom(state['2']['pos']), BALL_COLORS['2'], False, True, label='2', sunk=state['2']['sunk']),
                Ball(self.space, stom(state['3']['pos']), BALL_COLORS['3'], False, True, label='3', sunk=state['3']['sunk']),
                Ball(self.space, stom(state['4']['pos']), BALL_COLORS['4'], False, True, label='4', sunk=state['4']['sunk']),
                Ball(self.space, stom(state['5']['pos']), BALL_COLORS['5'], False, True, label='5', sunk=state['5']['sunk']),
                Ball(self.space, stom(state['6']['pos']), BALL_COLORS['6'], False, True, label='6', sunk=state['6']['sunk']),
                Ball(self.space, stom(state['7']['pos']), BALL_COLORS['7'], False, True, label='7', sunk=state['7']['sunk']),

                Ball(self.space, stom(state['9']['pos']), BALL_COLORS['9'], True, True, label='9', sunk=state['9']['sunk']),
                Ball(self.space, stom(state['10']['pos']), BALL_COLORS['10'], True, True, label='10', sunk=state['10']['sunk']),
                Ball(self.space, stom(state['11']['pos']), BALL_COLORS['11'], True, True, label='11', sunk=state['11']['sunk']),
                Ball(self.space, stom(state['12']['pos']), BALL_COLORS['12'], True, True, label='12', sunk=state['12']['sunk']),
                Ball(self.space, stom(state['13']['pos']), BALL_COLORS['13'], True, True, label='13', sunk=state['13']['sunk']),
                Ball(self.space, stom(state['14']['pos']), BALL_COLORS['14'], True, True, label='14', sunk=state['14']['sunk']),
                Ball(self.space, stom(state['15']['pos']), BALL_COLORS['15'], True, True, label='15', sunk=state['15']['sunk'])
            ]
        }

        self.players = ['p1', 'p2']

        handler = self.space.add_collision_handler(1, 2)
        handler.begin = self.collide

    def collide(self, arbiter, space, data):
        ball, bound = arbiter.shapes
        print(ball.custom['label'], bound.custom['label'])

        return True

    def reflect(self, ray, hit, n):
        # where vec is the vec that hit this surface, hit is the hitinfo, reflect is the number of remaining relections
        #if reflect > 0

        if n == 0:
            return ray, hit

        CAST_LEN = 10000

        norm = np.array([hit.normal.x, hit.normal.y])
        pos = np.array([hit.point.x, hit.point.y])
        ray /= np.linalg.norm(ray)

        v = ray - 2*(np.dot(ray, norm))*norm
        v /= np.linalg.norm(v)

        r_v = np.array([v[1] * BALL_RADIUS, -v[0] * BALL_RADIUS])

        filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS())

        mid_start = tuple(pos)
        mid_end = tuple(pos + v*CAST_LEN)
        mid_hit = self.space.segment_query_first(mid_start, mid_end, 1, filter)

        top_start = tuple(pos + r_v)
        top_end = tuple(pos + r_v + v*CAST_LEN)
        top_hit = self.space.segment_query_first(top_start, top_end, 1, filter)

        bottom_start = tuple(pos - r_v)
        bottom_end = tuple(pos - r_v + v*CAST_LEN)
        bottom_hit = self.space.segment_query_first(bottom_start, bottom_end, 1, filter)

        print(mid_hit.point)

        flag = False
        if top_hit:
            if top_hit.shape != None:
                if top_hit.shape.collision_type == 1:
                    flag = True
        
        if not flag and bottom_hit:
            if bottom_hit.shape != None:
                if bottom_hit.shape.collision_type == 1:
                    flag = True

        if not flag and mid_hit:
            if mid_hit.shape != None:
                if mid_hit.shape.collision_type != 1:
                    return self.reflect(v, mid_hit, n - 1)
                
        return None, None

    def scan(self, ball): # solve for an input

        CAST_LEN = 10000

        theta = 0
        bounces = 0 # start with 0 bounces, then 1 bounce allowed, up to 2

        prev_filter = ball.shape.filter
        ball.shape.filter = pymunk.ShapeFilter(categories=0b10)

        while theta <= 2*np.pi:
            pos = ball.body.position
            filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS()^0b10)

            v = np.array([np.cos(theta), np.sin(theta)])
            r_v = np.array([v[1] * BALL_RADIUS, -v[0] * BALL_RADIUS])

            mid_start = pos
            mid_end = pos + v*CAST_LEN
            mid_hit = self.space.segment_query_first(mid_start, mid_end, 1, filter)

            top_start = pos + r_v
            top_end = pos + r_v + v*CAST_LEN
            top_hit = self.space.segment_query_first(top_start, top_end, 1, filter)

            bottom_start = pos - r_v
            bottom_end = pos - r_v + v*CAST_LEN
            bottom_hit = self.space.segment_query_first(bottom_start, bottom_end, 1, filter)

            flag = False
            if top_hit:
                if top_hit.shape != None:
                    if top_hit.shape.collision_type == 1:
                        flag = True
            
            if not flag and bottom_hit:
                if bottom_hit.shape != None:
                    if bottom_hit.shape.collision_type == 1:
                        flag = True

            if not flag and mid_hit:
                if mid_hit.shape != None:
                    if mid_hit.shape.collision_type != 1:
                        ball.shape.filter = prev_filter
                        return theta, mid_hit

            theta += np.pi/16
        
        ball.shape.filter = prev_filter
        return -1, None

    def move(self, pos, theta, power, placements):
        #print(theta)

        ball = self.geometry['balls'][0]

        theta, hit = self.scan(ball)

        impulse = (np.cos(theta) * 1000000, np.sin(theta) * 1000000)

        test_ray, test_hit = self.reflect(impulse, hit, 1)

        ball.body.apply_impulse_at_local_point(impulse,(0,0))




        while True:
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
                        #if group == 'balls':
                        #    if obj.shape.custom['sunk'] != None:
                        #        continue
                        obj.draw(self.display)


                # TODO: just messing around
                if True:
                #    pygame.draw.line(self.display, (255,0,0), mtog(pos[0], pos[1]), mtog(point[0], point[1]), 1)
                #    pygame.draw.line(self.display, (0, 0, 255), mtog(point[0], point[1]), mtog(point[0] + norm[0] * 10, point[1] + norm[1] * 10))

                    print(mtog(test_hit.point[0], test_hit.point[1]), test_hit.shape)
                    pygame.draw.line(self.display, (255,0,0), mtog(test_hit.point[0], test_hit.point[1]), mtog(test_hit.point[0] + test_ray[0], test_hit.point[1] + test_ray[1]), 1)
                #    vec = point - pos

                    #r =

                    #print(math.degrees(math.pi - norm.get_angle_between(vec)))

                pygame.display.update()
                self.clock.tick(FPS * SIM_SPEED)

            for _ in range(SIM_SPEED):
                for group in self.geometry:
                    for obj in self.geometry[group]:
                        if group == 'balls':
                            if obj.shape.custom['sunk'] != None:
                                continue
                        obj.step()
                self.space.step(1/(FPS * SIM_SPEED))

            delta = False
            for group in self.geometry:
                for obj in self.geometry[group]:
                    if group == 'balls':
                        if obj.shape.custom['sunk'] != None:
                            continue
                    if obj.body.velocity.length > 0.25:
                        delta = True
                        break
                if delta:
                    break
            
            if not delta:
                break
        
        state = {}
        for ball in self.geometry['balls']:
            state[ball.shape.custom['label']] = {
                'sunk' : ball.shape.custom['sunk'],
                'pos' : (ball.body.position.x, ball.body.position.y)
            }

        return state
            
def random_pos(p1):
    (x0, y0), (x1, y1) = P1_BOUNDS if p1 else P2_BOUNDS
    return (x0 + random.random() * (x1 - x0), y0 + random.random() * (y1 - y0))

def run():
    init_state = {
        'p1' : {'sunk': None, 'pos': random_pos(True)},
        'p2' : {'sunk': None, 'pos': random_pos(False)},
        '1' : {'sunk': None, 'pos': random_pos(True)},
        '2' : {'sunk': None, 'pos': random_pos(True)},
        '3' : {'sunk': None, 'pos': random_pos(True)},
        '4' : {'sunk': None, 'pos': random_pos(True)},
        '5' : {'sunk': None, 'pos': random_pos(True)},
        '6' : {'sunk': None, 'pos': random_pos(True)},
        '7' : {'sunk': None, 'pos': random_pos(True)},
        '9' : {'sunk': None, 'pos': random_pos(False)},
        '10' : {'sunk': None, 'pos': random_pos(False)},
        '11' : {'sunk': None, 'pos': random_pos(False)},
        '12' : {'sunk': None, 'pos': random_pos(False)},
        '13' : {'sunk': None, 'pos': random_pos(False)},
        '14' : {'sunk': None, 'pos': random_pos(False)},
        '15' : {'sunk': None, 'pos': random_pos(False)}
    }
    
    sim = Sim(init_state, draw=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
        state = sim.move(None, None, None, None)
        #pretty_print_state(state)

        for label in state:
            if state[label]['sunk'] is not None:
                print(label)

'''
    TODO
    - allow to init with sunk balls
    - include turns
    - move should include a dict with placement positions for balls sunk in middle
    - implement mutliple shots if you knock ball in outer pockets / scratches
'''