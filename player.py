import pygame

class Player():
    def __init__(self):
        self.player_rect = pygame.Rect(0, 0, 20, 30)
        self.spawn_point = (0, 0)
        #self.spawn_point = (0, -100)
        self.player_rect.center = (0, 0)

        
        self.player_color = (255, 255, 0)
        
        # Mouvements et vitesse du joueur
        self.player_movement = [0, 0]
        self.player_speed = 5  # Ajuster la vitesse de déplacement
        self.player_dir = ""
        self.time_in_dir = 0
        self.time_max_accel = 15
        self.player_accel_speed = 25

        # Dash du joueur
        self.dash_timer = 0
        self.dash_speed = 15
        self.is_dashing = False
        self.dash_time = 0.25
        self.dash_cooldown = 0
        self.dash_cooldown_time = 0.5
        self.dash_dir = ""

        
        # Variables pour le saut et la gravité
        self.player_jump_strength = -15  # Ajuster la force du saut (plus négatif = plus haut)
        self.player_double_jump_strength = -10
        self.gravity = 1  # Ajuster la gravité (plus la valeur est grande, plus la gravité est forte)
        self.max_gravity = 10  # Limiter la vitesse de chute
        self.is_grounded = False
        self.can_double_jump = False
        self.time_from_jump = 0
        self.time_left_from_ground = 0
        self.is_first_jump = False
        self.time_of_jump = 0

        ##4a2480
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    

    def update(self, platforms):
        # Utiliser pygame.key.get_pressed() pour capturer les touches pressées
        keys = pygame.key.get_pressed()

        # Réinitialiser le mouvement horizontal à chaque itération
        self.player_movement[0] = 0

        # Mouvements gauche/droite
        if keys[pygame.K_LEFT]:
            if self.player_dir == "right":
                self.player_dir = "left"
                self.player_movement[0] = -self.player_speed
                self.time_in_dir = 0
            else:
                self.player_dir = "left"
                self.player_movement[0] = -self.player_speed
                if self.time_in_dir < self.time_max_accel:
                    self.player_movement[0] = -self.player_speed + -self.player_accel_speed * (self.time_in_dir / self.time_max_accel)
                else:
                    self.player_movement[0] = -self.player_speed + -self.player_accel_speed
                self.time_in_dir += 1/60

        if keys[pygame.K_RIGHT]:
            if self.player_dir == "left":
                self.player_dir = "right"
                self.player_movement[0] = self.player_speed
                self.time_in_dir = 0
            else:
                self.player_dir = "right"
                self.player_movement[0] = self.player_speed
                if self.time_in_dir < self.time_max_accel:
                    self.player_movement[0] = self.player_speed + self.player_accel_speed * (self.time_in_dir / self.time_max_accel)
                else:
                    self.player_movement[0] = self.player_speed + self.player_accel_speed
                self.time_in_dir += 1/60
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.player_dir = ""
            self.time_in_dir = 0
        self.dash_cooldown -= 1/60
        mouse_click = pygame.mouse.get_pressed()
        # Saut
        if keys[pygame.K_UP]  and not self.is_first_jump and (self.is_grounded or self.time_left_from_ground < 0.2):  # Appuyer sur "espace" pour sauter
            self.jump()
            self.time_of_jump = 0
            self.time_left_from_ground += 5
            self.time_from_jump = 0
            self.is_first_jump = True

                    
        
        if (mouse_click[0] and not self.is_dashing and not self.is_grounded and self.is_first_jump and self.dash_cooldown <= 0) or self.is_dashing:
            self.dash(platforms)

        if keys[pygame.K_UP]and self.is_first_jump:
            self.time_of_jump += 1 / 60
            
        if not keys[pygame.K_UP] and self.is_first_jump:
            if self.player_movement[1] < 0:
                self.player_movement[1] /= 2
            self.is_first_jump = False
            self.can_double_jump = True

        if keys[pygame.K_UP] and self.can_double_jump:
            self.jump()
            self.can_double_jump = False

        
        self.time_from_jump += 1 / 60

        if self.is_grounded:
            self.time_left_from_ground = 0
        else:
            self.time_left_from_ground += 1/60

        # Appliquer la gravité
        if not self.is_grounded and not self.is_dashing:
            self.player_movement[1] += self.gravity
            if self.player_movement[1] > self.max_gravity:
                self.player_movement[1] = self.max_gravity  # Limiter la vitesse de chute

        # Appliquer les mouvements
        self.move(self.player_rect, self.player_movement, platforms)

        if self.player_rect.y > 600:
            self.player_rect.center = self.spawn_point

    

    def collisiontest(self, rect, platforms):
        hit_list = []
        for platform in platforms:
            if rect.colliderect(platform):
                hit_list.append(platform)
        return hit_list

    def move(self, rect, movement, platforms):
        # Déplacement horizontal
        rect.x += movement[0]
        hit_list = self.collisiontest(rect, platforms)
        for hit in hit_list:
            if movement[0] > 0:
                rect.right = hit.left
            if movement[0] < 0:
                rect.left = hit.right


        rect.y += 1
        self.is_grounded = False
        hit_list = self.collisiontest(rect, platforms)
        if hit_list != [] and not hit_list == []:
            self.is_grounded = True
        rect.y -= 1
         
        rect.y += movement[1]
        hit_list = self.collisiontest(rect, platforms)
        for hit in hit_list:
            if movement[1] > 0: # si le joueur est en train de tomber
                rect.bottom = hit.top
                self.is_grounded = True
                self.is_first_jump = False
                self.is_dashing = False
                self.player_movement[1] = 0  # Stopper la chute après contact avec le sol
            if movement[1] < 0:
                rect.top = hit.bottom
                self.player_movement[1] = 0  # Stopper le saut après contact avec une plateforme
    
    def dash(self, platforms):
        movement = [0, 0]
        if self.is_dashing:
            
            if self.dash_dir == "right":
                movement[0] = self.dash_speed
            elif self.dash_dir == "left":
                movement[0] = -self.dash_speed

            self.dash_timer += 1 / 60
            if self.dash_timer > self.dash_time:
                self.is_dashing = False
                self.dash_timer = self.dash_cooldown_time
        else:
            if self.player_dir == "right":
                self.dash_dir = "right"
                movement[0] = self.dash_speed
            elif self.player_dir == "left":
                self.dash_dir = "left"
                movement[0] = -self.dash_speed
            self.is_dashing = True
            self.player_movement[1] = 0
            self.dash_timer = 0
            self.can_double_jump = False
        
        self.move(self.player_rect, movement, platforms)
   

    def jump(self):
        self.player_movement[1] = self.player_jump_strength

    def collide(self):
        pass
