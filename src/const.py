# Simulation Visuals
BALL_APPEARANCE = {
    'p1': {'color': (255, 255, 255), 'draw_stripe': False, 'draw_label': False},
    'p2': {'color': (255, 255, 255), 'draw_stripe': False, 'draw_label': False},
    '1' : {'color': (255, 205, 0), 'draw_stripe': False, 'draw_label': True},
    '2' : {'color': (0, 0, 205), 'draw_stripe': False, 'draw_label': True},
    '3' : {'color': (205, 0, 0), 'draw_stripe': False, 'draw_label': True},
    '4' : {'color': (128, 0, 128), 'draw_stripe': False, 'draw_label': True},
    '5' : {'color': (255, 102, 0), 'draw_stripe': False, 'draw_label': True},
    '6' : {'color': (0, 128, 0), 'draw_stripe': False, 'draw_label': True},
    '7' : {'color': (128, 0, 0), 'draw_stripe': False, 'draw_label': True},
    '9' : {'color': (255, 205, 0), 'draw_stripe': True, 'draw_label': True},
    '10' : {'color': (0, 0, 205), 'draw_stripe': True, 'draw_label': True},
    '11' : {'color': (205, 0, 0), 'draw_stripe': True, 'draw_label': True},
    '12' : {'color': (128, 0, 128), 'draw_stripe': True, 'draw_label': True},
    '13' : {'color': (255, 102, 0), 'draw_stripe': True, 'draw_label': True},
    '14' : {'color': (0, 128, 0), 'draw_stripe': True, 'draw_label': True},
    '15' : {'color': (128, 0, 0), 'draw_stripe': True, 'draw_label': True}
}

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
TABLE_WIDTH, TABLE_HEIGHT = 478, 232
       
POCKET_RADIUS = 16
TABLE_CORNER = POCKET_RADIUS
TABLE_MID = POCKET_RADIUS * 2

TABLE_BEZEL = POCKET_RADIUS * 2
MARK_RADIUS = 3 
TRIM_RADIUS = 2

BOUND_1_START = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + TABLE_CORNER, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)
BOUND_1_END = (WINDOW_WIDTH//2 - TABLE_MID//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)

BOUND_2_START = (WINDOW_WIDTH//2 + TABLE_MID//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)
BOUND_2_END = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 - TABLE_CORNER, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TRIM_RADIUS)

BOUND_3_START = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 + TABLE_CORNER, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)
BOUND_3_END = (WINDOW_WIDTH//2 - TABLE_MID//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)

BOUND_4_START = (WINDOW_WIDTH//2 + TABLE_MID//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)
BOUND_4_END = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 - TABLE_CORNER, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TRIM_RADIUS)

BOUND_5_START = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TRIM_RADIUS, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 - TABLE_CORNER)
BOUND_5_END = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TRIM_RADIUS, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + TABLE_CORNER)

BOUND_6_START = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TRIM_RADIUS, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 - TABLE_CORNER)
BOUND_6_END = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TRIM_RADIUS, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 + TABLE_CORNER)

POCKET_1_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2)
POCKET_2_POS = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + POCKET_RADIUS//2)
POCKET_3_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2)
POCKET_4_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2)
POCKET_5_POS = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - POCKET_RADIUS//2)
POCKET_6_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2)

TABLE_OUTLINE_LEFT = WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL - 5 
TABLE_OUTLINE_TOP = WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL - 5
TABLE_OUTLINE_WIDTH = TABLE_WIDTH + TABLE_BEZEL * 2 + 10
TABLE_OUTLINE_HEIGHT = TABLE_HEIGHT + TABLE_BEZEL * 2 + 10

TABLE_EDGE_LEFT = WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL
TABLE_EDGE_TOP = WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL
TABLE_EDGE_WIDTH = TABLE_WIDTH + TABLE_BEZEL * 2
TABLE_EDGE_HEIGHT = TABLE_HEIGHT + TABLE_BEZEL * 2

TABLE_GREEN_LEFT = WINDOW_WIDTH//2 - TABLE_WIDTH//2
TABLE_GREEN_TOP = WINDOW_HEIGHT//2 - TABLE_HEIGHT//2

MARK_TOP_1_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2)
MARK_TOP_2_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//4, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2)
MARK_TOP_3_POS = (WINDOW_WIDTH//2 - 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2)
MARK_TOP_4_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2)
MARK_TOP_5_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//4, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2),
MARK_TOP_6_POS = (WINDOW_WIDTH//2 + 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2),

MARK_BOTTOM_1_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2)
MARK_BOTTOM_2_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//4, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2)
MARK_BOTTOM_3_POS = (WINDOW_WIDTH//2 - 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2)
MARK_BOTTOM_4_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2)
MARK_BOTTOM_5_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//4, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2)
MARK_BOTTOM_6_POS = (WINDOW_WIDTH//2 + 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2)

MARK_LEFT_1_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//4)
MARK_LEFT_2_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2)
MARK_LEFT_3_POS = (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//4)

MARK_RIGHT_1_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//4)
MARK_RIGHT_2_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2)
MARK_RIGHT_3_POS = (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//4)

# Simulation Logic
SIM_SPEED = 1
FPS=60

BALL_RADIUS = 7
BALL_DENSITY = 25
BALL_ELASTICITY = 0.9
BALL_FRICTION = 0.8

BOUND_ELASTICITY = 0.8

RAYCAST_IGNORE = 0b10
RAYCAST_LEN = 10000

BALL_COLLISION_TYPE = 1
POCKET_COLLISION_TYPE = 2

P1_BOUNDS = ((BALL_RADIUS, BALL_RADIUS), (3*TABLE_WIDTH//8, TABLE_HEIGHT - BALL_RADIUS))
P2_BOUNDS = ((5*TABLE_WIDTH//8, BALL_RADIUS), (TABLE_WIDTH - BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS))

P1_SHOOT_BOUNDS = ((BALL_RADIUS, BALL_RADIUS), (TABLE_WIDTH//8, TABLE_HEIGHT - BALL_RADIUS))
P2_SHOOT_BOUNDS = ((7*TABLE_WIDTH//8, BALL_RADIUS), (TABLE_WIDTH - BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS))


# Optimization
PLAYOUT_DEPTH_LIMIT = 4

NAIVE_MUTATION_PROB = {
    'steepness': 2.0,
    'offset': -2.5,
    'above_avg_prob': 1/14
}

INFORMED_MUTATION_PROB = {
    'steepness': 2.5,
    'offset': -2.5,
    'above_avg_prob': 1/14
}

NAIVE_MUTATION_SD = {
    'steepness': -0.3,
    'offset': 1,
    'scale': 40,
    'minimum': 5
}

INFORMED_MUTATION_SD = {
    'steepness': -0.3,
    'offset': 1,
    'scale': 25,
    'minimum': 20
}

PENALTY_MULT = {
    'steepness': 0.25,
    'offset': 0
}
