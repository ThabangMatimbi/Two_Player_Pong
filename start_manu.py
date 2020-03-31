import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)
blue = (0,0,225)
green = (0,255,0)
silver = (192,192,192)
## Menu class is for start up menu option

class Menu(object):
    state = 0
    def __init__(self,items,font_color=blue,select_color=red,ttf_font=None,font_size=40):
        self.items = items
        self.font_color = font_color
        self.select_color = select_color
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            #total height of menu text block
            total_height = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (total_height /2) + (index * height)
            
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):                                                     
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1
