
import pygame

class itens():
    def __init__(self,x,y,cor,lar,alt):
        self.itemrc=pygame.Rect(x,y,lar,alt)
        self.itemrr=pygame.Rect(x+lar,y,5,alt)
        self.itemrl=pygame.Rect(x-5,y,5,alt)
        self.itemrd=pygame.Rect(x-5,y+alt,lar+10,5)
        self.cor=cor
        self.velx=0
        self.vely=0
        self.ativo=True
        self.moveu=True
        self.grav=True

    def desenha(self,window):
        pygame.draw.rect(window,self.cor,self.itemrc)

    def move(self,itens,passos):
        if self.moveu==True:

            if(self.velx>0):
                self.itemrc.x+=1*passos
                self.itemrd.x+=1*passos
                self.itemrl.x+=1*passos
                self.itemrr.x+=1*passos
                #self.itemc.x+=1*passos
            if(self.velx<0):
                self.itemrc.x-=1*passos
                self.itemrd.x-=1*passos
                self.itemrl.x-=1*passos
                self.itemrr.x-=1*passos
            if(self.vely>0):
                for i1 in range(len(itens)):
                    if i1 == 0:
                        continue
                    for i2 in range(len(itens[i1])):
                        if itens[i1][i2].ativo==True:
                            if(self.itemrd.colliderect(itens[i1][i2].itemrc)):
                                self.vely=0   #gravidade
                if(self.vely>0):
                    self.itemrc.y+=1*passos
                    self.itemrd.y+=1*passos
                    self.itemrl.y+=1*passos
                    self.itemrr.y+=1*passos

            if(self.vely<0):
                self.itemrc.y-=1*passos
                self.itemrd.y-=1*passos
                self.itemrl.y-=1*passos
                self.itemrr.y-=1*passos
    def gravi(self):
        self.vely+=1


class chara(itens):
    def __init__(self,x,y,cor,lar,alt):
        itens.__init__(self,x,y,cor,lar,alt)  
        self.ponto=0

class item(itens):
    def __init__(self,x,y,cor,lar,alt):
        itens.__init__(self,x,y,cor,lar,alt)
        
 
class cena(itens):
    def __init__(self,x,y,cor,lar,alt):
        itens.__init__(self,x,y,cor,lar,alt)
        self.moveu=False