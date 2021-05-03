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

# sys.path.append("../../src/")    #include source code directory. This should be uncommented in your working directory
import logger
import logging
from dbMap import Design, DBDot
from editor import Editor
from sim import sim

seed(1)

def arg_parser():
    parser = argparse.ArgumentParser(description='Design randomizer script.')
    parser.add_argument('design', help='Design to be randomized', type=str)
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

design_name = "DESIGN_NAME"
sim_mu = -0.25
number_of_inputs = 2              # currently gateFinder only support 2 and 3 input gates
ext_potential_vector = None

#   Creation of design
design = Design(args.design)
designDBs = design.getDBDots()

##      Design Definitions        ##

    # Please insert your DBs definitions here. Example of usage of Design class methods are provided
    # in examples/AND2/gatefinder.py





##      PLEASE DO NOT EDIT BELOW THIS LINE. THIS PIECE OF CODE IS DESTINED TO AUTOMATICALLY     ##
##      HANDLE THE MODIFIED VERSION OF DESIGN AND GENERATE THE CORRECT SIMS AND OUTPUTS         ##

design.overwriteDBDots()
designDBs = design.getDBDots()
design.removeDBDot(designDBs[0].dbAttribs)   #removing stub DB
design.overwriteDBDots()

# In this flow, we need to create randomizer after definition of design DBs

editor = Editor(design)

sim(design, design_name, number_of_inputs, sim_mu, ext_potential_vector)



