import pygame
import sys #access system
import time
import os
#import from bin
from data.bin.tile import Tile
from data.bin.message import MessageBox
from data.bin.inventory import Inventory
from data.bin.mobs import *
from data.bin.combat import Combat
from data.bin.mainchar import Main_Player
from data.bin.chest import Chest
from data.bin.npc import Merchant
from data.bin.icons import Icons
os.environ['SDL_VIDEO_CENTERED'] = '1' #this sets the window
pygame.init() #initializes pygame, always need to have this

main_path = os.path.dirname('MainGame')
image_path = os.path.join(main_path, 'data\sprites\obj')

#establishes fps
clock = pygame.time.Clock()
run = True
all_icons = Icons()
#Tile Dimensions
class GAMEFRAME:
  def __init__(self, MAP_X,MAP_Y,TILESIZE):
    self.MAP_X = MAP_X
    self.MAP_Y = MAP_Y
    self.SIZE = TILESIZE
    self.win = pygame.display.set_mode((MAP_X*self.SIZE,MAP_Y*self.SIZE)) #window sizes
    pygame.display.set_caption("Game_Name") #window name

    #ALL IMAGE STUFF HAPPENS HERE

    self.level1 = [
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
      [0,1,1,1,1,1,1,1,1,1,0,1,1,0,0], #2
      [0,0,1,1,0,1,1,1,1,1,0,0,1,0,0], #3
      [0,1,1,3,1,1,3,1,1,1,0,3,0,1,0], #4
      [0,1,1,1,1,1,1,1,1,1,1,1,0,1,0], #5
      [0,1,1,1,1,1,1,1,1,1,1,1,1,0,0], #6
      [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0], #7
      [0,1,1,1,1,1,1,1,1,1,1,0,1,1,0], #8
      [0,1,0,0,1,1,1,1,1,1,1,1,1,1,0], #9
      [0,1,0,1,1,1,1,0,0,0,1,1,1,1,0], #10
      [0,1,0,1,0,0,0,1,1,1,0,0,1,0,0], #11
      [0,0,1,1,1,0,0,1,0,1,0,0,1,1,0], #12
      [0,1,1,1,1,0,1,1,0,1,0,0,1,1,0], #13
      [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]  #14
      ]

    self.collision_dict = {}
    self.party = []
    self.enemy_dict = {}
    self.npc_dict = {}
    self.chest_dict = {}

    """Zero: item ID
      First: item name
      Second: Item classification, and the type
      Third: REQUIRED LEVEL NEEDED TO USE IT
      ----ALWAYS INDEX NUMBER 4------
      Fourth: The specific status of it.

      Equipment specific statuses go like this:
      [Attack,Defense,Health,Speed]

      could include:
        Critical Strike?


      Fifth: [Buy Price, Sell Price]
      Sixth: Description of item




      """

    self.item_list =[
      [0, "Small Health Potion",["Consumable", "Health"], [1,"Potion"], 10,  [10,5], ["This restores 10 HP to a character."]],
      [1, "Large Health Potion",["Consumable", "Health"], [1,"Potion"], 50,  [25,10],["This restores 50 HP to a character."]],
      [2, "Super Health Potion",["Consumable", "Health"], [1,"Potion"], 100, [50,20],["This restores 100 HP to a character."]],

      [3, "Small Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 10,  [10,5], ["This restores 10 MP to a character."]],
      [4, "Large Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 50,  [25,10], ["This restores 50 MP to a character."]],
      [5, "Super Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 100, [50,20], ["This restores 100 MP to a character."]],

      [6, "Small Dagger"    ,["Equipment","Weapon"], [1,"Dagger"], [1,0,0,3],  [1,8],  ["A small, yet effective weapon."]],
      [7, "Bronze Sword"    ,["Equipment","Weapon"], [3,"Sword"], [2,1,0,2],  [50,25], ["What squires swing at eachother trying to be knights."]],
      [8, "Iron Sword"      ,["Equipment","Weapon"], [5,"Sword"], [3,1,0,1],  [100,50],["Brave and noble nights wield these."]],

      [9,  "Cloth Hat"      ,["Equipment","Helm"], [1, "Cloth"], [0,1,2,3],  [15,8],["Farmhands use these to protect from the sun, and you wanna protect from a sword."]],
      [10, "Bronze Helm"    ,["Equipment","Helm"], [3, "Plate"], [0,2,3,2],  [50,25],["Made with the finest bronze the local towns have to offer."]],
      [11, "Iron Helm"      ,["Equipment","Helm"], [5, "Plate"],[0,3,5,1],  [75,25], ["Many of these are scattered in deserts."]],


      [12, "Cloth Armor"    ,["Equipment","Chest"],[1, "Cloth"],[0,1,2,2], [15,8], ["Taken from a practice dummy, this hopefully will keep you alive."]],
      [13, "Bronze Armor"   ,["Equipment","Chest"],[3, "Plate"],[0,2,3,1], [50,25],["Guards wear it, and now you!"]],
      [14, "Iron Armor"     ,["Equipment","Chest"],[5, "Plate"],[0,3,5,1], [75,25], ["You can take an arrow to the gut with this and make it away."]]

       ]
    self.level_list = [
      [2,40], #level, amount to next level
      [3,120]
      ]

    self.level1_chest_rewards = [
      [(3,3), 6],
      [(11,3),7],
      [(6,3) ,8]
    ]

  def draw_tiles(win,levelList,collide_dict):
    #loops through every row and column in our level list
    for row in range(GAME.MAP_Y):
      for height in range(GAME.MAP_X):
        if levelList[row][height] == 0: #WALL
          image = all_icons.wall
        if levelList[row][height] == 1: #FLOOR
          image = all_icons.floor

        #GET COLLISION BOUNDARIES
        image_rect = image.get_rect()
        image_rect.topleft = (height * image_rect.width,
                              row    * image_rect.height)
        #position of tile
        new_x = height*GAME.SIZE
        new_y = row   *GAME.SIZE

        GAME.win.blit(image,(new_x,new_y,GAME.SIZE,GAME.SIZE)) #draw basic chest

        #DICT FOR TILES COLLISION ETC KEEP OR INFINITE LOOP AND NO MEMORY
        tc = (row, height)
        if levelList[row][height] == 0:
          if tc not in collide_dict:
            newTile = Tile(new_x,new_y)
            collide_dict[tc,'WALL'] = newTile
          GAME.win.blit(image,(new_x,new_y,GAME.SIZE,GAME.SIZE)) #draw walls

        if levelList[row][height] == 3: #CHEST
          if tc not in collide_dict:
            newChest = Chest(new_x,new_y,0)
            collide_dict[tc]   = newChest

          if tc not in GAME.chest_dict:
            newChest = Chest(new_x,new_y,0)
            GAME.chest_dict[tc]= [newChest,newChest.openpos]
            GAME.win.blit(image,(new_x,new_y,GAME.SIZE,GAME.SIZE)) #draw basic chest

          if tc in GAME.chest_dict:
            for chest in GAME.chest_dict:
              image = GAME.chest_dict[chest][0].update(main_char,message,GAME,inventory)
              GAME.win.blit(image,(GAME.chest_dict[chest][0].x, \
                                   GAME.chest_dict[chest][0].y, \
                                   GAME.SIZE,\
                                   GAME.SIZE)) #draw basic chest


start_inventory = [
      [0, "Small Health Potion",["Consumable", "Health"], [1,"Potion"], 10,  [10,5], ["This restores 10 HP to a character."]],
      [3, "Small Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 10,  [10,5], ["This restores 10 MP to a character."]],
      [6, "Small Dagger"    ,["Equipment","Weapon"], [1,"Dagger"], [1,0,0,3],  [1,8],  ["A small, yet effective weapon."]],
      [8, "Iron Sword"      ,["Equipment","Weapon"], [5,"Sword"], [3,1,0,1],  [100,50],["Brave and noble nights wield these."]],
      [9,  "Cloth Hat"      ,["Equipment","Helm"], [1, "Cloth"], [0,1,2,3],  [15,8],["Farmhands use these to protect from the sun, and you wanna protect from a sword."]],
      [12, "Cloth Armor"    ,["Equipment","Chest"],[1, "Cloth"],[0,1,2,2], [15,8], ["Taken from a practice dummy, this hopefully will keep you alive."]]
      ]

tier1_consumables = [
      [0, "Small Health Potion",["Consumable", "Health"], [1,"Potion"], 10,  [10,5], ["This restores 10 HP to a character."]],
      [3, "Small Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 10,  [10,5], ["This restores 10 MP to a character."]]
                     ]
tier1_gear = [
      [9,  "Cloth Hat"      ,["Equipment","Helm"], [1, "Cloth"], [0,1,2,3],  [15,8],["Farmhands use these to protect from the sun, and you wanna protect from a sword."]],
      [12, "Cloth Armor"    ,["Equipment","Chest"],[1, "Cloth"],[0,1,2,2], [15,8], ["Taken from a practice dummy, this hopefully will keep you alive."]]
      ]

tier1_weapons = [
      [6, "Small Dagger"    ,["Equipment","Weapon"], [1,"Dagger"], [1,0,0,3],  [1,8],  ["A small, yet effective weapon."]]
 ]

akey = ''

########################## INSTANCES #########
#INITIALIZE GAME
GAME = GAMEFRAME(15,14,32)
#max length per line, 50 chars   USE THIS ['',''] FORMAT
message = MessageBox('',0,GAME.win, GAME.MAP_X, GAME.SIZE)
#instance              #x,   y
main_char = Main_Player(64,64,GAME.collision_dict,GAME.enemy_dict,GAME.npc_dict,25,10)
inventory = Inventory(GAME.win,GAME.item_list,main_char,GAME.party,start_inventory)
bat1 = Bat(1,10,1,1,10,6,6)
bat2 = Bat(1,10,1,1,10,9,9)
bat3 = Bat(1,10,1,1,10,11,11)
merchant1 = Merchant(5,3,tier1_consumables,2)
combat = Combat()
###############################################
enemies = [bat1,bat2]
npcs = [merchant1]
GAME.enemy_dict['mob'] = bat1
GAME.enemy_dict['mob1'] = bat2
GAME.enemy_dict['mob2'] = bat3
GAME.npc_dict['merchant1'] = merchant1

GAME.party.append(main_char)
GAME.party.append(main_char)
GAME.party.append(main_char)
GAME.party.append(main_char)
#always want drawing to be done in one area, anytime i redraw it needs to be here
def update_screen():
  keys = pygame.key.get_pressed()
  if message.show == 0 and \
    inventory.show_inv == 0 and \
    inventory.nav_menu_in == 0 and \
    main_char.incombat == 0:

    GAME.win.fill((0,0,0)) #ALWAYS KEEP THIS
    GAME.draw_tiles(GAME.level1,GAME.collision_dict)
    main_char.move()
    main_char.in_combat() #checks for combat
    main_char.draw(GAME.win)

    merchant1.update(main_char,message)

    for enemy in enemies:
      enemy.draw(GAME.win)

    for npc in npcs:
        npc.draw(GAME.win)

  if message.show == 1:
    message.update_text()

  #CHAR SHOULD BE LAST BECAUSE HE SHOULD BE THE LAST THING ON TOP OF EVERYTHING
  pygame.display.update() #updates our screen

########## MAIN LOOP FOR GAME ###
#Main loop for game
while run:
  #GET ALL INPUTS
  keys = pygame.key.get_pressed()
  for event in pygame.event.get(): #list of all events in pygame
    if event.type == pygame.QUIT:  #If we quit it
      run = False
    if event.type == pygame.KEYDOWN: #means we can access inventory
      #MESSAGE THINGS
      if message.show == 1 and message.laste == 1:
        if event.key == pygame.K_e:
          message.show = 0
          message.laste = 0
      #inventory stuff
      if message.show == 0:
        ############################################
        #THESE EVENTS ARE PURELY FOR INVENTORY ONLY#
        ############################################
        if event.key == pygame.K_i and inventory.lasti == 0:
          inventory.show_inv = 1
        if event.key == pygame.K_i and inventory.lasti == 1 and inventory.nav_menu_in == 0:
          inventory.show_inv = 0
          inventory.nav_menu = 1

        if event.key == pygame.K_s:
          akey = 's'
        if event.key == pygame.K_a:
          akey = 'a'
        if event.key == pygame.K_d:
          akey = 'd'
        if event.key == pygame.K_w:
          akey = 'w'
        if event.key == pygame.K_e:
          akey = 'e'
        if event.key == pygame.K_q:
          akey = 'q'

        inventory.update(akey)
        akey = ''
########################
#These automatically update the screen rather than updating on a keydown action
########################
    if inventory.show_inv == 1 and inventory.nav_menu_in == 0 and message.show == 0:
      inventory.show_inventory(inventory.show_inv)
      inventory.show_char_stats(GAME.level_list)
    #INTERACTS WITH SUB MENU
    if inventory.nav_menu_in == 1:
      inventory.access_submenu(inventory.nav_menu)

    if inventory.nav_menu_in == 2:
      if inventory.nav_menu == 2: #on equipment
        inventory.access_submenu(inventory.nav_menu)
      #inventory.sub_choose()

    if inventory.nav_menu_in == 3:
      if inventory.nav_menu == 2:
        inventory.equipment(inventory.curr_party_member)

    if inventory.nav_menu_in == 4:
      if inventory.nav_menu == 2:
        inventory.show_equipment_selection = 1
        inventory.cycle_weapons()


      #inventory.update_inventory()

##    if inventory.nav_menu_in == 1:  KEEP FOR ITEMS
##      inv = inventory.update_dict()
##      inventory.change_buttons()
##      if len(inv) < 1:
##        inventory.nav_menu_in = 0
##      inventory.access_submenu(inventory.nav_menu)


###################### END OF INVENTORY #########
    if event.type == pygame.KEYUP: #reset variables
      #reset for inventory
      if event.key == pygame.K_e:

        if inventory.nav_menu_in == 2:
          inventory.laste = 1
        if inventory.nav_menu_in == 3:
          inventory.laste = 2
        if inventory.nav_menu_in == 4:
          inventory.laste = 3
        if inventory.nav_menu_in == 5:
          inventory.laste = 4

        if message.show == 1:
          message.laste = 1
      if event.key == pygame.K_i:
        if inventory.show_inv == 1:
          inventory.lasti = 1
        if inventory.show_inv == 0:
          inventory.lasti = 0

  update_screen() #updates our screen

  clock.tick(20)
  pygame.event.pump()
pygame.quit()


#TEXT ON SCREEN
