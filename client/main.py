import pygame as pg
from game_scene import GameScene
from login_scene import LoginScene
from connection_manager import ConnectionManager

if __name__ == "__main__":
    # init
    pg.init()
    size = (1280, 720)
    screen = pg.display.set_mode(size)
    dt = 0.0

    # framerate
    clock = pg.time.Clock()

    # game state
    connection_manager = ConnectionManager()
    scene = LoginScene(screen, connection_manager)

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

        if scene.next_scene == "game":
            connection_manager = scene.connection_manager
            scene = GameScene(screen, connection_manager)

        pg.display.flip()

