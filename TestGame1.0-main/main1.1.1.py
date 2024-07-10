

import random, time, sys
import pygame
import item2 as item


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

def reset(mapa):
    if mapa==1:
        global itens
        itens=[]
        global cena
        cena=[]
        global coins
        coins=[]
        global itemc
        itemc=[]
        itens.append(item.chara(150,150,RED,25,50))
        itens.append(cena)
        itens.append(coins)
        itens.append(itemc)
        itens[1].append(item.cena(50,250,GREEN,500,20))
        itens[1].append(item.cena(50,550,GREEN,700,20))
        itens[2].append(item.item(200,150,YELLOW,10,10))
        itens[2].append(item.item(250,150,YELLOW,10,10))
        itens[2].append(item.item(300,150,YELLOW,10,10))
        itens[2].append(item.item(350,80,YELLOW,10,10))
        itens[3].append(item.item(100,100,WHITE,25,25))
        itens[3].append(item.item(150,100,WHITE,25,25))

reset(1)


while True:
    window.fill(BLACK)
    itens[0].desenha(window)
    for i1 in range(1,4):
        for i2 in itens[i1]:
            if i2.ativo==True:
                i2.desenha(window)


    pygame.display.update()
    time.sleep(0.01)
    itens[0].vely+=1
    itens[0].move(passos)


    if(itens[0].itemc.colliderect(itens[3][0].itemc)): #chara caixa
        itens[0].gravi(passos)
        itens[0].vely=1

    
    if(itens[0].itemc.colliderect(itens[3][0].itemc)): #chara caixa
        itens[3][0].velx=itens[0].velx
    else:
        itens[3][0].velx=0
    

    itens[3][0].vely+=1
    itens[3][0].move(passos)
    
    for i in itens[2]:    #chara coins
        if(itens[0].itemc.colliderect(i.itemc)):
            if i.ativo:
                i.ativo=False
        

    for i in range(2):

        if(itens[1][i].itemc.colliderect(itens[0].itemc)): #chao chara
            itens[0].gravi(passos)
            itens[0].vely=1
        
        if(itens[1][i].itemc.colliderect(itens[3][0].itemc)): #chao caixa
            itens[3][0].gravi(passos)
            itens[3][0].vely=1

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
                reset(1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                itens[0].velx=0
            if event.key == pygame.K_RIGHT:
                itens[0].velx=0


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
		     
    continue

