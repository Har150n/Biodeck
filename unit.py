import pygame 

class Unit(pygame.sprite.Sprite):
    #This class represents each unit a player has
    def __init__(self, name: str, hp: int, mana: int, att: int, image, side: int = 0, x_pos: int = 0, y_pos: int = 0):
        #Calls the parent class (Sprite) constructor
        super().__init__()

        self.name = name
        self.hp = hp
        self.mana = mana
        self.att = att
        self.alive = True
        self.taunted = False
        self.image = pygame.transform.scale(image,(100,100))
        self.rect = self.image.get_rect()
        self.side = side
        self.x_pos = x_pos
        self.y_pos = y_pos
        
    





