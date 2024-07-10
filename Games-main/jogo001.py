#!/bin/python3


import random
import string

senha=[]
alphabet = string.ascii_letters 
senhalen=6
senhavaria=6
letracerta=0
digitocerto=0
tentativasmax=20
tentativas=0

def criasenha(digitlen,digitvar):
	senha=""
	for i in digitlen:
		senha=senha+random.choice(alfa[0:digitvar])
	return senha

def testasenha(senha,tenta):
	
	global letracerta
	global digitocerto
	letracerta=0
	digitocerto=0
	
	for i1 in range(len(tenta)):
		for i2 in range(len(senha)):
			if tenta[l1] == senh[l2]:
				if l1==l1:
					digitocerto+=1
				else:
					letracerta+=1
				break
	

while True:
	senha=criasenha(senhalen,digitovaria)
	while tentativas < tentativasmax:

		
		
	


