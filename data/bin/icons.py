import pygame

import os
import sys

a = os.path.lexists("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/closed_G_chest.gif")  
pygame.init()
class Icons():
    def __init__(self):
        
        self.win = pygame.display.set_mode((480,448)) #window sizes

        self.gold_chest_closed_pre= pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/closed_G_chest.gif").convert_alpha()
        self.gold_chest_closed = pygame.transform.scale(self.gold_chest_closed_pre,(32,32))

        self.gold_chest_opened_pre = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/open_G_chest.gif").convert()
        self.gold_chest_opened = pygame.transform.scale(self.gold_chest_opened_pre,(32,32))

        self.wall = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/a_test_wall.gif").convert()
        self.floor = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/a_test_floor.gif").convert()

        self.icon_old = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/chat_icon.gif").convert_alpha()
        self.icon     = pygame.transform.scale(self.icon_old, (16,16))

        self.heart    = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/heart.gif").convert_alpha()
        self.hearticon = pygame.transform.scale(self.heart, (21,21))

        self.mana      = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/mana.gif").convert_alpha()
        self.manaicon  = pygame.transform.scale(self.mana, (21,21))

        self.attack      = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/attack.gif").convert_alpha()
        self.attackicon  = pygame.transform.scale(self.attack, (21,21))

        self.defence      = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/defence.gif").convert_alpha()
        self.defenceicon  = pygame.transform.scale(self.defence, (21,21))



        self.equipiconpre = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/equip.gif").convert_alpha()
        self.equipicon = pygame.transform.scale(self.equipiconpre, (13,13))

        self.speediconpre = pygame.image.load("/Users/isaaccampbell/Desktop/pygame-sandbox/data/sprites/obj/speed.gif").convert_alpha()
        self.speedicon = pygame.transform.scale(self.speediconpre, (21,21))