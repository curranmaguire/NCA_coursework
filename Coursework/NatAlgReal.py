#################################################################################
#### PLEASE READ ALL COMMENTS BELOW AND MAKE SURE YOU FOLLOW MY INSTRUCTIONS ####
#################################################################################

# This is the skeleton program 'NatAlgReal.py' around which you should build your implementation.
# Please read through this program and follow the instructions given.

# There are no input or output files, with the_MINSparams_mins printed to the standard output.

# As regards the two values to be entered below
# - make sure that the first two values appear within double quotes
# - make sure that no comments are inserted after you have entered the values.

# Ensure that your implementation works for *arbitrary* hard-coded functions of arbitrary
# dimension and arbitray min- and max-ranges!

##############################
#### ENTER YOUR USER-NAME ####
##############################

username = "cgmj52"

###############################################################
#### ENTER THE CODE FOR THE ALGORITHM YOU ARE IMPLEMENTING ####
###############################################################

alg_code = "WO"

################################################################
#### DO NOT TOUCH ANYTHING BELOW UNTIL I TELL YOU TO DO SO! ####
####      THIS INCLUDES IMPORTING ADDITIONAL MODULES!       ####
################################################################

import time
import random
import math
import sys
import os
import datetime


def compute_f(point):
    f = (
        40
        + (point[0] ** 2 - 10 * math.cos(2 * math.pi * point[0]))
        + (point[1] ** 2 - 10 * math.cos(2 * math.pi * point[1]))
        + (point[2] ** 2 - 10 * math.cos(2 * math.pi * point[2]))
        + (point[3] ** 2 - 10 * math.cos(2 * math.pi * point[3]))
    )
    return f


n = 4

min_range = [-5.12, -5.12, -5.12, -5.12]
max_range = [5.12, 5.12, 5.12, 5.12]

start_time = time.time()

#########################################################################################
#### YOU SHOULDN'T HAVE TOUCHED *ANYTHING* UP UNTIL NOW APART FROM SUPPLYING VALUES  ####
####                 FOR 'username' and 'alg_code' AS REQUESTED ABOVE.               ####
####                        NOW READ THE FOLLOWING CAREFULLY!                        ####
#########################################################################################

# The function 'f' is 'n'-dimensional and you are attempting to MINIMIZE it.
# To compute the value of 'f' at some point 'point', where 'point' is a list of 'n' integers or floats,
# call the function 'compute_f(point)'.
# The ranges for the values of the components of 'point' are given above. The lists 'min_range' and
# 'max_range' above hold the minimum and maximum values for each component and you should use these
# list variables in your code.

# On termination your algorithm should be such that:
#   - the reserved variable 'min_f' holds the minimum value that you have computed for the
#     function 'f'
#   - the reserved variable 'minimum' is a list of 'n' entries (integer or float) holding the point at which
#     your value of 'min_f' is attained.

# Note that the variables 'username', 'alg_code', 'f', 'point', 'min_f', 'n', 'min_range', 'max_range' and
# 'minimum' are all reserved.

# FOR THE RESERVED VARIABLES BELOW, YOU MUST ENSURE THAT ON TERMINATION THE TYPE
# OF THE RESPECTIVE VARIABLE IS AS SHOWN.

#  - 'min_f'                int or float
#  - 'minimum'              list of int or float

# You should ensure that your code works on any function hard-coded as above, using the
# same reserved variables and possibly of a dimension different to that given above. I will
# run your code with a different such function/dimension to check that this is the case.

