import pygame
pygame.init()



class SCREEN:
  def __init__(self,x,y):
    self.x = x #length
    self.y = y #width
    self.window = pygame.display.set_mode((self.x, self.y))
    self.FPSRATE = 30
    self.font = pygame.font.SysFont("Arial",125)
    self.clock = pygame.time.Clock()
    self.rect = self.window.get_rect()
    
    
  def drawScreen(self):
    self.window.fill((255,255,255))


  def text(self,message,xpos,ypos):
    text = self.font.render(message, True, (0,0,0))
    text_rect = text.get_rect(center = (xpos,ypos))
    self.window.blit(text,text_rect)



pygame.display.set_caption("M's RPG")

main_menu_screen = SCREEN(800,500)
main_menu_screen.text('TEST',200,200)

#menu button
def updateScreen():
  main_menu_screen.drawScreen()
  pygame.display.update()



def main():
  running = True
  while running:
    updateScreen()
    main_menu_screen.clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          pygame.quit()


main()


  
  
