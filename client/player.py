"""Modules used for initializing the loading module,
pygame and the loading module itself."""
from os import path
import pygame
from loading_tools import Loader

main_dir = path.split(path.abspath(__file__))[0]
loader = Loader(main_dir)

# initialize constants
MAX_VEL = 3  # maximum speed in either direction
ROT_VEL = 3  # rotational speed
RESISTANCE = 0.02  # this isn't physics class --> we don't roll forever


class Player:
    """A class used to represent the player in the game."""
    def __init__(self, position, car, rotation=0):
        # TODO: reduce number of attributes
        # load image and rect using helper function
        self.original_image, self.rect = loader.load_image(
            path.join("sprites", "cars", f"car{car}.png"), scale=0.3)
        self.image = self.original_image  # required for rotating
        self.car = car  # required for translation between object and tuple

        # initialize player values
        self.position = pygame.Vector2(position)
        self.rect.center = self.position

        # init movement values
        self.velocity = 0
        self.acceleration = 0
        self.rotation = rotation
        self.rot_acc = 0  # using this avoids a bunch of copying of values
        self.direction = pygame.math.Vector2(1, 0)  # a vector pointing
        # straight in front of the car; useful for direction based movement
        self.direction.rotate_ip(self.rotation)  # adjust vector to fit any value supplied by server

    def update(self):
        """This function is used to run all separate update methods."""
        self.update_physics()
        self.update_image()

    def update_physics(self):
        """This function is used to update the physics of the player."""
        # resistance
        self.velocity -= self.velocity * RESISTANCE

        # handle speed
        self.velocity += self.acceleration
        # clamp velocity between +-MAX_VEL
        self.velocity = min(MAX_VEL, max(-MAX_VEL, self.velocity))

        # handle rotation
        self.direction.rotate_ip(self.rot_acc)  # rotate the direction vector in place
        self.rotation += self.rot_acc  # change the cars current rotation
        # (required for rotating the image)

        # handle position
        self.position += self.direction * self.velocity
        self.rect.center = self.position

    def update_image(self):
        """This function is used to update the image of the player."""
        self.image = pygame.transform.rotate(self.original_image, -self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, window):
        """This function is used to draw the player on the screen."""
        # update the player
        self.update()

        # draw the player
        window.blit(self.image, self.rect)

    def move(self):
        """This function is used to move the player on the screen
        by changing acceleration (directional and rotational)."""
        # get list of all keys and whether they are currently pressed
        pressed = pygame.key.get_pressed()

        # handle input
        if pressed[pygame.K_a]:
            self.rot_acc = -3

        if pressed[pygame.K_d]:
            self.rot_acc = +3

        if ((not pressed[pygame.K_a] and not pressed[pygame.K_d]) or
                (pressed[pygame.K_d] and pressed[pygame.K_a])):
            self.rot_acc = 0

        if pressed[pygame.K_w]:
            self.acceleration = 0.1

        if pressed[pygame.K_s]:
            self.acceleration = -0.1

        if ((not pressed[pygame.K_w] and not pressed[pygame.K_s]) or
                (pressed[pygame.K_w] and pressed[pygame.K_s])):
            self.acceleration = 0