# The various algorithms all have additional parameters (see the lectures). These parameters
# are detailed below and are referred to using the following reserved variables.
#
# AB (Artificial Bee Colony)
#   - 'n' = dimension of the optimization problem       int
#   - 'num_cyc' = number of cycles to iterate           int
#   - 'N' = number of employed bees / food sources      int
#   - 'M' = number of onlooker bees                     int
#   - 'lambbda' = limit threshold                       float or int
#
# FF (Firefly)
#   - 'n' = dimension of the optimization problem       int
#   - 'num_cyc' = number of cycles to iterate           int
#   - 'N' = number of fireflies                         int
#   - 'lambbda' = light absorption coefficient          float or int
#   - 'alpha' = scaling parameter                       float or int
#
# CS (Cuckoo Search)
#   - 'n' = dimension of optimization problem           int
#   - 'num_cyc' = number of cycles to iterate           int
#   - 'N' = number of nests                             int
#   - 'p' = fraction of local flights to undertake      float or int
#   - 'q' = fraction of nests to abandon                float or int
#   - 'alpha' = scaling factor for Levy flights         float or int
#   - 'beta' = parameter for Mantegna's algorithm       float or int
#
# WO (Whale Optimization)
#   - 'n' = dimension of optimization problem           int
#   - 'num_cyc' = number of cycles to iterate           int
#   - 'N' = number of whales                            int
#   - 'b' = spiral constant                             float or int
#
# BA (Bat)
#   - 'n' = dimension of optimization problem           int
#   - 'num_cyc' = number of cycles to iterate           int
#   - 'N' = number of fireflies                         int
#   - 'sigma' = scaling factor                          float or int
#   - 'f_min' = minimum frequency                       float or int
#   - 'f_max' = maximum frequency                       float or int

# These are reserved variables and need to be treated as such, i.e., use these names for these
# parameters and don't re-use the names. Don't forget to ensure that on termination all the above
# variables have the stated type. In particular, if you use specific numpy types then you'll need
# to ensure that they are changed prior to termination (this is checked).

# INITIALIZE THE ACTUAL PARAMETERS YOU USE FOR YOUR ALGORITHM BELOW. ENSURE THAT YOU INITIALIZE
# *ALL* OF THE PARAMETERS REQUIRED APPROPRIATELY (SEE ABOVE) FOR YOUR CHOSEN ALGORITHM.

# In summary, before you input the bulk of your code, ensure that you:
# - import any (legal) modules you wish to use in the space provided below
# - initialize your parameters in the space provided below
# - ensure that reserved variables have the correct type on termination.

###########################################
#### NOW YOU CAN ENTER YOUR CODE BELOW ####
###########################################
####################################################
#### FIRST IMPORT ANY MODULES IMMEDIATELY BELOW ####
####################################################
import random
import math
from collections import Counter

##########################################################
#### NOW INITIALIZE YOUR PARAMETERS IMMEDIATELY BELOW ####
##########################################################
num_cyc = 3
b = 1
N = 20


def create_population(N, n):
    population = []
    for _ in range(N):
        whale = [random.uniform(min_range[i], max_range[i]) for i in range(n)]

        population.append((compute_f(whale), whale))
    return population


def calc_fittest(population):
    """
    give the fitness of the whales by running them in the function
    return the fittest
    """
    return min(population)


def manhattan_distance(fittest, whale, n):
    distance = 0
    for i in range(n):
        distance = distance + abs(fittest[i] + whale[i])
    return distance


def circle_whale(n, new_whale, comparison_whale, whale, C, A, max_range, min_range):
    for i in range(n):
        D = abs(C[i] * comparison_whale[1][i] - whale[1][i])
        new_whale[i] = comparison_whale[1][i] - A[i] * D
        if new_whale[i] > max_range[i]:
            new_whale[i] = max_range[i]
        elif new_whale[i] < min_range[i]:
            new_whale[i] == min_range[i]
    return (compute_f(new_whale), new_whale)


def search_whale(n, new_whale, comparison_whale, whale, C, A, max_range, min_range):
    for i in range(n):
        D = abs(C[i] * comparison_whale[i] - whale[1][i])
        new_whale[i] = comparison_whale[i] - A[i] * D
        if new_whale[i] > max_range[i]:
            new_whale[i] = max_range[i]
        elif new_whale[i] < min_range[i]:
            new_whale[i] == min_range[i]
        return (compute_f(new_whale), new_whale)


