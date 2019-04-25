import pygame

from ball import Ball
from brick import Brick
from game import Game
from paddle import Paddle
from text_object import TextObject


class Breakout(Game):
    ...


def main():
    Breakout().run()


if __name__ == '__main__':
    main()
