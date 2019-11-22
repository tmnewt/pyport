def forceYesNo():
    '''Asks for input in terms of Yes\\No answer.

    Returns string \'Y\' or \'N\'

    Will continue to ask until answered with \'Y\' or \'N\''''

    hold = True
    while hold:
        response = input('Please answer with \'Y\' or \'N\'\n')
        response = response.upper()
        if response in ('Y', 'N'):
            hold = False
    return response

def ask_to_display(question_asked, thing_to_display):
    print(question_asked)
    question_answer = forceYesNo()
    if question_answer == 'Y':
        print(thing_to_display)


def pause_output():
    output_hold = True
    while output_hold:
        input('\nPress return key to continue.\n')
        output_hold = False