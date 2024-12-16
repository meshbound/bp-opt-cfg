# constants
from const import *

import pymunk

class Pocket():
    def __init__(self, space, pos, label):
        # body
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos

        # shape
        self.shape = pymunk.Circle(self.body, POCKET_RADIUS - BALL_RADIUS)
        self.shape.filter = pymunk.ShapeFilter(categories=RAYCAST_IGNORE)
        self.shape.collision_type = POCKET_COLLISION_TYPE
        self.shape.sensor = True

        # custom
        self.shape.custom = {
            'label': label
        }

        space.add(self.body, self.shape)

    def step(self):
        pass
