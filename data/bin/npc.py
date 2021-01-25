import pygame

class Merchant:
    """
    x,y: location of Merchant
    alist: items they sell
    thetype: type of merchant
        1: Consumables
        2: Weapons
        3: Armor
    """
    def __init__(self,x,y,alist,thetype):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x*32,self.y*32, 32,32)
        self.can_talk = [(self.x,self.y+1)] #being one space around it will let you speak
        self.goods = alist
        self.atype = thetype
        self.interacting = 0 #not interacting
    def draw(self,win):
        pygame.draw.rect(win, (0,0,100),self.rect,2)

    def update(self,achar,amessage):
        keys = pygame.key.get_pressed()
        if self.interacting == 0:
            if achar.current_pos in self.can_talk:
                if achar.rect.top == self.rect.bottom:
                    if keys[pygame.K_e]:
                        self.interacting = 1
                        amessage.show += 1 #show chatting message
                        if self.atype == 1: #Consumables
                            amessage.text = ["The finest goods in the land."]
                        if self.atype == 2: #WEAPONS
                            amessage.text = ["Ill help you shed blood."]
                        if self.atype == 3:
                            amessage.text = ["Looking to not get killed?"]
