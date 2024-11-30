from objects.ball import Ball
from objects.bound import Bound
from objects.pocket import Pocket

from draw import Draw
from util import *

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
        if ball_a.custom['sunk'] != None or ball_b.custom['sunk'] != None:
            return False
        return True

    def __init__(self, state, draw=False):
        self.space = pymunk.Space()
        self.draw = draw
        self.turn = 'p1'

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
                Ball(self.space, Simulation.state_to_pymunk(state['p1']['pos']), label='p1', sunk=state['p1']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['p2']['pos']), label='p2', sunk=state['p2']['sunk']),

                Ball(self.space, Simulation.state_to_pymunk(state['1']['pos']), label='1', sunk=state['1']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['2']['pos']), label='2', sunk=state['2']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['3']['pos']), label='3', sunk=state['3']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['4']['pos']), label='4', sunk=state['4']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['5']['pos']), label='5', sunk=state['5']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['6']['pos']), label='6', sunk=state['6']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['7']['pos']), label='7', sunk=state['7']['sunk']),

                Ball(self.space, Simulation.state_to_pymunk(state['9']['pos']), label='9', sunk=state['9']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['10']['pos']), label='10', sunk=state['10']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['11']['pos']), label='11', sunk=state['11']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['12']['pos']), label='12', sunk=state['12']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['13']['pos']), label='13', sunk=state['13']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['14']['pos']), label='14', sunk=state['14']['sunk']),
                Ball(self.space, Simulation.state_to_pymunk(state['15']['pos']), label='15', sunk=state['15']['sunk'])
            ]
        }

        pocket_handler = self.space.add_collision_handler(1, 2)
        pocket_handler.begin = Simulation.pocket_collide

        ball_handler = self.space.add_collision_handler(1, 1)
        ball_handler.begin = Simulation.ball_collide

    def reflect(self, ray, hit):
        CAST_LEN = 10000

        norm = np.array([hit.normal.x, hit.normal.y])
        pos = np.array([hit.point.x, hit.point.y]) + norm * BALL_RADIUS
        ray /= np.linalg.norm(ray)

        v = ray - (1+BALL_ELASTICITY*BOUND_ELASTICITY)*(np.dot(ray, norm))*norm
        v /= np.linalg.norm(v)

        r_v = np.array([v[1] * BALL_RADIUS, -v[0] * BALL_RADIUS])

        filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS()^0b10)

        mid_start = tuple(pos)
        mid_end = tuple(pos + v*CAST_LEN)
        mid_hit = self.space.segment_query_first(mid_start, mid_end, 1, filter)

        top_start = tuple(pos + r_v)
        top_end = tuple(pos + r_v + v*CAST_LEN)
        top_hit = self.space.segment_query_first(top_start, top_end, 1, filter)

        bottom_start = tuple(pos - r_v)
        bottom_end = tuple(pos - r_v + v*CAST_LEN)
        bottom_hit = self.space.segment_query_first(bottom_start, bottom_end, 1, filter)

        point = None
        if top_hit:
            top_point = np.array([top_hit.point.x, top_hit.point.y]) - r_v
            point = top_point
        if bottom_hit:
            bottom_point = np.array([bottom_hit.point.x, bottom_hit.point.y]) + r_v
            if point is None or (point is not None and bottom_point[0] < point[0]):
                point = bottom_point
        if mid_hit:
            mid_point = np.array([mid_hit.point.x - BALL_RADIUS, mid_hit.point.y])
            if point is None or (point is not None and mid_point[0] < point[0]):
                point = mid_point

        if point is not None and point[0] > Simulation.state_to_pymunk(P2_SHOOT_BOUNDS[0])[0]:
            return v, point
        
        return None, None

    def scan(self, ball, player_ball):
        CAST_LEN = 10000

        theta = 0

        prev_filter = ball.shape.filter
        prev_player_filter = player_ball.shape.filter

        ball.shape.filter = pymunk.ShapeFilter(categories=0b10)
        player_ball.shape.filter = pymunk.ShapeFilter(categories=0b10)

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
                if point is None or (point is not None and bottom_point[0] < point[0]):
                    point = bottom_point
            if mid_hit:
                if mid_hit.shape and mid_hit.shape.collision_type == 1:
                    can_reflect = False
                mid_point = np.array([mid_hit.point.x - BALL_RADIUS, mid_hit.point.y])
                if point is None or (point is not None and mid_point[0] < point[0]):
                    point = mid_point
            
            if point is not None and point[0] > Simulation.state_to_pymunk(P2_SHOOT_BOUNDS[0])[0]:
                ball.shape.filter = prev_filter
                player_ball.shape.filter = prev_player_filter
                return v, point
            else:
                if can_reflect and mid_hit:
                    v, reflect_point = self.reflect(v, mid_hit)

                    if reflect_point is not None:
                        ball.shape.filter = prev_filter
                        player_ball.shape.filter = prev_player_filter
                        return v, reflect_point
            theta += np.pi/32
        
        ball.shape.filter = prev_filter
        player_ball.shape.filter = prev_player_filter
        return None, None

    def move(self, dir, origin, power):
        player_ball = self.geometry['balls'][1]

        impulse = (-dir[0] * power, -dir[1] * power)

        player_ball.body.position = (origin[0], origin[1] + 0.5) # use a small random offset for the y direction
        player_ball.body.apply_impulse_at_local_point(impulse,(0,0))

        while True:
            if self.draw:
                Draw.draw_frame(self.geometry)

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
                'pos' : Simulation.pymunk_to_state((ball.body.position.x, ball.body.position.y))
            }

        return state

    def actions(self):
        player_ball = self.geometry['balls'][1] # p2

        # get the discrete points: all non-sunk balls not on the players side
        balls = []
        for ball in self.geometry['balls']:
            if ball.shape.custom['label'] in ['p1', 'p2']:
                continue
            if ball.shape.custom['sunk'] != None:
                continue
            if ball.body.position[0] < Simulation.state_to_pymunk(P2_BOUNDS[0])[0]:
                balls.append(ball)

        pois = []
        for ball in balls:
            v, point = self.scan(ball, player_ball)
            if v is None:
                continue
            pois.append((v,point))

        return pois
