import pygame

class Menu:
    def __init__(self, screen, font, color, title):
        super().__init__()
        self.screen = screen
        self.font = font
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.title = title

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.draw_text(self.title, self.font, self.screen, 400, 300)
        self.draw_text("Press any key to continue", self.font, self.screen, 400, 400)

    def draw_score(self, score):
        self.draw_text(str(score), self.font, self.screen, 400, 100)

    def draw_win(self):
        self.draw_text("YOU WIN", self.font, self.screen, 400, 300)

    def draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, True, self.WHITE)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)