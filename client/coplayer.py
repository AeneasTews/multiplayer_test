import pygame as pg
import loading_tools as lt
from os import path

pg.init()

main_dir = path.split(path.abspath(__file__))[0]
loader = lt.Loader(main_dir)


class Coplayer(pg.sprite.Sprite):
    def __init__(self, position, number):
        super().__init__()

        self.image, self.rect = loader.load_image(path.join('sprites', 'cars', f'car{number}.png'), scale=0.3)
        self.original_image = self.image

        # initialize position and rotation
        self.position = position
        self.angle = 0

    def update(self):
        # rotation
        self.image = pg.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)

        # movement
        self.rect.center = self.position

    def set_rotation(self, angle):
        self.angle = angle

    def set_position(self, position):
        self.position = position
