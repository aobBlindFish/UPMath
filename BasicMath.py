import sys, random


def c_round(a, rounder=2, method="normal") -> float:
    #var security
    if type(a) not in [int, float] or type(rounder) not in [int, float]:
        sys.exit("c_round: invalid var type")
    #var preparation
    if abs(rounder) >= 9:
        rounder = 9
    rounder = round(abs(rounder))
    #calculation
    if type(method) != bool:
        #standart rounding
        output = round((a*(10**rounder)))/(10**rounder)
    elif method:
        #round up
        output = (int((a*(10**rounder)))+1)/(10**rounder)
    else:
        #round down
        output = int((a*(10**rounder)))/(10**rounder)
    if round(output) == output:
        output = int(output)
    return output

def c_comp(a, b, rounder=None, rounder_method="normal") -> bool:
    #var security
    if type(a) not in [int, float] or type(b) not in [int, float]:
        sys.exit("c_comp: invalid var type")
    #basic case
    if type(rounder) in [int, float]:
        a = c_round(a, rounder, rounder_method)
        b = c_round(b, rounder, rounder_method)
    return a == b

def c_range(bottom, constant, top, rounder=2, rounder_method="normal") -> bool: #true if bottom < constant < top
    output = False
    #var security
    if bottom >= top:
        return False
    #var calculation
    bottom = c_round(bottom, rounder, rounder_method)
    constant = c_round(constant, rounder, rounder_method)
    top = c_round(top, rounder, rounder_method)
    if bottom < constant < top:
        output = True
    return output

def if_prime(a) -> bool:
    try:
        a = int(a)
        if a <= 1:
            return False
        number_list = []
        for i in range(a - 2):
            number_list.append(i + 2)
        for number in number_list:
            if a % number == 0:
                return False
        return True
    except ValueError:
        return False

def ran_num(start, stop):
    return random.randint(start, stop)

def list_rev(a):
    #var security
    if type(a) != list:
        sys.exit("list_rev: incorrect data type")
    
    output = []
    for i in range(len(a)):
        output.append(a[-1-i])

    return output
