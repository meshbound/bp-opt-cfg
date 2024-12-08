# constants
from const import *

import pymunk

class Ball():
    def __init__(self, space, pos, label, sunk):
        # body
        self.body = pymunk.Body()
        self.body.position = pos

        # shape
        self.shape = pymunk.Circle(self.body, BALL_RADIUS)
        self.shape.density = BALL_DENSITY
        self.shape.elasticity = BALL_ELASTICITY
        self.shape.collision_type = BALL_COLLISION_TYPE

        # custom
        self.shape.custom = {
            'label': label,
            'sunk': sunk
        }

        space.add(self.body, self.shape)

    def step(self):
        friction_force = (self.body.mass * 9.81) * BALL_FRICTION
        dir = -pymunk.Vec2d.normalized(self.body.velocity)
        self.body.apply_force_at_local_point((friction_force * dir.x, friction_force * dir.y), (0,0))
