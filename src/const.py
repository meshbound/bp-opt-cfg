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

P1_SHOOT_BOUNDS = ((BALL_RADIUS, BALL_RADIUS), (TABLE_WIDTH//8, TABLE_HEIGHT - BALL_RADIUS))
P2_SHOOT_BOUNDS = ((7*TABLE_WIDTH//8, BALL_RADIUS), (TABLE_WIDTH - BALL_RADIUS, TABLE_HEIGHT - BALL_RADIUS))

BALL_ELASTICITY = 0.9
BOUND_ELASTICITY = 0.8

# sim
SIM_SPEED = 1
FPS=60
