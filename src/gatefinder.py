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

# this imports assumes that a pysimanneal directory containing __init__.py,
# simanneal.py, and the compiled simanneal library (_simanneal.so for Linux or
# _simanneal.pyd for Windows) are present.
# also a src directory containing dbMap.py, inputPermuter.py e randomizer.Py
# should be present.

# sys.path.append("../../src/")    #include source code directory. This should be uncommented in your working directory
import logger
from pysimanneal import simanneal
from dbMap import Design, DBDot
from editor import Editor
from inputPermuter import Permuter
from sim import sim

seed(1)

def create_logger ():
    build_logger = logger.Logger()
    build_logger.set_error()
    return build_logger

def arg_parser():
    parser = argparse.ArgumentParser(description='Design randomizer script.')
    parser.add_argument('design', help='Design to be randomized', type=str)
    args = parser.parse_args()
    return args

def arg_check():
    if not os.path.isfile(args.design):
        log.error(f"Could not find design file {args.design}")

log = create_logger()
args = arg_parser()
arg_check()

##  EDIT DESIGN BELOW THIS LINE. EXAMPLES OF CLASS METHOD'S USAGE ARE PROVIDED IN src/examples      ##
##      User Parameters  - those should be always provided      ##

design_name = "DESIGN_NAME"
sim_mu = -0.28
number_of_inputs = 3              # currently gateFinder only support 2 and 3 input gates
ext_potential_vector = None

#   Creation of design, randomizer and inputPermuter is necessary for design edition and sim automation
design = Design(args.design)
editor = Editor(design)

##      Design Modifications        ##

# This Part is reserved for user's modifications definitions. Please use classes methods to
# modify DBs here.






##      PLEASE DO NOT EDIT BELOW THIS LINE. THIS PIECE OF CODE IS DESTINED TO AUTOMATICALLY     ##
##      HANDLE THE MODIFIED VERSION OF DESIGN AND GENERATE THE CORRECT SIMS AND OUTPUTS         ##
sim(design, design_name, number_of_inputs, sim_mu, ext_potential_vector)