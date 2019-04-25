import colors
import pygame
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
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)


def main():
    Breakout().run()


if __name__ == '__main__':
    main()
