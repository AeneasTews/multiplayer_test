import pygame as pg
import player

if __name__ == "__main__":
    # init
    pg.init()
    size = (1280, 720)
    screen = pg.display.set_mode(size)
    dt = 0.0

    # framerate
    clock = pg.time.Clock()

    # test
    player = player.Player(number=1, game_size=size)
    playersprite = pg.sprite.GroupSingle()
    playersprite.add(player)
    background = pg.surface.Surface(size)
    background.convert()
    background.fill((25, 25, 25))

    # game loop
    while True:
        dt = clock.tick(60) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player.accelerate(acceleration=0.1)
                elif event.key == pg.K_DOWN:
                    player.accelerate(acceleration=-0.1)
                elif event.key == pg.K_LEFT:
                    player.rotate(speed=-4)
                elif event.key == pg.K_RIGHT:
                    player.rotate(speed=4)
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    player.accelerate(acceleration=0)
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    player.rotate(speed=0)

        # test
        playersprite.update()
        screen.blit(background, (0, 0))
        playersprite.draw(screen)

        pg.display.flip()
