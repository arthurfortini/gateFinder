#############################################################################
#                               UFMG - 2021                                 #
#                        SiDB RobustnessAnalysis:                           #
#      Algorithm to perform robustness analysis in SiDB circuits            #
#                                                                           #
# Authors: Arthur Fortini                                                   #
# File:                                                                     #
# Description: Example of how to use the defined errorAnalysis class        #
#               methods to create an errorAnalysis script                   #
#                                                                           #
#############################################################################

import argparse
import os
from random import seed
import sys

# this imports assumes that a pysimanneal directory containing __init__.py,
# simanneal.py, and the compiled simanneal library (_simanneal.so for Linux or
# _simanneal.pyd for Windows) are present.
# also a src directory containing dbMap.py, inputPermuter.py e randomizer.Py
# should be present.

sys.path.append("../../../gateFinder/src/")    #include source code directory.
import logger
import logging
from dbMap import Design, DBDot
from editor import Editor
from errorSimulator import errorSimulator
from sim import sim
from errorSimulator import errorSimulator

seed(1)

def arg_parser():
    parser = argparse.ArgumentParser(description='Robustness Analysis top level script.')
    parser.add_argument('design', help='Design to be modified or simulated', type=str)
    args = parser.parse_args()
    return args

def arg_check():
    if not os.path.isfile(args.design):
        loggerTop.error(f"Could not find design file {args.design}")

logger.setup_logging()
loggerTop = logging.getLogger('gatefinder.errorAnalysis')
loggerTop.info('Setting up logger for errorAnalysis application...')
args = arg_parser()
arg_check()

##      User Parameters  - those should be always provided      ##
design_name = "OR2T"
sim_mu = -0.25
number_of_inputs = 2                # currently gateFinder only support 2 and 3 input gates
ext_potential_vector = None
errorInsertionType = "sequential"   # can be sequential or assignable
iterations = 10                     # number of interations of the whole error analysis process

# Golden Design read and simulation
design = Design(args.design)
errorSim = errorSimulator(design)

# Performing robustness analysis flow
goldenResults = errorSim.runGoldenSim(sim_mu, ext_potential_vector)

sequentialResults = errorSim.runSequentialModel(sim_mu, ext_potential_vector, iterations)

# First Analysis: Binary check of the truth tables - if identical, PASS, if not, FAIL
totalSims = len(sequentialResults)
totalPass = 0
totalError = 0
totalemptyresults = 0

for result in sequentialResults:
    if (result == goldenResults):
        totalPass = totalPass + 1
    else:
        if(not result):
            totalemptyresults = totalemptyresults + 1
        totalError = totalError + 1

robustness = (totalPass/totalSims)*100

# Second Analysis: Each Permutation is a case of pass and fail. Gives us a general perspective of the robustness of the gate. A more close look on robustness
#   Alternative results analysis -> compare element per element and each input permutation is a case of pass and fail.

generalPermutationPass = 0
generalPermutationFail = 0
generalAccuracy = 0
iterationPermutationPass = 0
iterationPermutationFail = 0
iterationAccuracy = 0
index = 0

fineAnalysis = []
errorIndexAbove70Percent = []
errorIndexBelow70Percent = []

for result in sequentialResults:
    for i in range(len(result)):
        l1 = result[i]
        l2 = goldenResults[i]
        if(l1 == l2):
            generalPermutationPass = generalPermutationPass + 1
            iterationPermutationPass = iterationPermutationPass + 1
        else:
            generalPermutationFail = generalPermutationFail + 1
            iterationPermutationFail = iterationPermutationFail + 1

    iterationAccuracy = (iterationPermutationPass/4)*100
    fineAnalysis.append([index, iterationAccuracy])
    iterationPermutationPass = 0
    iterationPermutationFail = 0
    index = index + 1

generalAccuracy = (generalPermutationPass/(4*totalSims))*100

for element in fineAnalysis:
    if element[1] > 75:             # checks if this errorInsertion only failed in one permutation. If so, appends it to the list.
        errorIndexAbove70Percent.append(element[0])
    else:
        errorIndexBelow70Percent.append(element[0])


# Logging results - Primitive version
# TODO: Add logging structuration -> to write the file (put it inside log module and just call the function here).

# print("Process Finished.\n"
#       "\tTotal number of iterations in method = " + str(iterations) + "\n"
#       "\tTotal error sims performed: " + str(totalSims) + "\n"
#       "\tTotal Passed tests: " + str(totalPass) + "\n"
#       "\tTotal Failed Tests: " + str(totalError) + "\n"
#       "\tAccuracy = " + str(robustness) + "%\n")

loggerTop.info("Process Finished.\n"
      "------------- Truth Table Based Analysis -------------\n"
      "\tTotal number of iterations in method = " + str(iterations) + "\n"
      "\tTotal error sims performed: " + str(totalSims) + "\n"
      "\tTotal Passed tests: " + str(totalPass) + "\n"
      "\tTotal Failed Tests: " + str(totalError) + "\n"
      "\tAccuracy = " + str(robustness) + "%\n"
      "------------- Finer Analysis -------------\n"
      "\tTotal Passed tests: " + str(generalPermutationPass) + "\n"  
      "\tTotal Failed tests: " + str(generalPermutationFail) + "\n" 
      "\tGeneral Accuracy = " + str(generalAccuracy) + "\n"
      "\tTests That had over 70% PASS: " + str(errorIndexAbove70Percent) + "\n"
      "\tTests that had below 70% PASS: " + str(errorIndexBelow70Percent) + "\n")


# editor.modifySpecificDB(editor.std[0], -1, "x")
# sim(design, design_name, number_of_inputs, sim_mu, ext_potential_vector)