def mock_function(thingy, *arguments):
    print(thingy)
    calc_in_function = arguments[0] + arguments[1] + arguments[2]
    print(calc_in_function)
    
    inner_function(arguments[0], arguments[1], arguments[3])

    uncertain_function(thingy, arguments[0], arguments[2])



def inner_function(arg1, arg2, arg3):
    print('This is done in the inner function')
    inner_calc = arg1 * arg2 + arg3
    return inner_calc

def uncertain_function(certain_arg, *uncertain_args):
    print(certain_arg)
    print('this is done in an uncertain function')
    for each in uncertain_args:
        print(each)

mock_function('something something to say:', 5, 3, 4, 10, 20)


# this was a refresher on *args