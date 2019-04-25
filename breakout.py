import colors
import pygame
import random
import time

import config as c

from ball import Ball
from brick import Brick
from button import Button
from game import Game
from paddle import Paddle
from text_object import TextObject


class Breakout(Game):

    def show_message(self, text, color=colors.WHITE, font_name='Arial', font_size=20, centralized=False):
        message = TextObject(c.screen_width//2, c.screen_height//2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)

    def create_menu(self):
        def on_play(button):
            for b in self.menu_buttons:
                self.objects.remove(b)

            self.is_game_running = True
            self.start_level = True

        def on_quit(button):
            self.game_over = True
            self.is_game_running = False

        for i, (text, handler) in enumerate((('PLAY', on_play), ('QUIT', on_quit))):
            b = Button(
                c.menu_offset_x,
                c.menu_offset_y + (c.menu_button_h+5) * i,
                c.menu_button_w,
                c.menu_button_h,
                text,
                handler,
                padding=5
            )

    def create_ball(self):
        speed = (random.randint(-2, 2), c.ball_speed)
        self.ball = Ball(c.screen_width//2, c.screen_height//2, c.ball_radius, c.ball_color, speed)
        self.objects.append(self.ball)

    def handle_ball_collisions(self):
        def intersect(obj, ball):
            edges = dict(
                left=pygame.Rect(obj.left, obj.top, 1, obj.height),
                right=pygame.Rect(obj.right, obj.top, 1, obj.height),
                top=pygame.Rect(obj.left, obj.bottom, obj.width, 1),
                bottom=pygame.Rect(obj.left, obj.bottom, obj.width, 1)
            )
            collisions = set(edge for edge in edges.items() if ball.bounds.colliderect(rect))
            if not collisions:
                return None

            if len(collisions) == 1:
                return list(collisions)[0]

            if 'top' in collisions:
                if ball.centery >= obj.top:
                    return 'top'
                if ball.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

            if 'bottom' in collisions:
                if ball.centery >= obj.bottom:
                    return 'bottom'
                if ball.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

            s = self.ball.speed
            edge = intersect(self.paddle, self.ball)
            if edge is not None:
                self.sound_effects['paddle_hit'].play()
            if edge == 'top':
                speed_x = s[0]
                speed_y = -s[1]
                if self.paddle.moving_left:
                    speed_x -= 1
                elif self.paddle.moving_left:
                    speed_x += 1
                self.ball.speed = speed_x, speed_y
            elif edge in ('left', 'right'):
                self.ball.speed = (-s[0], s[1])

            if self.ball.top > c.screen_height:
                self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            else:
                self.create_ball()

            if self.ball.top < 0:
                self.ball.speed(s[0], -s[1])

            if self.ball.left < 0 or self.ball.right > c.screen_width:
                self.ball.speed = (-s[0], s[1])

            for brick in self.bricks:
                edge = intersect(brick, self.ball)
                if not edge:
                    continue

                self.bricks.remove(brick)
                self.objects.remove(brick)
                self.score += self.points_per_brick

                if edge in ('top', 'bottom'):
                    self.ball.speed = (s[0], -s[1])
                else:
                    self.ball.speed = (-s[0], s[1])


def main():
    Breakout().run()


if __name__ == '__main__':
    main()