def attacking_whale(
    n, new_whale, comparison_whale, whale, C, A, max_range, min_range, l, b
):
    for i in range(n):
        D = abs(comparison_whale[1][i] - whale[1][i])
        new_whale[i] = (
            comparison_whale[1][i] + math.exp(l * b) * math.cos(2 * math.pi * l) * D
        )
        if new_whale[i] > max_range[i]:
            new_whale[i] = max_range[i]
        elif new_whale[i] < min_range[i]:
            new_whale[i] == min_range[i]
    return (compute_f(new_whale), new_whale)


def whale_algorithm(n, num_cyc, N, b):
    """
    - 'n' = dimension of optimization problem           int
    - 'num_cyc' = number of cycles to iterate           int
    - 'N' = number of whales                            int
    - 'b' = spiral constant                             float or int
    """
    # create the initial population and get the fittest whale
    population = create_population(N, n)
    fittest_whale = calc_fittest(population)

    cycle = 1
    while num_cyc >= cycle:
        # update a
        a = 2 - (2 / num_cyc) * cycle

        for i, whale in enumerate(population):
            if whale == fittest_whale:
                continue
            # update A,C,l,p
            r = [0] * n
            C = [0] * n

            A = [0] * n
            for i in range(n):
                r[i] = random.random()
                C[i] = 2 * r[i]
                A[i] = a * (2 * r[i] - 1)

            l = random.uniform(
                -1, 1 - (2 * cycle) / num_cyc
            )  # ensures that it gets less as cycles increase
            p = random.random()
            new_whale = [0] * n
            if p < 0.8:
                if abs(sum(A)) < l:  # circle A can be found differently
                    population[i] = circle_whale(
                        n, new_whale, fittest_whale, whale, C, A, max_range, min_range
                    )
                else:  # search
                    population[i] = search_whale(
                        n,
                        new_whale,
                        random.choice(population)[1],
                        whale,
                        C,
                        A,
                        max_range,
                        min_range,
                    )

            else:
                population[i] = attacking_whale(
                    n, new_whale, fittest_whale, whale, C, A, max_range, min_range, l, b
                )

        fittest_whale = calc_fittest(population)
        cycle += 1
    return fittest_whale


"""
ways to optimise:
    changing the P chance
    ammend the encircling formula

    """


def parameter_tuning(num_cyc_values, N_values, b_values):
    params_mins = []
    for i in range(20):
        for num_cyc in num_cyc_values:
            for N in N_values:
                for b in b_values:
                    min_f, minimum = whale_algorithm(n, num_cyc, N, b)
                    params_mins.append([round(min_f), num_cyc, N, b])
    params_mins.sort()
    mins = []
    for i in range(10):
        print(f" minimum was: {params_mins[i][0]}\n")
    params_mins = [tuple(result) for result in params_mins]
    zeros = [i for i in params_mins if i[0] == 0]
    # Count occurrences of parameter combinations
    param_counts = Counter(zeros)

    # Find the most common parameter combinations
    most_common_params = param_counts.most_common(len(zeros))

    print("Most common parameter combinations:")
    for params, count in most_common_params:
        print(f"Parameters: {params}, Occurrences: {count}")


num_cyc_values = [
    50,
    100,
    150,
    200,
    300,
    400,
    500,
    600,
]
N_values = [70, 75, 80, 85, 90, 95, 100, 110, 120]
b_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
parameter_tuning(num_cyc_values, N_values, b_values)
min_f, minimum = whale_algorithm(n, 600, 80, 0.3)

