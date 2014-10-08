"""
Infinite population simulation of the discrete model from the Boyd Richerson 
     "Cultural Evolution is Rare" (1998) paper.
Author:  Alden Wright   Oct. 2014
"""
# The parameters come from this file which is also used for the indidividual-based simulation.
from Parameters import Params 

tb = '\t'  # shorthand for tab characters

def outParams():
	"""
	Returns a string which shows the parameters on two tab-delimited lines.
	The first line is a header line, and the second line is the values of the parameters.
	"""
	delta = Params.delta
	gamma = Params.gamma
	W0 = Params.W0
	n = Params.n
	D = Params.D
	Cl = Params.Cl
	Cs = Params.Cs
	K = Params.K
	EQ1 = (1.0-(1.0-delta)**n)*(1.0-gamma)*(D*(1.0-gamma)+Cl-Cs)-K  # equation 1 from paper
	EQ2 = (delta*(1.0-gamma)*(D*(1.0-delta)+Cl-Cs))/(gamma+(1-gamma)*delta) - K
	result = 'W0'+tb+'K'+tb+'D'+tb+'delta'+tb+'gamma'+tb+'Cl'+tb+'Cs'+tb+'n'+tb+'EQ1'+tb+'EQ2'+'\n'
	result += str(W0)+tb+str(K)+tb+str(D)+tb+str(delta)+tb+str(gamma)+tb+str(Cl)+tb+str(Cs)
	result += tb+str(n)+tb+str('%0.2f'%EQ1)+tb+str('%0.2f'%EQ2)
	return result

def InfPop():
	"""
	Runs the infinite population simulation.
	See the Parameters.py file and the paper for documentation of the parameters.
	See the file  discrete_model.pdf  for psuedocode and a higher level description of the code.
	"""
	printEveryGeneration = False
	G = Params.G    
	s = Params.S/float(Params.N)
	n = Params.n
	delta = Params.delta
	W0 = Params.W0
	Cl = Params.Cl
	Cs = Params.Cs
	K = Params.K
	D = Params.D
	q = 0.0
	print( outParams() )
	print('gen'+tb+'p'+tb+'q'+tb+'s')
	for g in range(G):
		p = 1.0 - (1.0-q)**n    
		q = (1-s)*delta+s*(p+(1-p)*delta)
		indiv = (1-s)*(1-delta)*(W0-Cl) + (1-s)*delta*(W0+D-Cl) 
		social = s*p*(W0+D-Cs-K) + s*(1-p)*delta*(W0+D-Cl-K) + s*(1.0-p)*(1.0-delta)*(W0+D-Cl-K)
		total = indiv + social
		s = social/total
		if printEveryGeneration:
			print(str(g)+tb+str("%.4f"%p)+tb+str("%.4f"%q)+tb+str("%.4f"%s))
		elif g == G-1:
			print(str(g)+tb+str("%.4f"%p)+tb+str("%.4f"%q)+tb+str("%.4f"%s))

InfPop()
