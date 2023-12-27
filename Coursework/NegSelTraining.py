#################################################################################
#### PLEASE READ ALL COMMENTS BELOW AND MAKE SURE YOU FOLLOW MY INSTRUCTIONS ####
#################################################################################

# This is the skeleton program 'NegSelTraining.py' around which you should build your implementation.

# The training set should be in a file 'self_training.txt' (in the same folder as this program).

# The output is a detector set that is in the file 'detector_<timestamp>.txt' where '<timestamp>' is a timestamp
# so that you do not overwrite previously produced detector sets. You can always rename these files.

# In summary, it is assumed that 'NegSelTraining.py' and 'self_training.txt' are in the same folder
# and that the file containing the detector set is written in this folder.

# As regards the four values to be entered below
# - make sure that no comments are inserted after you have entered the values
# - make sure that the first two values appear within double quotes
# - make sure that the type of 'threshold' is int or float
# - make sure that the type of 'num_detectors' is int.

# Ensure that your implementation works for data of *general* dimension n and not just for the
# particular dimension of the given data sets!

##############################
#### ENTER YOUR USER-NAME ####
##############################

username = "cgmj52"

###############################################################
#### ENTER THE CODE FOR THE ALGORITHM YOU ARE IMPLEMENTING ####
###############################################################

alg_code = "RV"

#####################################################################################################################
#### ENTER THE THRESHOLD: IF YOU ARE IMPLEMENTING VDETECTOR THEN SET THE THRESHOLD AS YOUR CHOICE OF SELF-RADIUS ####
#####################################################################################################################

threshold = 0.1

######################################################
#### ENTER THE INTENDED SIZE OF YOUR DETECTOR SET ####
######################################################

num_detectors = 1000 #500

################################################################
#### DO NOT TOUCH ANYTHING BELOW UNTIL I TELL YOU TO DO SO! ####
####      THIS INCLUDES IMPORTING ADDITIONAL MODULES!       ####
################################################################

import time
import os.path
import random
import math
import sys
    
def get_a_timestamp_for_an_output_file():
    local_time = time.asctime(time.localtime(time.time()))
    timestamp = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
    timestamp = timestamp.replace(" ", "0") 
    return timestamp

def read_points_only(f, point_length, num_points, file):
    list_of_points = []
    count = 0
    error = []
    the_line = f.readline()
    while the_line != "":
        points = the_line.split("[")
        points.pop(0)
        how_many = len(points)
        for i in range(0, how_many):
            if points[i][len(points[i]) - 1] == ",":
                points[i] = points[i][0:len(points[i]) - 2]
            elif points[i][len(points[i]) - 1] == "\n":
                points[i] = points[i][0:len(points[i]) - 3]
            else:
                points[i] = points[i][0:len(points[i]) - 1]
            split_point = points[i].split(",")
            if len(split_point) != point_length:
                error.append("\n*** error: point {0} has the wrong number of components\n".format(i + 1))
                return list_of_points, error
            numeric_point = []
            for j in range(0, point_length):
                numeric_point.append(float(split_point[j]))
            list_of_points.append(numeric_point[:])
            count = count + 1
        the_line = f.readline()
    if count != num_points:
        error.append("\n*** error: there should be {0} points in {1} but there are {2}\n".format(num_points, file, count))
    return list_of_points, error
 
location_of_self = "self_training.txt"

if not os.path.exists(location_of_self):
    print("\n*** error: {0} does not exist\n".format(location_of_self))
    sys.exit()

f = open(location_of_self, "r")

self_or_non_self = f.readline()
if self_or_non_self != "Self\n":
    print("\n*** error: the file " + location_of_self + " is not denoted as a Self-file\n")
    f.close()
    sys.exit()
dim = f.readline()
length_of_dim = len(dim)
dim = dim[len("n = "):length_of_dim - 1]
n = int(dim)
num_points = f.readline()
length_of_num_points = len(num_points)
num_points = num_points[len("number of points = "):length_of_num_points - 1]
Self_num_points = int(num_points)

list_of_points, error = read_points_only(f, n, Self_num_points, location_of_self)
Self = list_of_points[:]

f.close()

if error != []:
    length = len(error)
    for i in range(0, length):
        print(error[i])
    sys.exit()

detectors = []

start_time = time.time()

intended_num_detectors = num_detectors

#########################################################################################
#### YOU SHOULDN'T HAVE TOUCHED *ANYTHING* UP UNTIL NOW APART FROM SUPPLYING VALUES  ####
#### FOR 'username', 'alg_code', 'threshold' and 'num_detectors' AS REQUESTED ABOVE. ####
####                        NOW READ THE FOLLOWING CAREFULLY!                        ####
#########################################################################################

# The training data has now been read with the following reserved variables:
#   - 'n' = the dimension of the points in the training set                 int
#   - 'threshold' = the threshold or self-radius, as appropriate            int or float
#   - 'Self_num_points' = the number of points in the training set
#   - 'Self' = the list of points in the training set.
# These are reserved variables and their names should not be changed.

# You also have the reserved variables
#   - 'user_name', 'alg_code', 'threshold', 'num_detectors', 'intended_num_detectors' and 'start_time'.
# Remember: if 'alg_code' = 'VD' then 'threshold' denotes your chosen self-radius.

# You need to initialize any other parameters (if you are implementing 'Real-valued Negative Selection'
# or 'VDetector') yourself in your code below.

