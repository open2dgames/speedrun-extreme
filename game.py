import pygame
import sys
from player import Player
from editor import load_map
from menu import Menu
import os
import time

class Game():
    def __init__(self):
        super().__init__()
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))

        self.win = False

        self.camera = [25, 25]
        self.camera_speed = 10 # More the number is small more the camera move

        self.font = pygame.font.Font(None, 74)
        
        self.player = Player()

        self.has_quit_menu = False

        self.last_file_update = time.time()

        self.time_start = None
        self.score = 0
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.menu = Menu(self.screen, self.font, self.WHITE, "Menu")
        
        self.platforms = []
        self.goal = None

        self.map, self.player.player_rect.center, self.goal = load_map()
        self.player.spawn_point = self.player.player_rect.center
        self.platforms = []
        for platform in self.map:
            self.platforms.append(platform)
        

        # code example for loading an image to the screen 
        #self.image = pygame.image.load("player.png")


        self.display_color = self.hex_to_rgb('#051f39')
        self.platforms_color = self.hex_to_rgb('#c53a9d')

        # rajouter une condition qui est de faire le menu 
        self.run()


    ##4a2480
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def run(self):
        while True:
            need_reload_map, self.last_file_update = self.has_file_changed('map.txt', self.last_file_update)
            if need_reload_map:
                self.map,  none_pos, none_goal = load_map()
                for platform in self.map:
                    self.platforms.append(platform)
        
            # Gérer les événements ici (fermer la fenêtre par exemple)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.has_quit_menu = True

            # Remplir les surfaces
            self.screen.fill('black')
            self.display.fill(self.display_color)

            # Dessiner les plateformes
            for platform in self.platforms:
                pygame.draw.rect(self.display, self.platforms_color, pygame.Rect(platform[0] - self.camera[0], platform[1] - self.camera[1], platform[2], platform[3]))
            pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.goal[0] - self.camera[0], self.goal[1] - self.camera[1], self.goal[2], self.goal[3]))

            # Appeler la méthode update du joueur pour capturer les inputs et mettre à jour sa position
            self.player.update(self.platforms)


            # Dessiner le joueur sur l'écran (la petite surface low-res)
            pygame.draw.rect(self.display, self.player.player_color, pygame.Rect(self.player.player_rect.x - self.camera[0], self.player.player_rect.y - self.camera[1], self.player.player_rect.width, self.player.player_rect.height))

            # Scaler et blitter l'affichage sur la grande fenêtre
            self.screen.blit(pygame.transform.scale(self.display, (800, 600)), (0, 0))

            self.camera[0] += (self.player.player_rect.x - self.camera[0] - 200) / self.camera_speed
            self.camera[1] += (self.player.player_rect.y - self.camera[1] - 150) / self.camera_speed


            if self.player.player_rect.colliderect(self.goal):
                self.win = True
            if not self.has_quit_menu:self.menu.draw_menu()
            elif not self.win: 
                if self.time_start is None: self.time_start = time.time()
                
                score_with_one_decimal = "{:.1f}".format(self.score)
                self.menu.draw_score(score_with_one_decimal)
                self.score = time.time() - self.time_start

            else: self.menu.draw_win()

            
            # Mettre à jour l'écran
            pygame.display.flip()

            # Limiter à 60 FPS
            self.clock.tick(60)



    def has_file_changed(self, file_path, last_mod_time):
        current_mod_time = os.path.getmtime(file_path)
        return current_mod_time != last_mod_time, current_mod_time


if __name__ == '__main__':
    game = Game()
