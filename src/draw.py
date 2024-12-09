# constants
from const import *

# lib
import sim
import pygame

class Draw():
    def __init__(self, headless=False):
        pygame.init()

        if headless:
            self.display = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        else:
            self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.headless = headless
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 12)

    @staticmethod
    def pymunk_to_pygame(pos):
        return int(pos[0]), sim.WINDOW_HEIGHT - int(pos[1])

    def draw_obj(self, obj):
        if isinstance(obj, sim.Ball):
            custom = obj.shape.custom

            if custom['sunk']:
                return

            pos = obj.body.position

            pygame.draw.circle(
                surface=self.display,
                color=(0, 0, 0),
                center=Draw.pymunk_to_pygame(pos),
                radius=BALL_RADIUS + 1
            )
            pygame.draw.circle(
                surface=self.display,
                color=BALL_APPEARANCE[custom['label']]['color'],
                center=Draw.pymunk_to_pygame(pos),
                radius=BALL_RADIUS
            )
            
            if BALL_APPEARANCE[custom['label']]['draw_stripe']:
                pygame.draw.line(
                    surface=self.display,
                    color=(255, 255, 255),
                    start_pos=Draw.pymunk_to_pygame((pos[0] - BALL_RADIUS, pos[1])),
                    end_pos=Draw.pymunk_to_pygame((pos[0] + BALL_RADIUS, pos[1])),
                    width=2
                )

            if BALL_APPEARANCE[custom['label']]['draw_label']:
                text_width, _ = self.font.size(custom['label'])

                text_surface = self.font.render(
                    custom['label'],
                    False,
                    (255, 255, 255)
                )

                self.display.blit(
                    text_surface,
                    Draw.pymunk_to_pygame((pos[0] - text_width//2, pos[1] + BALL_RADIUS))
                )

        elif isinstance(obj, sim.Bound):
            custom = obj.shape.custom

            start = custom['start']
            end = custom['end']

            pygame.draw.line(
                surface=self.display,
                color=(84, 57, 29),
                start_pos=Draw.pymunk_to_pygame(start),
                end_pos=Draw.pymunk_to_pygame(end),
                width=TRIM_RADIUS * 2
            )

        elif isinstance(obj, sim.Pocket):
            pos = obj.body.position
            pygame.draw.circle(
                surface=self.display,
                color=(0, 0, 0), 
                center=Draw.pymunk_to_pygame(pos),
                radius=POCKET_RADIUS
            )
            #pygame.draw.circle(self.display, (0, 255, 0), mtog(x, y), POCKET_RADIUS - BALL_RADIUS) # critical region  
        
    def draw_frame(self, geometry):
        if not self.headless:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
        self.display.fill((255, 255, 255))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(TABLE_OUTLINE_LEFT, TABLE_OUTLINE_TOP, TABLE_OUTLINE_WIDTH, TABLE_OUTLINE_HEIGHT))
        pygame.draw.rect(self.display, (101, 67, 33), pygame.Rect(TABLE_EDGE_LEFT, TABLE_EDGE_TOP, TABLE_EDGE_WIDTH, TABLE_EDGE_HEIGHT))
        pygame.draw.rect(self.display, (0, 128, 0), pygame.Rect(TABLE_GREEN_LEFT, TABLE_GREEN_TOP, TABLE_WIDTH, TABLE_HEIGHT))

        pygame.draw.circle(self.display, (255, 255, 255), MARK_TOP_1_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_TOP_2_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_TOP_3_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_TOP_4_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_TOP_5_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_TOP_6_POS, MARK_RADIUS)

        pygame.draw.circle(self.display, (255, 255, 255), MARK_BOTTOM_1_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_BOTTOM_2_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_BOTTOM_3_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_BOTTOM_4_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_BOTTOM_5_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_BOTTOM_6_POS, MARK_RADIUS)

        pygame.draw.circle(self.display, (255, 255, 255), MARK_LEFT_1_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_LEFT_2_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_LEFT_3_POS, MARK_RADIUS)

        pygame.draw.circle(self.display, (255, 255, 255), MARK_RIGHT_1_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_RIGHT_2_POS, MARK_RADIUS)
        pygame.draw.circle(self.display, (255, 255, 255), MARK_RIGHT_3_POS, MARK_RADIUS)

        for group in geometry:
            for obj in geometry[group]:
                self.draw_obj(obj)

        if not self.headless:
            pygame.display.update()
            self.clock.tick(FPS * SIM_SPEED)

    def save_image(self, filepath):
        print('saving as', filepath)
        pygame.image.save(self.display, filepath)
