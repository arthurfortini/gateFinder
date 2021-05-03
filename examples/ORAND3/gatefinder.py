#############################################################################
#                               UFMG - 2021                                 #
#                            SiDB GateFinder:                               #
#      Framework to facilitate edition and testing of SiDB circuits         #
#                                                                           #
# Authors: Arthur Fortini and Gustavo Guedes                                #
# File: gatefinder.py                                                       #
# Description: Top level file to address user modifications in a base       #
#              SiDB file and facilitate simulation and anaylis of results.  #
#              Please note that some parts should be edited by user and     #
#              some parts are an automated flow that should not be modified #
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

sys.path.append("../../src/")    #include source code directory. This should be uncommented in your working directory
import logger
import logging
from dbMap import Design, DBDot
from editor import Editor
from sim import sim

seed(1)

def arg_parser():
    parser = argparse.ArgumentParser(description='GateFinder Framework top level script.')
    parser.add_argument('design', help='Design to be modified or simulated', type=str)
    args = parser.parse_args()
    return args

def arg_check():
    if not os.path.isfile(args.design):
        loggerTop.error(f"Could not find design file {args.design}")

logger.setup_logging()
loggerTop = logging.getLogger('gatefinder.toplevel')
loggerTop.info('Setting up logger for gateFinder application...')
args = arg_parser()
arg_check()

##  EDIT DESIGN BELOW THIS LINE. EXAMPLES OF CLASS METHOD'S USAGE ARE PROVIDED IN src/examples      ##
##      User Parameters  - those should be always provided      ##

design_name = "ORAND3"
sim_mu = -0.28
number_of_inputs = 3              # currently gateFinder only support 2 and 3 input gates
ext_potential_vector = None

#   Creation of design, randomizer and inputPermuter is necessary for design edition and sim automation
design = Design(args.design)
editor = Editor(design)

##      Design Modifications        ##

editor.modifyInputAngle(editor.std[0], editor.inputs[0], editor.inPerturber[0], 120)
editor.modifyInputAngle(editor.std[1], editor.inputs[1], editor.inPerturber[1], -180)
editor.modifyInputAngle(editor.std[2], editor.inputs[2], editor.inPerturber[2], -120)

editor.modifySpecificDB(editor.inPerturber[0], 3, "y")
editor.modifySpecificDB(editor.inPerturber[0], 1, "x")
editor.modifySpecificDB(editor.inPerturber[2], -3, "y")
editor.modifySpecificDB(editor.inPerturber[2], 1, "x")

(n,m,l) = editor.inPerturber[0].latcoord
editor.changecoord(editor.inPerturber[0], n, m, 0)
(n,m,l) = editor.inPerturber[2].latcoord
editor.changecoord(editor.inPerturber[2], n, m, 1)

editor.modifySpecificDB(editor.inputs[1], 2, "x")
editor.modifySpecificDB(editor.inPerturber[1], 2, "x")
editor.modifySpecificDB(editor.std[1], 2, "x")
editor.modifySpecificDB(editor.outPerturber[0], -1, "x")


##      PLEASE DO NOT EDIT BELOW THIS LINE. THIS PIECE OF CODE IS DESTINED TO AUTOMATICALLY     ##
##      HANDLE THE MODIFIED VERSION OF DESIGN AND GENERATE THE CORRECT SIMS AND OUTPUTS         ##
sim(design, design_name, number_of_inputs, sim_mu, ext_potential_vector)