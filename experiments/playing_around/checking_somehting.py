import pandas as pd

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

#mock_function('something something to say:', 5, 3, 4, 10, 20)


# this was a refresher on *args

# following is a refesher on type checking:

def send_something(something):
    if type(something) == str:
        print('you sent a string')
        
        # designed to be trial and error.
        try:
            new_thing = something * 2
        except:
            pass
            
        print('try another thing')
        try:
            new_thing = something * 3
        except:
            pass

        print('yet, another try')
        try:
            print('hey there')
        except:
            pass

send_something('sdd')

# that was all... 


# checking pandas datetime capabilities

date = pd.to_datetime('3/21/2004')
date_day_first = pd.to_datetime('21/3/2004')
date_unclear = pd.to_datetime('2/1/2004')
date_dash = pd.to_datetime('2-1-2004')
date_year_only = pd.to_datetime('2004')

print(date)
print(date_day_first)
print(date_unclear)
print(date_dash)
print(date_year_only)

# ok I'm done messing around.