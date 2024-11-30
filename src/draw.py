# constants
from const import *

# lib
import sim
import pygame

# pygame initalization
pygame.init()

# pygame constants
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 12)

class Draw():

    @staticmethod
    def pymunk_to_pygame(pos):
        return int(pos[0]), sim.WINDOW_HEIGHT - int(pos[1])

    @staticmethod
    def draw_obj(obj):
        if isinstance(obj, sim.Ball):
            custom = obj.shape.custom

            if custom['sunk']:
                return

            pos = obj.body.position

            pygame.draw.circle(
                surface=display,
                color=(0, 0, 0),
                center=Draw.pymunk_to_pygame(pos),
                radius=BALL_RADIUS + 1
            )
            pygame.draw.circle(
                surface=display,
                color=BALL_APPEARANCE[custom['label']]['color'],
                center=Draw.pymunk_to_pygame(pos),
                radius=BALL_RADIUS
            )
            
            if BALL_APPEARANCE[custom['label']]['draw_stripe']:
                pygame.draw.line(
                    surface=display,
                    color=(255, 255, 255),
                    start_pos=Draw.pymunk_to_pygame((pos[0] - BALL_RADIUS, pos[1])),
                    end_pos=Draw.pymunk_to_pygame((pos[0] + BALL_RADIUS, pos[1])),
                    width=2
                )

            if BALL_APPEARANCE[custom['label']]['draw_label']:
                text_width, _ = font.size(custom['label'])

                text_surface = font.render(
                    custom['label'],
                    False,
                    (255, 255, 255)
                )

                display.blit(
                    text_surface,
                    Draw.pymunk_to_pygame((pos[0] - text_width//2, pos[1] + BALL_RADIUS))
                )

        elif isinstance(obj, sim.Bound):
            custom = obj.shape.custom

            start = custom['start']
            end = custom['end']

            pygame.draw.line(
                surface=display,
                color=(84, 57, 29),
                start_pos=Draw.pymunk_to_pygame(start),
                end_pos=Draw.pymunk_to_pygame(end),
                width=TRIM_RADIUS * 2
            )

        elif isinstance(obj, sim.Pocket):
            pos = obj.body.position
            pygame.draw.circle(
                surface=display,
                color=(0, 0, 0), 
                center=Draw.pymunk_to_pygame(pos),
                radius=POCKET_RADIUS
            )
            #pygame.draw.circle(display, (0, 255, 0), mtog(x, y), POCKET_RADIUS - BALL_RADIUS) # critical region  
        
    @staticmethod
    def draw_frame(geometry):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        display.fill((255, 255, 255))
        pygame.draw.rect(display, (0, 0, 0), pygame.Rect(WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL - 5, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL - 5, TABLE_WIDTH + TABLE_BEZEL * 2 + 10, TABLE_HEIGHT + TABLE_BEZEL * 2 + 10))
        pygame.draw.rect(display, (101, 67, 33), pygame.Rect(WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL, TABLE_WIDTH + TABLE_BEZEL * 2, TABLE_HEIGHT + TABLE_BEZEL * 2))
        pygame.draw.rect(display, (0, 128, 0), pygame.Rect(WINDOW_WIDTH//2 - TABLE_WIDTH//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2, TABLE_WIDTH, TABLE_HEIGHT))

        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//4, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//4, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 - TABLE_HEIGHT//2 - TABLE_BEZEL//2), MARK_RADIUS)

        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//4, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//4, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + 3*TABLE_WIDTH//8, WINDOW_HEIGHT//2 + TABLE_HEIGHT//2 + TABLE_BEZEL//2), MARK_RADIUS)

        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//4), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 - TABLE_WIDTH//2 - TABLE_BEZEL//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//4), MARK_RADIUS)

        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2 - TABLE_HEIGHT//4), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2), MARK_RADIUS)
        pygame.draw.circle(display, (255, 255, 255), (WINDOW_WIDTH//2 + TABLE_WIDTH//2 + TABLE_BEZEL//2, WINDOW_HEIGHT//2 + TABLE_HEIGHT//4), MARK_RADIUS)

        for group in geometry:
            for obj in geometry[group]:
                Draw.draw_obj(obj)

        pygame.display.update()
        clock.tick(FPS * SIM_SPEED)
