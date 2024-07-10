
import pygame,time,sys

raio=4

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)


class Map():
    def __init__(self,x=800,y=600):
        self.x=x
        self.y=y
        self.window = pygame.display.set_mode((self.x,self.y), 0, 32)
        self.window.fill(BLACK)
        if((x==800) and (y==600)):
            self.linha=5
            self.coluna=5

    def MapUpdate(self,itens):
        #self.window.fill(BLACK)

        for i in itens:
            goal=(i.col*mapa.linha+(raio),i.lin*mapa.coluna+(raio))
            pygame.draw.circle(mapa.window, i.cor, goal, raio-1, 0)
            pygame.display.update()

    def MapUpdateMelhor(self,itens):
        #self.window.fill(BLACK)

        for i in itens:
            if(i.DX==1):
                suavex=raio*1.5
            else:
                suavex=0
            if(i.DY==1):
                suavey=raio*1.5
            else:
                suavey=0
            goal=(i.col*mapa.linha+(suavex),i.lin*mapa.coluna+(suavey))
            pygame.draw.circle(mapa.window, i.cor, goal, raio-1, 0)
            pygame.display.update()

class item():
    def __init__(self,col=1,lin=1,cor=GREEN,vx=1,vy=1):
        self.col=col
        self.lin=lin
        self.cor=cor
        self.DX=vx
        self.DY=vy

pygame.init()



mapa=Map()
itens=[item(),item(5,3,RED)]
while True:
    mapa.MapUpdate(itens)
    time.sleep(0.1)
    #mapa.MapUpdateMelhor(itens)

    for i in itens:
        if(i.DX==1):
            if(i.col<158):
                i.col=i.col+1
            else:
                i.DX=0
        if(i.DX==0):
            if(i.col>0):
                i.col=i.col-1
            else:
                i.col=i.col+1
                i.DX=1
        if(i.DY==1):
            if(i.lin<118):
                i.lin=i.lin+1
            else:
                i.DY=0
        if(i.DY==0):
            if(i.lin>0):
                i.lin=i.lin-1
            else:
                i.lin=i.lin+1
                i.DY=1


	
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
		     
    continue
