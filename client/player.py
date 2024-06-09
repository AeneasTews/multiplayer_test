import pygame as pg
import loading_tools as lt
from os import path

pg.init()

main_dir = path.split(path.abspath(__file__))[0]
loader = lt.Loader(main_dir)


class Player(pg.sprite.Sprite):
    def __init__(self, game_size, position=(420, 420), number=1):
        super().__init__()
        # load image and rect using helper function
        self.image, self.rect = loader.load_image(path.join('sprites', 'cars', f'car{number}.png'), scale=0.3)
        self.original_image = self.image

        # initialize position and rotation
        self.position = pg.math.Vector2(position)
        self.direction = pg.math.Vector2(1, 0)

        # initialize values for movement
        self.speed = 0
        self.acceleration = 0
        self.MAX_SPEED = 3
        self.RESISTANCE = 0.02
        self.angle_speed = 0
        self.angle = 0

        # get max game size
        self.game_size = game_size

    def update(self):
        # rotation
        self.direction.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        self.image = pg.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # movement
        # handle resistance
        self.speed -= self.speed * self.RESISTANCE

        # check speed against max speed and reduce if necessary, otherwise update speed
        if self.speed > self.MAX_SPEED:
            self.speed = self.MAX_SPEED
        elif self.speed < -self.MAX_SPEED:
            self.speed = -self.MAX_SPEED
        else:
            self.speed += self.acceleration

        # update position
        self.position += self.direction * self.speed
        self.rect.center = self.position
        self.check_boundary()

    def accelerate(self, acceleration=0):
        self.acceleration = acceleration

    def rotate(self, speed=0):
        self.angle_speed = speed

    def check_boundary(self):
        if not self.game_size[0] - 50 > self.position.x > 50:
            self.position.x = int(self.game_size[0] / 2)
        if not self.game_size[1] - 50 > self.position.y > 50:
            self.position.y = int(self.game_size[1] / 2)
