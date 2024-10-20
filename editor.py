import pygame

# bloc of 10 by 10
def load_map():
    platforms = []
    player_spawn = (0, 0)
    goal = None

    # Ouvrir le fichier en mode lecture
    with open('map.txt', 'r') as fichier:
        for numero_line, line in enumerate(fichier, start=0):
            for numero_character, character in enumerate(line, start=0):
                if character == "1": platforms.append(pygame.Rect((numero_character * 20, numero_line * 20), (20, 20)))
                if character == "2": player_spawn = (numero_character * 20, numero_line * 20)
                if character == "3": goal = (pygame.Rect((numero_character * 20, numero_line * 20), (20, 20)))


    return platforms, player_spawn, goal

