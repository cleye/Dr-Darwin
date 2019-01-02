import pygame , sys
from pygame.locals import *
pygame.init()


def _PASS():
    pass


def _mouse_up_(button):
    return (button.__prev_pressed__[1] and not button.__prev_pressed__[0])

def _mouse_down_(button):
    return (not button.__prev_pressed__[1] and button.__prev_pressed__[0])


class Button:
    buttons = []
    style_default = {"font":pygame.font.SysFont("Consolas", 25),"visible":True,"padding":(4,8,4,8),"border":(1,(255,255,255)),"bgcolor":(0,0,0),"txcolor":(255,255,255)}

    def __init__(self,text="Button",pos=(0,0), w=None, h=None):

        # GENERAL
        self.text = text
        self.x,self.y = pos

        # EVENTS
        self.__prev_pressed__ = [False,False,False]
        self.mouse_down = _PASS
        self.mouse_up = _PASS

        # STYLING
        self.font = Button.style_default["font"]
        self.visible = Button.style_default["visible"]
        self.padding = Button.style_default["padding"]
        self.border = Button.style_default["border"]
        self.bgcolor = Button.style_default["bgcolor"]
        self.txcolor = Button.style_default["txcolor"]
        self.text_width,self.text_height = self.font.size(self.text)
        if w is None and h is None:
            self.w = self.text_width+self.padding[1]+self.padding[3]
            self.h = self.text_height+self.padding[0]+self.padding[2]
        else:
            self.w = w
            self.h = h
        self.width = self.w+self.border[0]*2
        self.height = self.h+self.border[0]*2
        self.surface = pygame.Surface((self.width,self.height))

    def add(self,surface):
        if self.visible:
            self.surface.lock()
            if self.border:
                pygame.draw.rect(self.surface,self.border[1],(0,0,self.width,self.height))
            pygame.draw.rect(self.surface,self.bgcolor,(self.border[0],self.border[0],self.w,self.h))
            self.surface.unlock()

            text_img = self.font.render(self.text,True,self.txcolor)
            self.surface.blit(text_img, (self.width/2 - text_img.get_rect().width/2, self.height/2 - text_img.get_rect().height/2))

            Button.buttons.append(self)
            surface.blit(self.surface,(self.x,self.y))

            self.__prev_pressed__[2] = self.__prev_pressed__[1]
            self.__prev_pressed__[1] = self.__prev_pressed__[0]

            if pygame.mouse.get_pressed()[0]:
                self.__prev_pressed__[0] = True
            else:
                self.__prev_pressed__[0] = False

            if self.x < pygame.mouse.get_pos()[0]<self.width+self.x and self.y<pygame.mouse.get_pos()[1]<self.height+self.y:
                if _mouse_up_(self):
                    self.mouse_up()
                if _mouse_down_(self):
                    self.mouse_down()
                pygame.mouse.set_cursor(*pygame.cursors.arrow)





