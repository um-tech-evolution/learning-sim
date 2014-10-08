class Params:
	"""
	This is where the model and simulation paramters are set and stored as static variables.
	tb = '\t'
	First, the simulation parameters
	"""
	N = 10000  # the population size
	S = 5  # initial number of social learners
	I = N-S  # initial number of individual learners
	G = 100   # the number of generations
	R = 40   # the number of runs
	"""
	Now, the model parameters:
	"""
	W0 = 2.0   	# base fitness
	Cl = 0.3   	# fitness cost of individual learning (even if learning fails)
	Cs = 0.6   	# cost of social learning (if successful)
	K = 1.0    	# fitness penalty for being a social learner
	D = 1.5    	# fitness increment for having the skill
	n =  5    	# number of previous generation individuals observed by social learner
	delta = 0.2 # probability of success during individual learning
	gamma = 0.0	# probability per generation of an environment change
