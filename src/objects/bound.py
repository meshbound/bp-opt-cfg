# constants
from const import *

import pymunk

class Bound():
    def __init__(self, space, start, end):
        # body
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        # shpae
        self.shape = pymunk.Segment(self.body, start, end, TRIM_RADIUS)
        self.shape.elasticity = BOUND_ELASTICITY

        # custom
        self.shape.custom = {
            'start': start,
            'end': end
        }

        space.add(self.body, self.shape)

    def step(self):
        pass
