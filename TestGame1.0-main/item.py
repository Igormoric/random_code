
import pygame


class chara():
    def __init__(self,x,y,cor,lar,alt):
        self.itemc=pygame.Rect(x,y,lar,alt)
        self.cor=cor
        self.velx=0
        self.vely=0
        self.ativo=True

    def desenha(self,window):
        pygame.draw.rect(window,self.cor,self.itemc)
    

    def move(self,passos):
        if(self.velx>0):
            self.itemc.x+=1*passos
        if(self.velx<0):
            self.itemc.x-=1*passos
        if(self.vely>0):
            self.itemc.y+=1*passos
        if(self.vely<0):
            self.itemc.y-=1*passos
    
    def gravi(self,passos):
        if(self.vely>0):
            self.itemc.y-=1*passos

class item():
    def __init__(self,x,y,cor,lar=50,alt=50):
        self.itemc=pygame.Rect(x,y,lar,alt)
        self.cor=cor
        self.velx=0
        self.vely=0
        self.ativo=True
        self.moveu=False
        
    def desenha(self,window):
        pygame.draw.rect(window,self.cor,self.itemc)
    
    
    def move(self,passos):
        if(self.velx>0):
            self.itemc.x+=1*passos
        if(self.velx<0):
            self.itemc.x-=1*passos
        if(self.vely>0):
            self.itemc.y+=1*passos
        if(self.vely<0):
            self.itemc.y-=1*passos
    
    def gravi(self,passos):
        if(self.vely>0):
            self.itemc.y-=1*passos
        if(self.vely<0):
            self.itemc.y+=1*passos
  
class cena():
    def __init__(self,x,y,cor,lar,alt):
        self.itemc=pygame.Rect(x,y,lar,alt)
        self.cor=cor
        self.ativo=True

    def desenha(self,window):
        pygame.draw.rect(window,self.cor,self.itemc)
    