

def dist2p(ax,ay,bx,by,aredonda=True): #eu nao sei se ja existe uma funcao para calcular a distancia entre 2 pontos,entao eu criei uma.
	d = (((ax-bx)**2)+((ay-by)**2))**(1/2)
	if(aredonda):
		return int(d)
	else:
		return d
	
