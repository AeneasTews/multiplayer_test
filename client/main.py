import pygame as pg
from game_scene import GameScene
from login_scene import LoginScene

if __name__ == "__main__":
    # init
    pg.init()
    size = (1280, 720)
    screen = pg.display.set_mode(size)
    dt = 0.0

    # framerate
    clock = pg.time.Clock()

    # game state
    game_state = "login"

    #scene = GameScene(screen)
    scene = LoginScene(screen)

    # game loop
    while True:
        dt = clock.tick(60) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                scene.handle_key(event)
            elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEMOTION:
                scene.handle_mouse(event)

        scene.update()

        pg.display.flip()
        game_state = scene.get_next_scene()