# The list of detectors that your code generates needs to be stored in the variable 'detectors'.
# This is a reserved variable and has just been initialized as empty above. You need to ensure that
# your computed detector set is stored in 'detectors' as a list of points, i.e., as a list of lists-of-
# floats-of-length-'n' for NS and RV and 'n' + 1 for VD (remember: a detector for VD is a point plus
# its individual radius - see Lecture 4).

# FOR ALL OF THE RESERVED VARIABLES BELOW, YOU MUST ENSURE THAT ON TERMINATION THE TYPE
# OF THE RESPECTIVE VARIABLE IS AS SHOWN.

#  - 'n'                int
#  - 'threshold'        int or float

# Finally, if you choose to use numpy then import it below (and don't forget to ensure that 
# variables are of the correct type on termination).

###########################################
#### NOW YOU CAN ENTER YOUR CODE BELOW ####
###########################################

import random
import numpy as np 
#uses euclidean distance 
def calcDistance(origin, point, dimensions):
    "origin is the detector and point is the space away from the detector"
    squared = 0.0
    for i in range(dimensions):
        squared += (origin[1][i] - point[i])**2
    return np.sqrt(squared)

#knearest neighbours is needed and needs to return the set of nearest neighbours

def kNearestNeighbours(k, origin, S, dimensions):
    neighbours= list()
    for i in S:
        dist = calcDistance(origin, i, dimensions)
        neighbours.append((dist,i))
    neighbours.sort()
    return neighbours[:k]#returns the tuple of distances and their neighbours




#need to generate a new detector function

def newDetector(dimensions):
    'returns as tuple in format dimensions, age'
    return [0, [random.random() for i in range(dimensions)]]

def timeDecay(time, decay, initialDecay):
    return initialDecay * math.exp(-time/decay)

#need to create the vector 1 function 
def vectorOneTransform(origin, dimensions, decay, initialDecay, neighbours):
    sumOfNeighboursVector = [0.0]*dimensions
    
    for point in neighbours:
        for i in range(dimensions):
            sumOfNeighboursVector[i] += origin[1][i] - point[1][i]
    return [(origin[1][i] + sumOfNeighboursVector[i] * timeDecay(origin[0], decay, initialDecay)) for i in range(dimensions)]


#need the vector 2 function 
def mewD( origin, detector, dimensions, r):
    dist = calcDistance(origin, detector[1], dimensions)
    return math.exp((-dist**2)/2 * r **2)

def vectorTwoTransform(origin, dimensions, decay, initialDecay,  neighbours, r):
    outputVector = [0]*dimensions
    mewChange = 0
    ageDecay = timeDecay(origin[0], decay, initialDecay)
    for detector in neighbours:
        mewChange = mewD(origin, detector, dimensions, r)
        for i in range(dimensions):
            outputVector[i] += (origin[1][i] - detector[1][i]) * mewChange 
    for i in range(dimensions):
        outputVector[i] = outputVector[i] * ageDecay
    return outputVector
        


def RNS(S, r, N, max_iterations, max_age, initialDecay, decay, k):
    iteration = 1
    dimensions = len(S[0])
    detectors = [newDetector(dimensions) for i in range(N)]#randomly generated list of detectors
    while iteration <= max_iterations:
        for i, D in enumerate(detectors):
            neighbours = kNearestNeighbours(k, D, S, dimensions)
            m = np.median([a[0] for a in neighbours])

            if m < r:
                if D[0] > max_age:
                    #age is too great so replace the old detector
                    detectors[i] = newDetector(dimensions)

                else:
                    D[0] = D[0] + 1
                    D[1] = vectorOneTransform(D, dimensions, decay, initialDecay, neighbours )
                    detectors[i] = D
            else:
                D[0] = 0
                D[1] = vectorTwoTransform(D, dimensions, decay, initialDecay, kNearestNeighbours(k, D, [detector[1] for detector in detectors], dimensions),r)
        iteration = iteration + 1
    return [x[1] for x in detectors]


detectors = RNS(Self, threshold, num_detectors, 10, 3, 0.1, 2, 5)



























#########################################################
#### YOU SHOULD HAVE NOW FINISHED ENTERING YOUR CODE ####
####     DO NOT TOUCH ANYTHING BELOW THIS COMMENT    ####
#########################################################

# At this point in the execution, you should have computed
# - the list 'detectors' of your detector set.

now_time = time.time()
training_time = round(now_time - start_time, 1)

timestamp = get_a_timestamp_for_an_output_file()
detector_set_location = "detector.txt" #_" + timestamp + "

f = open(detector_set_location, "w")

f.write("username = {0}\n".format(username))
f.write("detector set\n")
f.write("algorithm code = {0}\n".format(alg_code))
f.write("dimension = {0}\n".format(n))
if alg_code != "VD":
    f.write("threshold = {0}\n".format(threshold))
else:
    f.write("self-radius = {0}\n".format(threshold))
num_detectors = len(detectors)
f.write("number of detectors = {0} (from an intended number of {1})\n".format(num_detectors, intended_num_detectors))
f.write("training time = {0}\n".format(training_time))
detector_length = n
if alg_code == "VD":
    detector_length = n + 1
for i in range(0, num_detectors):
    f.write("[")
    for j in range(0, detector_length):
        if j != detector_length - 1:
            f.write("{0},".format(detectors[i][j]))
        else:
            f.write("{0}]".format(detectors[i][j]))
            if i == num_detectors - 1:
                f.write("\n")
            else:
                f.write(",\n")
f.close()

print("detector set saved as {0}\n".format(detector_set_location))















    
