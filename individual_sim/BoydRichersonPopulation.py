"""
An individual-based simulation of of the discrete model of the
``Cultural evolution is rare'' paper of Boyd Richerson (1996).
Author:  Alden Wright  10/2014
"""
from Parameters import Params
from BoydRichersonLearner import BoydRichersonLearner
import random
tb = '\t'

class BoydRichersonPopulation:
	"""
	
	"""
	#cummulativeDistribution = ()  # a 4-tuple of triples: (fitness,social,skilled)

	def __init__(self,numSocial,popSize=0):
		"""
		Initializes poplation with popSize BoydRichersonIndividuals
		"""
		self.popSize = popSize
		self.numSocial = numSocial
		self.population = list()
		for i in range(numSocial):
			self.population.append( BoydRichersonLearner(social=True) )
		for i in range(popSize-numSocial):
			self.population.append( BoydRichersonLearner(social=False) )
		#self.countSocial = numSocial
		self.previousPopulation = list()
		self.cummulativeDistribution = ()  # a 4-tuple of triples: (fitness,social,skilled)
		self.envChangeLastGeneration = True
		self.envChangeCount = 0
	
	def __str__(self):
		result = ''
		for i in self.population:
			result += i.__str__() + '\n'
		return result

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
		EQ1 = (1.0-(1.0-delta)**n)*(1.0-gamma)*(D*(1.0-gamma)+Cl-Cs)-K
		EQ2 = (delta*(1.0-gamma)*(D*(1.0-delta)+Cl-Cs))/(gamma+(1-gamma)*delta) - K
		result = 'W0'+tb+'K'+tb+'D'+tb+'delta'+tb+'gamma'+tb+'Cl'+tb+'Cs'+tb+'n'+tb+'EQ1'+tb+'EQ2'+'\n'
		result += str(W0)+tb+str(K)+tb+str(D)+tb+str(delta)+tb+str(gamma)+tb+str(Cl)+tb+str(Cs)
		result += tb+str(n)+tb+str('%0.2f'%EQ1)+tb+str('%0.2f'%EQ2)
		return result

	outputParams = staticmethod(outParams)

	def outputResultsHdr():
		"""
		Return a tb-delimited output header with the headings 'gen','indiv', 'social', 'unskill','skilled'
		as a string.
		"""
		return 'gen'+tb+'indiv'+tb+'social'+tb+'unskill'+tb+'skilled'+tb+'gnchCnt'

	outputResultsHeader = staticmethod(outputResultsHdr)

	def countSocialSkilled(self,generation):
		"""
		Count the number of indiv, social,  unskilled, skilled.
		Return as a tb-delimited string
		"""
		countSocial = 0
		countSkilled = 0
		for p in self.population:
			if p.social: 
				countSocial += 1
			if p.isSkilled: 
				countSkilled += 1
		countIndiv = len(self.population)-countSocial
		countUnSkilled = len(self.population)-countSkilled
		return str(generation)+tb+str(countIndiv)+tb+str(countSocial)+tb+str(countUnSkilled)\
			+tb+str(countSkilled)+tb+str(self.envChangeCount)

	def countSocial(self):
		countSocial = 0
		for p in self.population:
			if p.social: 
				countSocial += 1
		#self.countSocial = countSocial
		return countSocial

	def computeCummulativeDistribution(self):
		"""
		This is very specific to this problem.
		"""
		cummDist = list() # a list of triples: (fitness,social,skilled)
		#totalFitness = 0.0
		totalIndivUnskilled = 0.0
		totalSocialUnskilled = 0.0
		totalIndivSkilled = 0.0
		totalSocialSkilled = 0.0
		for i in self.population:
			if i.social and i.isSkilled:
				totalSocialSkilled += i.fitness
			if i.social and not i.isSkilled:
				totalSocialUnskilled += i.fitness
			if not i.social and i.isSkilled:
				totalIndivSkilled += i.fitness
			if not i.social and not i.isSkilled:
				totalIndivUnskilled += i.fitness
		totalFitness = totalSocialSkilled+totalSocialUnskilled+totalIndivSkilled+totalIndivUnskilled
		cummFit = totalSocialSkilled/totalFitness
		cummDist.append( (cummFit,True,True) )
		cummFit += totalSocialUnskilled/totalFitness
		cummDist.append( (cummFit,True,False) )
		cummFit += totalIndivUnskilled/totalFitness
		cummDist.append( (cummFit,False,True) )
		cummFit += totalIndivSkilled/totalFitness
		cummDist.append( (cummFit,False,False) )
		self.cummulativeDistribution = tuple(cummDist)
		#print(  'cummDistribution: ',self.cummulativeDistribution )

	def proportionalSelection(self):
		"""
		This is very specific to this problem.
		"""
		self.computeCummulativeDistribution()
		#print(  'cummDistribution: ',self.cummulativeDistribution )
		self.previousPopulation = list(self.population)
		self.population = list()
		for i in range(Params.N):
			r = random.random()
			for j in self.cummulativeDistribution:
				if r < j[0]:
					# New population members do not inherit skill
					self.population.append(BoydRichersonLearner(social=j[1],isSkilled=False))
					#print(  'r: ',r,'  i: ',i,'  j: ',j )
					break
			
	# Determines whether each population member learns socially by 
	# applying the procedure to determine if an individual learns socially
	# This is to take a random sample of size n of  self.previousPopultion, and learn if any is skilled
	# This routine also decides whether there is an environmental change
	def socialLearn(self):
		if random.random() < Params.gamma:
			self.envChangeLastGeneration = True  # No social learning takes place
			self.envChangeCount += 1
		else:
			self.envChangeLastGeneration = False  # Social learning takes place
			for p in self.population:
				if p.social and not p.isSkilled:
					sample = random.sample(self.previousPopulation,min(Params.n,len(self.previousPopulation)))
					for s in sample:
						if s.isSkilled:
							p.isSkilled = True
							p.fitness += -Params.Cs + Params.D
							break

	# Determines whether each population member learns individually by 
	# flipping a biased coin with probability Params.delta.
	def individualLearn(self):
		for p in self.population:
			if not p.isSkilled and random.random() < Params.delta:
				p.isSkilled = True
				p.fitness += -Params.Cl + Params.D
	