###########################################
#### NOW INCLUDE THE REST OF YOUR CODE ####
###########################################
"""
Most common parameter combinations:
Parameters: (0, 50, 95, 0.1), Occurrences: 2
Parameters: (0, 50, 95, 0.5), Occurrences: 1
Parameters: (0, 50, 110, 0.3), Occurrences: 1
Parameters: (0, 100, 70, 0.5), Occurrences: 1
Parameters: (0, 100, 75, 0.4), Occurrences: 1
Parameters: (0, 100, 80, 0.1), Occurrences: 1
Parameters: (0, 100, 90, 0.5), Occurrences: 1
Parameters: (0, 100, 95, 0.2), Occurrences: 1
Parameters: (0, 100, 110, 0.5), Occurrences: 1
Parameters: (0, 100, 110, 0.6), Occurrences: 1
Parameters: (0, 150, 70, 0.1), Occurrences: 1
Parameters: (0, 150, 70, 0.6), Occurrences: 1
Parameters: (0, 150, 80, 0.1), Occurrences: 1
Parameters: (0, 150, 85, 0.4), Occurrences: 1
Parameters: (0, 150, 110, 0.4), Occurrences: 1
Parameters: (0, 200, 85, 0.4), Occurrences: 1
Parameters: (0, 200, 95, 0.3), Occurrences: 1
Parameters: (0, 200, 100, 0.2), Occurrences: 1
Parameters: (0, 200, 110, 0.6), Occurrences: 1
Parameters: (0, 300, 75, 0.6), Occurrences: 1
Parameters: (0, 300, 90, 0.6), Occurrences: 1
Parameters: (0, 300, 95, 0.6), Occurrences: 1
Parameters: (0, 300, 110, 0.1), Occurrences: 1
Parameters: (0, 300, 120, 0.5), Occurrences: 1
Parameters: (0, 400, 80, 0.1), Occurrences: 1
Parameters: (0, 400, 85, 0.5), Occurrences: 1
Parameters: (0, 400, 90, 0.6), Occurrences: 1
Parameters: (0, 400, 120, 0.2), Occurrences: 1
Parameters: (0, 500, 70, 0.3), Occurrences: 1
Parameters: (0, 500, 80, 0.1), Occurrences: 1
Parameters: (0, 500, 85, 0.3), Occurrences: 1
Parameters: (0, 500, 90, 0.6), Occurrences: 1
Parameters: (0, 500, 100, 0.6), Occurrences: 1
Parameters: (0, 500, 110, 0.5), Occurrences: 1
Parameters: (0, 500, 120, 0.2), Occurrences: 1
Parameters: (0, 600, 75, 0.3), Occurrences: 1
Parameters: (0, 600, 80, 0.5), Occurrences: 1
Parameters: (0, 600, 80, 0.6), Occurrences: 1
Parameters: (0, 600, 100, 0.3), Occurrences: 1
Parameters: (0, 600, 120, 0.6), Occurrences: 1
"""
#########################################################
#### YOU SHOULD HAVE NOW FINISHED ENTERING YOUR CODE ####
####     DO NOT TOUCH ANYTHING BELOW THIS COMMENT    ####
#########################################################

# At this point in the execution, you should have computed your minimum value for the function 'f' in the
# variable 'min_f' and the variable 'minimum' should hold a list containing the values of the point 'point'
# for which function 'f(point)' attains your minimum.

now_time = time.time()
elapsed_time = round(now_time - start_time, 1)

error = []

try:
    n
    try:
        y = n
    except:
        error.append("*** error: 'n' has not been initialized")
        n = -1
except:
    error.append("*** error: the variable 'n' does not exist\n")
    n = -1
try:
    num_cyc
    try:
        y = num_cyc
    except:
        error.append("*** error: 'num_cyc' has not been initialized")
        num_cyc = -1
except:
    error.append("*** error: the variable 'num_cyc' does not exist")
    num_cyc = -1

if alg_code == "AB":
    try:
        N
        try:
            y = N
        except:
            error.append("*** error: 'N' has not been initialized")
            N = -1
    except:
        error.append("*** error: the variable 'N' does not exist")
        N = -1
    try:
        M
        try:
            y = M
        except:
            error.append("*** error: 'M' has not been initialized")
            M = -1
    except:
        error.append("*** error: the variable 'M' does not exist")
        M = -1
    try:
        lambbda
        try:
            y = lambbda
        except:
            error.append("*** error: 'lambbda' has not been initialized")
            lambbda = -1
    except:
        error.append("*** error: the variable 'lambbda' does not exist")
        lambbda = -1
