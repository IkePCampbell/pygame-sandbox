import pygame
import os
import os
main_path = os.path.dirname('message')
image_path = os.path.join(main_path, 'data\sprites\obj')
class MessageBox():
  def __init__(self,text,show,awin,x,size):
    self.icon_old = pygame.image.load(os.path.join(image_path, 'chat_icon.gif')).convert_alpha()
    self.icon = pygame.transform.scale(self.icon_old, (16,16))
    self.text = text
    self.show = show
    self.font  = pygame.font.SysFont('Arial',20)
    self.cfont  = pygame.font.SysFont('Arial',12)
    self.width = (x *size)-20 #460 
    self.y_pos = 350
    self.x_pos = 10
    self.height = 90
    self.win = awin
    self.laste = 0
    #self.message_box_old = pygame.image.load(os.path.join(image_path, 'message.gif')).convert_alpha()
    #self.message_box = pygame.transform.scale(self.message_box_old, (self.width, self.height))
    self.message_box = pygame.image.load(os.path.join(image_path, 'message.gif'))
  def update_text(self):

    rect = pygame.Rect(self.x_pos,self.y_pos,self.width,self.height)
    message_box = pygame.draw.rect(self.win,(230,230,230), rect)
    #self.win.blit(self.message_box, (self.x_pos,self.y_pos))
    newtext = []
    for word in self.text:
      newtext.append(self.font.render(word,True,(0,0,0)))
    for line in range(len(newtext)):  #row     #every new row
      self.win.blit(newtext[line],(rect.left+5,rect.top+5+(line*25)))

    #shows how to get out of the textbox
    #continuetext = self.cfont.render("Press E to continue",True,(0,0,0))
    self.win.blit(self.icon,(rect.right-19,rect.bottom-17))
