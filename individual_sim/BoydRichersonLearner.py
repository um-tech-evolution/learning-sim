from Parameters import Params

class BoydRichersonLearner:
	"""
	"""
	def __init__(self,social=False,isSkilled=False):
		self.social = social
		self.isSkilled = isSkilled
		# The following assumes the new individual in unskilled and learning will take place later
		if self.social:	
			self.fitness = Params.W0 - Params.K
		else:
			self.fitness = Params.W0 

	def __str__(self):
		if self.social:
			result = 'social learner '
		else:
			result = 'individual learner '
		if self.isSkilled:
			result += 'with skill'
		else:
			result += 'without skill'
		fit = self.fitness
		result += ' fitness: '+str(fit)
		return result

	"""
	def fitness(self):   # Assumes self.social and self.isSkilled have been set
		if not self.social:
			if self.isSkilled:
				return Params.W0 - Params.Cl + Params.D
			else:  # not isSkilled
				return Params.W0 - Params.Cl
		else:   #  social
			if self.isSkilled:
				return Params.W0 + Params.D - Params.Cs - Params.K
			else:  # not isSkilled
				return Params.W0 - Params.Cl - Params.K
	"""
