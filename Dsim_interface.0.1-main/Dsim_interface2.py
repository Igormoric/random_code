
from matgeo import dist2p	#eu nao sei se ja existe uma funcao para calcular a distancia entre 2 pontos,entao eu criei uma.
import random
import pygame,sys
from pygame.locals import *
import time


pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)



class pessoa:	#clase q cria pessoa
	def __init__(self,x,y,numero,d=0):
		self.x=x	#posicao horizontal da pessoa
		self.y=y	#posicao vertical da pessoa
		self.d=d	#se a pessoa esta doente(ou nivel de contaminacao)
		self.id=numero	#identifica a pessoa

class simu:	#o programa em si
	def __init__(self,tempo,contamidados,populacao,perigod=5,perigoc=5,mapa=100):	#prepara a simulacao
		self.populacao=[]	#todas as pessoas
		self.populacaoc=[]	#todas as pessoas doentes
		self.tempolimite=tempo	#quanto tempo vai durar a simulacao
		self.npd=perigod	#chance de se contaminar
		self.npc=perigoc	#distancia para se contaminar
		self.limitemap=mapa	#tamanho maximo do mapa
		self.window = pygame.display.set_mode((self.limitemap, self.limitemap), 0, 32)
		pygame.display.set_caption('grafic simu')
		for i in range(populacao):	#cria as pessoas na simulacao
			self.populacao.append(pessoa(random.randint(1,self.limitemap),random.randint(1,self.limitemap),i))
		for i in range(contamidados):	#contamina x pessoas na simulacao
			x=random.randint(1,populacao)
			while(self.populacao[x] in self.populacaoc):
				x=random.randint(1,populacao)
			self.populacao[x].d=self.npc
			self.populacaoc.append(self.populacao[x])	#uma lista de pessoas contaminadas
			#self.listamedia()
			
	def pessoamov(self,pessoa):	#simula o movimento das pessoas
		dire=random.randint(1,9)
		if((dire==7)or(dire==8)or(dire==9)):
			if(pessoa.x<self.limitemap):
				pessoa.x+=1
		if((dire==3)or(dire==6)or(dire==9)):
			if(pessoa.y<self.limitemap):
				pessoa.y+=1
		if((dire==7)or(dire==4)or(dire==1)):
			if(pessoa.y>1):
				pessoa.y-=1
		if((dire==1)or(dire==2)or(dire==3)):
			if(pessoa.x>1):
				pessoa.x-=1
	
	def pessoacontamina(self):	#simula a contaminacao
		for pessoa in self.populacaoc:	#primeiro ve se estao proximos o suficiente para contaminar
			for i in self.populacao:
				if i not in self.populacaoc:
					if((dist2p(pessoa.x,pessoa.y,i.x,i.y)<self.npd)):
						i.d+=2
		for i in self.populacao:	#depois ve se ficou perto por muito tempo ou muitas pessoas contamidadas
			if(i.d>self.npc-1):
				if i not in self.populacaoc:
					i.d=self.npc
					self.populacaoc.append(i)
			else:
                                if(i.d>1):
                                        i.d-=1
	def listamedia(self):	#informa quantas pessoas estao doentes
		print("{} pessoas doentes de {}".format(len(self.populacaoc),len(self.populacao)))
      
	def getvar(self):	#para rever os valores das variaves
		print("tempo:{}\npessoas:{}\nnivel de perigo:{}\ninfectados:{}".format(self.tempolimite,len(self.populacao),self.npd,len(self.populacaoc)))
                                        
	def start(self):	#inicia a simulacao em si
		self.window.fill(BLACK)	#desenha o mapa
		for d in range(0,self.tempolimite):
			self.window.fill(BLACK)	#limpa o mapa
			for i in self.populacao:
				self.pessoamov(i)
			self.pessoacontamina()
			
			for p in test.populacao:	#define cor para rastrear os doentes
				if(p.d==0):
					cor=GREEN
				if(p.d>0 and p.d<5):
					cor=YELLOW
				if(p.d>=5):
					cor=RED
				posisao=(p.x,p.y)
				pygame.draw.circle(self.window, cor, posisao, self.npc, 0)	
			pygame.display.update()
			
			print("dia:{} ".format(d+1))
			self.listamedia()
			time.sleep(0.1)
			if(len(self.populacao)==len(self.populacaoc)):	#cancela a simulacao se todos estao doentes
                                break
                               
                                        
#test=simu(1000,5,1000,mapa=400)
test=simu(50,5,1000,mapa=200)
test.start()
input()
            
            
