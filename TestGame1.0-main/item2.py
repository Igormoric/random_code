
import pygame


class itens():
    def __init__(self,x,y,cor,lar,alt):
        self.itemc=pygame.Rect(x,y,lar,alt)
        self.cor=cor
        self.velx=0
        self.vely=0
        self.ativo=True

    def desenha(self,window):
        pygame.draw.rect(window,self.cor,self.itemc)
    
    def gravi(self,passos):
        if(self.vely>0):
            self.itemc.y-=1*passos

class chara(itens):
    def __init__(self,x,y,cor,lar,alt):
        itens.__init__(self,x,y,cor,lar,alt)   

    def move(self,passos):
        if(self.velx>0):
            self.itemc.x+=1*passos
        if(self.velx<0):
            self.itemc.x-=1*passos
        if(self.vely>0):
            self.itemc.y+=1*passos
        if(self.vely<0):
            self.itemc.y-=1*passos

class item(itens):
    def __init__(self,x,y,cor,lar,alt):
        itens.__init__(self,x,y,cor,lar,alt)
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
  
class cena(itens):
    def __init__(self,x,y,cor,lar,alt):
        itens.__init__(self,x,y,cor,lar,alt)

    