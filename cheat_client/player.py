"""Modules used for initializing the loading module,
pygame and the loading module itself."""
from os import path
import pygame
from loading_tools import Loader

main_dir = path.split(path.abspath(__file__))[0]
loader = Loader(main_dir)

# initialize constants
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
        self.max_vel = 3  # maximum speed in either direction
        self.max_acc = 0.1  # acceleration when accelerating
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
        self.velocity = min(self.max_vel, max(-self.max_vel, self.velocity))

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
            self.acceleration = self.max_acc

        if pressed[pygame.K_s]:
            self.acceleration = -self.max_acc

        if ((not pressed[pygame.K_w] and not pressed[pygame.K_s]) or
                (pressed[pygame.K_w] and pressed[pygame.K_s])):
            self.acceleration = 0

        self.click_move()
        self.cheat_speed()

    def click_move(self):
        """This 'cheat' function enables the user to move the car by clicking anywhere on screen."""
        # get pressed buttons
        mouse = pygame.mouse.get_pressed()

        # move car to cursor when clicked
        if mouse[0] == 1:
            self.position = pygame.mouse.get_pos()

    def cheat_speed(self):
        """This function is used for increasing the max speed
        and acceleration of the car."""
        # get pressed buttons
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LSHIFT]:
            self.max_vel = 6
            self.max_acc = 0.5
        else:
            self.max_vel = 3
            self.max_acc = 0.1

    def cheat_rotate(self, mouse_wheel):
        """This function is used for rotating the car by spinning the mouse wheel."""
        self.rot_acc += mouse_wheel * 3
        self.update()