if __name__ == '__main__':
	delta = Params.delta
	n = Params.n
	gamma = Params.gamma
	D = Params.D
	Cl = Params.Cl
	Cs = Params.Cs
	K = Params.K
	eq1 = (1.0-(1.0-delta)**n)*(1.0-gamma)*(D*(1.0-gamma)+Cl-Cs)-K
	print( "EQ1: Social only ESS when > 0: ",eq1 )
	eq2 = (delta*(1.0-gamma)*(D*(1.0-delta)+Cl-Cs))/(gamma+(1-gamma)*delta) - K
	print( "EQ2: Social is an ESS when n = 1 and eq2 > 0: ",eq2 )
	print( BoydRichersonPopulation.outputParams() )
	#print(  'Initial pop' )
	#print(  pop )
	print( BoydRichersonPopulation.outputResultsHeader() )
	#print(  pop.countSocialSkilled(0) )
	for r in range(Params.R):
		pop = BoydRichersonPopulation(popSize=Params.N,numSocial=Params.S)
		for g in range(Params.G):
			gLast = g+1
			pop.socialLearn()
			#print(  'pop after social learn\n',pop )
			pop.individualLearn()
			#print(  'pop after individual learn\n',pop )
			#print( ( pop.countSocialSkilled(g+1)) )
			nSocial = pop.countSocial()
			#print(  "nSocial: ",nSocial,"  N:",Params.N )
			if (nSocial == 0) or (nSocial == Params.N):
				break
			if g != Params.G-1:
				pop.proportionalSelection()
			#print(  'pop after proportional selection\n',pop )
		print( pop.countSocialSkilled(gLast) )
