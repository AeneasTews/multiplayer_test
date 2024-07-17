import asyncio
import pygame as pg


class LoginScene:
    def __init__(self, screen, connection_manager):
        # init
        self.screen = screen
        self.font = pg.font.Font(None, 32)

        # set up scene elements
        self.username_box = pg.Rect(100, 100, 140, 32)
        self.password_box = pg.Rect(100, 200, 140, 32)
        self.colors = [pg.Color("lightskyblue3"), pg.Color("dodgerblue2"),
                       pg.Color("chartreuse2"), pg.Color("darkgreen"), pg.Color("azure4")]
        self.submit_button = pg.Rect(100, 300, 100, 32)

        self.uname_active = False
        self.passwd_active = False
        self.submit_button_active = False
        self.uname_txt = ""
        self.passwd_txt = ""
        self.submit_txt = "Login"

        # game settings
        self.car = 1

        # scene management
        self.connection_manager = connection_manager
        self.next_scene = "login_active"

    def update(self):
        self.screen.fill((30, 30, 30))

        # render text
        u_txt_surf = self.font.render(self.uname_txt, True, self.colors[1] if self.uname_active else self.colors[0])
        p_txt_surf = self.font.render(self.passwd_txt, True, self.colors[1] if self.passwd_active else self.colors[0])
        s_txt_surf = self.font.render(self.submit_txt, True, self.colors[4])
        # resize the box
        u_width = max(200, u_txt_surf.get_width() + 10)
        p_width = max(200, p_txt_surf.get_width() + 10)
        s_width = s_txt_surf.get_width() + 10
        self.username_box.w = u_width
        self.password_box.w = p_width
        self.submit_button.w = s_width

        # blit the box rects
        pg.draw.rect(self.screen, self.colors[1] if self.uname_active else self.colors[0], self.username_box, 2)
        pg.draw.rect(self.screen, self.colors[1] if self.passwd_active else self.colors[0], self.password_box, 2)
        pg.draw.rect(self.screen, self.colors[2] if self.submit_button_active else self.colors[3], self.submit_button)

        # blit the text
        self.screen.blit(u_txt_surf, (self.username_box.x + 5, self.username_box.y + 5))
        self.screen.blit(p_txt_surf, (self.password_box.x + 5, self.password_box.y + 5))
        self.screen.blit(s_txt_surf, (self.submit_button.x + 5, self.submit_button.y + 5))

    def handle_mouse(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.username_box.collidepoint(event.pos):
                self.uname_active = True
                self.passwd_active = False
            elif self.password_box.collidepoint(event.pos):
                self.passwd_active = True
                self.uname_active = False
            elif self.submit_button.collidepoint(event.pos):
                self.passwd_active = False
                self.uname_active = False
                self.submit_button_active = True
                if self.connection_manager.login(self.uname_txt, self.passwd_txt, self.car):
                    self.next_scene = "game"
                else:
                    print("Login failed")
            else:
                self.uname_active = False
                self.passwd_active = False
        elif event.type == pg.MOUSEMOTION:
            if self.submit_button.collidepoint(event.pos):
                self.submit_button_active = True
            else:
                self.submit_button_active = False

    def handle_key(self, event):
        if event.type == pg.KEYDOWN:
            if self.uname_active:
                if event.key == pg.K_BACKSPACE:
                    self.uname_txt = self.uname_txt[:-1]
                elif event.key == pg.K_RETURN:
                    self.uname_active = False
                    self.passwd_active = True
                else:
                    self.uname_txt += event.unicode
            elif self.passwd_active:
                if event.key == pg.K_BACKSPACE:
                    self.passwd_txt = self.passwd_txt[:-1]
                elif event.key == pg.K_RETURN:
                    self.passwd_active = False
                    self.uname_active = False
                    if self.connection_manager.login(self.uname_txt, self.passwd_txt, self.car):
                        self.next_scene = "game"
                    self.next_scene = "game"
                else:
                    self.passwd_txt += event.unicode
