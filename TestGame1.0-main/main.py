

import random, time, sys
import pygame
import item


pygame.init()

limitemapx=800
limitemapy=800
raio=1
passos=5

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)

window = pygame.display.set_mode((limitemapx,limitemapy), 0, 32)
window.fill(BLACK)
itens=[]
itens.append(item.chara(150,150,RED,25,50))
itens.append(item.cena(50,250,GREEN,500,20))
itens.append(item.item(100,100,WHITE,25,25))
itens.append(item.item(200,150,YELLOW,10,10))
itens.append(item.item(250,150,YELLOW,10,10))
itens.append(item.item(300,150,YELLOW,10,10))
itens.append(item.item(350,80,YELLOW,10,10))
itens.append(item.cena(250,550,GREEN,500,20))


while True:
    window.fill(BLACK)
    for i in itens:
        if i.ativo==True:
            i.desenha(window)
    pygame.display.update()
    time.sleep(0.01)
    itens[0].vely+=1
    itens[0].move(passos)


    if(itens[0].itemc.colliderect(itens[2].itemc)): #chara caixa
        itens[0].gravi(passos)
        itens[0].vely=1

    if(itens[0].itemc.colliderect(itens[2].itemc)): #chara caixa
        itens[2].velx=itens[0].velx
    else:
        itens[2].velx=0
    

    itens[2].vely+=1
    itens[2].move(passos)
    
    for i in range(3,7):    #chara coins
        if(itens[0].itemc.colliderect(itens[i].itemc)):
            if itens[i].ativo:
                itens[i].ativo=False
	

    if(itens[1].itemc.colliderect(itens[0].itemc)): #chao chara
        itens[0].gravi(passos)
        itens[0].vely=1
    
    if(itens[1].itemc.colliderect(itens[2].itemc)): #chao caixa
        itens[2].gravi(passos)
        itens[2].vely=1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                itens[0].vely=1
            if event.key == pygame.K_LEFT:
                itens[0].velx=-1
            if event.key == pygame.K_RIGHT:
                itens[0].velx=1
            if event.key == pygame.K_UP:
                if itens[0].vely==1:
                    itens[0].vely=-20
            if event.key == pygame.K_r:
                itens=[]
                itens.append(item.chara(150,150,RED,25,50))
                itens.append(item.cena(50,250,GREEN,500,20))
                itens.append(item.item(100,100,WHITE,25,25))
                itens.append(item.item(200,150,YELLOW,10,10))
                itens.append(item.item(250,150,YELLOW,10,10))
                itens.append(item.item(300,150,YELLOW,10,10))
                itens.append(item.item(350,80,YELLOW,10,10))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                itens[0].velx=0
            if event.key == pygame.K_RIGHT:
                itens[0].velx=0


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
		     
    continue

