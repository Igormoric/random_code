

def dist2p(ax,ay,bx,by,aredonda=True):
	d = (((ax-bx)**2)+((ay-by)**2))**(1/2)
	if(aredonda):
		return int(d)
	else:
		return d
	