if alg_code == "FF":
    try:
        N
        try:
            y = N
        except:
            error.append("*** error: 'N' has not been initialized")
            N = -1
    except:
        error.append("*** error: the variable 'N' does not exist")
        N = -1
    try:
        alpha
        try:
            y = alpha
        except:
            error.append("*** error: 'alpha' has not been initialized")
            alpha = -1
    except:
        error.append("*** error: the variable 'alpha' does not exist")
        alpha = -1
    try:
        lambbda
        try:
            y = lambbda
        except:
            error.append("*** error: 'lambbda' has not been initialized")
            lambbda = -1
    except:
        error.append("*** error: the variable 'lambbda' does not exist")
        lambbda = -1
if alg_code == "CS":
    try:
        N
        try:
            y = N
        except:
            error.append("*** error: 'N' has not been initialized")
            N = -1
    except:
        error.append("*** error: the variable 'N' does not exist")
        N = -1
    try:
        p
        try:
            y = p
        except:
            error.append("*** error: 'p' has not been initialized")
            p = -1
    except:
        error.append("*** error: the variable 'p' does not exist")
        p = -1
    try:
        q
        try:
            y = q
        except:
            error.append("*** error: 'q' has not been initialized")
            q = -1
    except:
        error.append("*** error: the variable 'q' does not exist")
        q = -1
    try:
        alpha
        try:
            y = alpha
        except:
            error.append("*** error: 'alpha' has not been initialized")
            alpha = -1
    except:
        error.append("*** error: the variable 'alpha' does not exist")
        alpha = -1
    try:
        beta
        try:
            y = beta
        except:
            error.append("*** error: 'beta' has not been initialized")
            beta = -1
    except:
        error.append("*** error: the variable 'beta' does not exist")
        beta = -1
if alg_code == "WO":
    try:
        N
        try:
            y = N
        except:
            error.append("*** error: 'N' has not been initialized")
            N = -1
    except:
        error.append("*** error: the variable 'N' does not exist")
        N = -1
    try:
        b
        try:
            y = b
        except:
            error.append("*** error: 'b' has not been initialized")
            b = -1
    except:
        error.append("*** error: the variable 'b' does not exist")
        b = -1
if alg_code == "BA":
    try:
        sigma
        try:
            y = sigma
        except:
            error.append("*** error: 'sigma' has not been initialized")
            sigma = -1
    except:
        error.append("*** error: the variable 'sigma' does not exist")
        sigma = -1
    try:
        f_max
        try:
            y = f_max
        except:
            error.append("*** error: the variable 'f_max' has not been initialized")
            f_max = -1
    except:
        error.append("*** error: the variable 'f_max' does not exist")
        f_max = -1
    try:
        f_min
        try:
            y = f_min
        except:
            error.append("*** error: 'f_min' has not been initialized")
            f_min = -1
    except:
        error.append("*** error: the variable 'f_min' does not exist")
        f_min = -1

if type(n) != int:
    error.append(
        "*** error: 'n' is not an integer: it is {0} and it has type {1}".format(
            n, type(n)
        )
    )
if type(num_cyc) != int:
    error.append(
        "*** error: 'num_cyc' is not an integer: it is {0} and it has type {1}".format(
            num_cyc, type(num_cyc)
        )
    )

if alg_code == "AB":
    if type(N) != int:
        error.append(
            "*** error: 'N' is not an integer: it is {0} and it has type {1}".format(
                N, type(N)
            )
        )
    if type(M) != int:
        error.append(
            "*** error: 'M' is not an integer: it is {0} and it has type {1}".format(
                M, type(M)
            )
        )
    if type(lambbda) != int and type(lambbda) != float:
        error.append(
            "*** error: 'lambbda' is not an integer or a float: it is {0} and it has type {1}".format(
                lambbda, type(lambbda)
            )
        )

