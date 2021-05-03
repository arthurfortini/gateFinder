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
    parser = argparse.ArgumentParser(description='Design randomizer script.')
    parser.add_argument('design', help='Design to be randomized', type=str)
    args = parser.parse_args()
    return args

def arg_check():
    if not os.path.isfile(args.design):
        log.error(f"Could not find design file {args.design}")

logger.setup_logging()
loggerTop = logging.getLogger('gatefinder.toplevel')
loggerTop.info('Setting up logger for gateFinder application...')
args = arg_parser()
arg_check()

##  EDIT DESIGN BELOW THIS LINE. EXAMPLES OF CLASS METHOD'S USAGE ARE PROVIDED IN src/examples      ##
##      User Parameters  - those should be always provided      ##

design_name = "AND2"
sim_mu = -0.25
number_of_inputs = 2              # currently gateFinder only support 2 and 3 input gates
ext_potential_vector = None

#   Creation of design
design = Design(args.design)
designDBs = design.getDBDots()

##      Design Definitions        ##

layer_id = 2
def calc_physloc (n, m, l):
    x = n*3.84
    y = m*3.84 + l*2.25
    return (x, y)

# Adding inputs
design.addDBDot(layer_id, (-4,-3, 1), calc_physloc(-4,-3, 1), "#ff00ff00")
design.addDBDot(layer_id, (-4, 2, 1), calc_physloc(-4, 2, 1), "#ff00ff00")

# Adding body DBs
design.addDBDot(layer_id, (-4,-2, 1), calc_physloc(-4,-2, 1), "#ffc8c8c8")
design.addDBDot(layer_id, (-4, 1, 1), calc_physloc(-4, 1, 1), "#ffc8c8c8")
design.addDBDot(layer_id, ( 4, 0, 0), calc_physloc( 4, 0, 0), "#ffc8c8c8")
design.addDBDot(layer_id, ( 6, 0, 0), calc_physloc( 6, 0, 0), "#ffc8c8c8")
design.addDBDot(layer_id, ( 11, 0, 0), calc_physloc( 11, 0, 0), "#ffc8c8c8")

# Adding output
design.addDBDot(layer_id, ( 13, 0, 0), calc_physloc( 13, 0, 0), "#ffff0000")

# Adding perturbers
design.addDBDot(layer_id, ( 18, 0, 0), calc_physloc( 18, 0, 0), "#ff0000ff")
design.addDBDot(layer_id, (-4, -5, 1), calc_physloc(-4, -5, 1), "#ffffff00")
design.addDBDot(layer_id, (-4,  4, 0), calc_physloc(-4,  4, 0), "#ffffff00")


##      PLEASE DO NOT EDIT BELOW THIS LINE. THIS PIECE OF CODE IS DESTINED TO AUTOMATICALLY     ##
##      HANDLE THE MODIFIED VERSION OF DESIGN AND GENERATE THE CORRECT SIMS AND OUTPUTS         ##

design.overwriteDBDots()
designDBs = design.getDBDots()
design.removeDBDot(designDBs[0].dbAttribs)   #removing stub DB
design.overwriteDBDots()

# In this flow, we need to create randomizer and inputPermuter after definition of design DBs
editor = Editor(design)
#inputpermuter = Permuter(design)

sim(design, design_name, number_of_inputs, sim_mu, ext_potential_vector)



