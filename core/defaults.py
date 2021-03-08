from numpy.core.fromnumeric import sum as numpy_sum

optimization_constraints = {
    'type': 'eq',
    'fun':  lambda x: numpy_sum(x)-1,
}