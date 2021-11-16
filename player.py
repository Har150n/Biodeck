import pygame 


class Player(pygame.sprite.Sprite):
    def __init__(self, player_one: bool, player_hp: int, player_mana: int, unit_list: list, image, x: int, y: int):
        self.player_one = player_one
        self.player_hp = player_hp
        self.player_mana = player_mana
        self.image = pygame.transform.scale(image,(100,100))
        self.x = x
        self.y = y
    

        