if alg_code == "FF":
    if type(N) != int:
        error.append(
            "*** error: 'N' is not an integer: it is {0} and it has type {1}".format(
                N, type(N)
            )
        )
    if type(lambbda) != int and type(lambbda) != float:
        error.append(
            "*** error: 'lambbda' is not an integer or a float: it is {0} and it has type {1}".format(
                lambbda, type(lambbda)
            )
        )
    if type(alpha) != int and type(alpha) != float:
        error.append(
            "*** error: 'alpha' is not an integer or a float: it is {0} and it has type {1}".format(
                alpha, type(alpha)
            )
        )

if alg_code == "CS":
    if type(N) != int:
        error.append(
            "*** error: 'N' is not an integer: it is {0} and it has type {1}".format(
                N, type(N)
            )
        )
    if type(p) != int and type(p) != float:
        error.append(
            "*** error: 'p' is not an integer or a float: it is {0} and it has type {1}".format(
                p, type(p)
            )
        )
    if type(q) != int and type(q) != float:
        error.append(
            "*** error: 'q' is not an integer or a float: it is {0} and it has type {1}".format(
                q, type(q)
            )
        )
    if type(alpha) != int and type(alpha) != float:
        error.append(
            "*** error: 'alpha' is not an integer or a float: it is {0} and it has type {1}".format(
                alpha, type(alpha)
            )
        )
    if type(beta) != int and type(beta) != float:
        error.append(
            "*** error: 'beta' is not an integer or a float: it is {0} and it has type {1}".format(
                beta, type(beta)
            )
        )

if alg_code == "WO":
    if type(N) != int:
        error.append(
            "*** error: 'N' is not an integer: it is {0} and it has type {1}\n".format(
                N, type(N)
            )
        )
    if type(b) != int and type(b) != float:
        error.append(
            "*** error: 'b' is not an integer or a float: it is {0} and it has type {1}".format(
                b, type(b)
            )
        )

if alg_code == "BA":
    if type(sigma) != int and type(sigma) != float:
        error.append(
            "*** error: 'sigma' is not an integer or a float: it is {0} and it has type {1}".format(
                sigma, type(sigma)
            )
        )
    if type(f_min) != int and type(f_min) != float:
        error.append(
            "*** error: 'f_min' is not an integer or a float: it is {0} and it has type {1}".format(
                f_min, type(f_min)
            )
        )
    if type(f_max) != int and type(f_max) != float:
        error.append(
            "*** error: 'f_max' is not an integer or a float: it is {0} and it has type {1}".format(
                f_max, type(f_max)
            )
        )

if type(min_f) != int and type(min_f) != float:
    error.append("*** error: there is no real-valued variable 'min_f'")
if type(minimum) != list:
    error.append("*** error: there is no tuple 'minimum' giving the minimum point")
elif type(n) == int and len(minimum) != n:
    error.append(
        "*** error: there is no {0}-tuple 'minimum' giving the minimum point; you have a {1}-tuple".format(
            n, len(minimum)
        )
    )
elif type(n) == int:
    for i in range(0, n):
        if not "int" in str(type(minimum[i])) and not "float" in str(type(minimum[i])):
            error.append(
                "*** error: the value for component {0} (ranging from 1 to {1}) in the minimum point is not numeric\n".format(
                    i + 1, n
                )
            )

if error != []:
    print("\n*** ERRORS: there were errors in your execution:")
    length = len(error)
    for i in range(0, length):
        print(error[i])
    print("\n Fix these errors and run your code again.\n")
else:
    print(
        "\nYou have found a minimum value of {0} and a minimum point of {1}.".format(
            min_f, minimum
        )
    )
    print("Your elapsed time was {0} seconds.\n".format(elapsed_time))
