import numpy

optimization_constraints = {
    'type': 'eq',
    'fun':  lambda x: numpy.sum(x)-1,
}