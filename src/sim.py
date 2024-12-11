from objects.ball import Ball
from objects.bound import Bound
from objects.pocket import Pocket

from draw import Draw
import util

# constants
from const import *

# lib
import pymunk
import random
import numpy as np

class Simulation():

    @staticmethod
    def state_to_pymunk(pos):
        x, y = pos
        return (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + x, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + y)

    @staticmethod
    def pymunk_to_state(pos):
        x, y = pos
        return (-WINDOW_WIDTH//2 + TABLE_WIDTH//2 + x, -WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + y) 

    @staticmethod
    def pocket_collide(arbiter, space, data):
        ball, bound = arbiter.shapes
        ball.custom['sunk'] = bound.custom['label']
        return True
    
    @staticmethod
    def ball_collide(arbiter, space, data):
        ball_a, ball_b = arbiter.shapes
        if ball_a.custom['sunk'] or ball_b.custom['sunk']:
            return False
        return True

    @staticmethod
    def is_point_in_bounds(point, player):
        if player == 1:
            return point[0] < Simulation.state_to_pymunk(P1_BOUNDS[1])[0]
        else:
            return point[0] > Simulation.state_to_pymunk(P2_BOUNDS[0])[0]
        
    @staticmethod
    def is_point_in_shoot_bounds(point, player):
        if player == 1:
            return point[0] < Simulation.state_to_pymunk(P1_SHOOT_BOUNDS[1])[0]
        else:
            return point[0] > Simulation.state_to_pymunk(P2_SHOOT_BOUNDS[0])[0]

    @staticmethod
    def is_closest_point(p1, p2, player):
        if player == 1:
            return p1[0] > p2[0]
        else:
            return p1[0] < p2[0]

    def __init__(self, draw=-1):
        self.space = pymunk.Space()

        if draw == -1:
            self.draw = None
        elif draw == 0:
            self.draw = Draw(False)
        elif draw == 1:
            self.draw = Draw(True)
        

        self.geometry = {
            'bounds': [
                Bound(self.space, BOUND_1_START, BOUND_1_END),
                Bound(self.space, BOUND_2_START, BOUND_2_END),
                Bound(self.space, BOUND_3_START, BOUND_3_END),
                Bound(self.space, BOUND_4_START, BOUND_4_END),
                Bound(self.space, BOUND_5_START, BOUND_5_END),
                Bound(self.space, BOUND_6_START, BOUND_6_END)
            ],
            'pockets': [
                Pocket(self.space, POCKET_1_POS, 'Top Left'),
                Pocket(self.space, POCKET_2_POS, 'Top Middle'),
                Pocket(self.space, POCKET_3_POS, 'Top Right'),
                Pocket(self.space, POCKET_4_POS, 'Bottom Left'),
                Pocket(self.space, POCKET_5_POS, 'Bottom Middle'),
                Pocket(self.space, POCKET_6_POS, 'Bottom Right')
            ],
            'balls': [
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='p1', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='p2', sunk=None),

                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='1', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='2', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='3', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='4', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='5', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='6', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(True)), label='7', sunk=None),

                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='9', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='10', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='11', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='12', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='13', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='14', sunk=None),
                Ball(self.space, Simulation.state_to_pymunk(util.random_pos(False)), label='15', sunk=None)
            ]
        }

        pocket_handler = self.space.add_collision_handler(1, 2)
        pocket_handler.begin = Simulation.pocket_collide

        ball_handler = self.space.add_collision_handler(1, 1)
        ball_handler.begin = Simulation.ball_collide

    def reflect(self, ray, hit, player):
        norm = np.array([hit.normal.x, hit.normal.y])
        pos = np.array([hit.point.x, hit.point.y]) + norm * BALL_RADIUS
        ray /= np.linalg.norm(ray)

        v = ray - (1+BALL_ELASTICITY*BOUND_ELASTICITY)*(np.dot(ray, norm))*norm
        v /= np.linalg.norm(v)

        r_v = np.array([v[1] * BALL_RADIUS, -v[0] * BALL_RADIUS])

        filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS()^RAYCAST_IGNORE)

        mid_start = tuple(pos)
        mid_end = tuple(pos + v*RAYCAST_LEN)
        mid_hit = self.space.segment_query_first(mid_start, mid_end, 1, filter)

        top_start = tuple(pos + r_v)
        top_end = tuple(pos + r_v + v*RAYCAST_LEN)
        top_hit = self.space.segment_query_first(top_start, top_end, 1, filter)

        bottom_start = tuple(pos - r_v)
        bottom_end = tuple(pos - r_v + v*RAYCAST_LEN)
        bottom_hit = self.space.segment_query_first(bottom_start, bottom_end, 1, filter)
        
        point = None
        if top_hit:
            top_point = np.array([top_hit.point.x, top_hit.point.y]) - r_v
            point = top_point
        if bottom_hit:
            bottom_point = np.array([bottom_hit.point.x, bottom_hit.point.y]) + r_v
            if point is None or (point is not None and Simulation.is_closest_point(bottom_point, point, player)):
                point = bottom_point
        if mid_hit:
            mid_point = np.array([mid_hit.point.x + BALL_RADIUS*player, mid_hit.point.y])
            if point is None or (point is not None and Simulation.is_closest_point(mid_point, point, player)):
                point = mid_point

        if point is not None and Simulation.is_point_in_shoot_bounds(point, player):
            return v, point
        
        return None, None

    def scan(self, ball, player):
        player_ball = self.get_ball('p1' if player == 1 else 'p2')
        
        prev_filter = ball.shape.filter
        prev_player_filter = player_ball.shape.filter

        ball.shape.filter = pymunk.ShapeFilter(categories=RAYCAST_IGNORE)
        player_ball.shape.filter = pymunk.ShapeFilter(categories=RAYCAST_IGNORE)

        theta = 0
        while theta <= 2*np.pi:
            pos = ball.body.position
            filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS()^RAYCAST_IGNORE)

            v = np.array([np.cos(theta), np.sin(theta)])
            r_v = np.array([v[1] * BALL_RADIUS, -v[0] * BALL_RADIUS])

            mid_start = pos
            mid_end = pos + v*RAYCAST_LEN
            mid_hit = self.space.segment_query_first(mid_start, mid_end, 1, filter)

            top_start = pos + r_v
            top_end = pos + r_v + v*RAYCAST_LEN
            top_hit = self.space.segment_query_first(top_start, top_end, 1, filter)

            bottom_start = pos - r_v
            bottom_end = pos - r_v + v*RAYCAST_LEN
            bottom_hit = self.space.segment_query_first(bottom_start, bottom_end, 1, filter)

            point = None
            can_reflect = True

            if top_hit:
                if top_hit.shape and top_hit.shape.collision_type == 1:
                    can_reflect = False
                top_point = np.array([top_hit.point.x, top_hit.point.y]) - r_v
                point = top_point
            if bottom_hit:
                if bottom_hit.shape and bottom_hit.shape.collision_type == 1:
                    can_reflect = False
                bottom_point = np.array([bottom_hit.point.x, bottom_hit.point.y]) + r_v
                if point is None or (point is not None and Simulation.is_closest_point(bottom_point, point, player)):
                    point = bottom_point
            if mid_hit:
                if mid_hit.shape and mid_hit.shape.collision_type == 1:
                    can_reflect = False
                mid_point = np.array([mid_hit.point.x - BALL_RADIUS, mid_hit.point.y])
                if point is None or (point is not None and Simulation.is_closest_point(mid_point, point, player)):
                    point = mid_point
            
            if point is not None and Simulation.is_point_in_shoot_bounds(point, player):
                ball.shape.filter = prev_filter
                player_ball.shape.filter = prev_player_filter
                return v, point
            else:
                if can_reflect and mid_hit:
                    v, reflect_point = self.reflect(v, mid_hit, player)

                    if reflect_point is not None:
                        ball.shape.filter = prev_filter
                        player_ball.shape.filter = prev_player_filter
                        return v, reflect_point
            theta += np.pi/32
        
        ball.shape.filter = prev_filter
        player_ball.shape.filter = prev_player_filter
        return None, None

    def set_state(self, state):
        for ball_label in state:
            ball = self.get_ball(ball_label)
            ball.shape.custom['sunk'] = state[ball_label]['sunk']
            ball.body.position = self.state_to_pymunk(state[ball_label]['pos'])
            ball.body.velocity = (0,0)
            self.space.step(5)

    def actions(self, state, player):
        self.set_state(state)

        # get the discrete points: all non-sunk balls not on the players side
        balls = []
        for ball in self.geometry['balls']:
            if ball.shape.custom['label'] in ['p1', 'p2'] or ball.shape.custom['sunk']:
                continue
            if not Simulation.is_point_in_bounds(ball.body.position, player):
                balls.append(ball)

        actions = []
        for ball in balls:
            dir, origin = self.scan(ball, player)
            if dir is None:
                continue
            for power in [500000, 750000, 1000000]:
                actions.append((dir,origin,power))

        if len(actions) == 0:
            theta = random.random()*2*np.pi
            dir = (np.cos(theta), np.sin(theta))
            origin = util.random_pos(player, True)
            power = 1000000
            actions.append((dir,origin,power))

        return actions

    def get_ball(self, label):
        for ball in self.geometry['balls']:
            if ball.shape.custom['label'] == label:
                return ball
        return None

    def move(self, state, player, dir, origin, power):
        self.set_state(state)

        player_ball = self.get_ball('p1' if player == 1 else 'p2')

        # if the player's ball is sunk then we will make it un-sunk
        if player_ball.shape.custom['sunk']:
            player_ball.shape.custom['sunk'] = None

        impulse = (-dir[0] * power, -dir[1] * power)

        player_ball.body.position = (origin[0], origin[1]) # small offset
        player_ball.body.apply_impulse_at_local_point(impulse,(0,0))

        while True:
            if self.draw:
                self.draw.draw_frame(self.geometry)

            for _ in range(SIM_SPEED):
                for group in self.geometry:
                    for obj in self.geometry[group]:
                        if group == 'balls':
                            if obj.shape.custom['sunk']:
                                continue
                        obj.step()
                self.space.step(1/(FPS * SIM_SPEED))

            delta = False
            for group in self.geometry:
                for obj in self.geometry[group]:
                    if group == 'balls':
                        if obj.shape.custom['sunk']:
                            continue
                    if obj.body.velocity.length > 0.25:
                        delta = True
                        break
                if delta:
                    break
            if not delta:
                break
        
        new_state = {}
        for ball in self.geometry['balls']:
            new_state[ball.shape.custom['label']] = {
                'sunk' : ball.shape.custom['sunk'],
                'pos' : Simulation.pymunk_to_state((ball.body.position.x, ball.body.position.y))
            }

        return new_state
