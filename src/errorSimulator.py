import argparse
import os
from random import seed
import random
import numpy as np
import sys
import re
import copy

# this imports assumes that a pysimanneal directory containing __init__.py,
# simanneal.py, and the compiled simanneal library (_simanneal.so for Linux or
# _simanneal.pyd for Windows) are present.
# also a src directory containing dbMap.py, inputPermuter.py e randomizer.Py
# should be present.

# sys.path.append("../../../../gateFinder/src/")    #include source code directory.
import logger
import logging
from pysimanneal import simanneal
from dbMap import Design, DBDot
from editor import Editor
from inputPermuter import Permuter


module_logger = logging.getLogger('gatefinder.errorSimulation')

class errorSimulator ():
    def __init__(self, designObj) -> None:
        self.logger = logging.getLogger('gatefinder.errorSimulator')
        self.logger.info('creating an instance of errorSimulator')
        self.goldenDesign = designObj
        self.goldenResults = []
        self.NumErrorInserted = 0


    def runSimAnneal(self, design, sim_mu, num_instances, ext_potential_vector=None):
        editor = Editor(design)
        db_pos = []

        for i, DBDot in enumerate(editor.inputs):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.std):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.inPerturber):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.outPerturber):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.outputs):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        sp = simanneal.SimParams()
        sp.mu = sim_mu
        sp.set_db_locs(db_pos)
        # increase instance count
        sp.num_instances = num_instances
        if (ext_potential_vector != None):
            sp.set_v_ext(ext_potential_vector)
            # sp.set_v_ext(np.zeros(len(sp.db_locs)))
        sa = simanneal.SimAnneal(sp)
        sa.invokeSimAnneal()
        results = sa.suggested_gs_results()
        return results

    def rungoldenSimAnneal(self, sim_dir, sim_mu, ext_potential_vector=None):
        directory = "sims"
        path = os.path.join(directory, sim_dir)
        os.chdir(path)
        design = Design(sim_dir + ".xml")
        editor = Editor(design)
        db_pos = []

        for i, DBDot in enumerate(editor.inputs):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.std):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.inPerturber):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.outPerturber):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        for i, DBDot in enumerate(editor.outputs):
            (n, m, l) = DBDot.latcoord
            db_pos.append([int(n), int(m), int(l)])

        sp = simanneal.SimParams()
        sp.mu = sim_mu
        sp.set_db_locs(db_pos)
        # increase instance count
        sp.num_instances=100
        if (ext_potential_vector != None):
            sp.set_v_ext(ext_potential_vector)
            # sp.set_v_ext(np.zeros(len(sp.db_locs)))
        sa = simanneal.SimAnneal(sp)
        sa.invokeSimAnneal()
        results = sa.suggested_gs_results()
        return results


    def runExhaustiveGS(self):
        return 1


    def runGoldenSim(self, sim_mu, ext_potential_vector=None):
        self.logger.info('ErrorAnalysis:    Running Golden Simulation...')
        resultsBuffer = []
        num_inputs = 0
        design_name = "golden"
        goldenCopy = copy.deepcopy(self.goldenDesign)
        editor = Editor(goldenCopy)
        inputpermuter = Permuter(goldenCopy)
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, design_name)
        os.mkdir(path)
        os.chdir(path)

        if (len(editor.inputs) == 2):
            num_inputs = 2
            inputpermuter.permute2inputs(design_name)
        elif (len(editor.inputs) == 3):
            num_inputs = 3
            inputpermuter.permute3inputs(design_name)
        else:
            self.logger.error('Number of inputs (' + str(len(editor.inputs)) + ') not supported!')

        if (num_inputs == 2):
            counter = 0
            simdir = ""

            for i in range(4):
                if (counter == 0):
                    simdir = design_name + "_00"
                elif (counter == 1):
                    simdir = design_name + "_01"
                elif (counter == 2):
                    simdir = design_name + "_10"
                elif (counter == 3):
                    simdir = design_name + "_11"

                if (ext_potential_vector != None):
                    result = self.rungoldenSimAnneal(simdir, sim_mu, ext_potential_vector)
                else:
                    result = self.rungoldenSimAnneal(simdir, sim_mu)

                outputStr = str(result[0])
                find_output_regex = r"[-+\s][0-1](?=])"
                outputRes = re.search(find_output_regex, outputStr).group(0)

                resultsBuffer.append(outputRes)

                counter = counter + 1
                os.chdir(path)

        elif (num_inputs == 3):
            counter = 0
            simdir = ""

            for i in range(8):
                if (counter == 0):
                    simdir = design_name + "_000"
                elif (counter == 1):
                    simdir = design_name + "_001"
                elif (counter == 2):
                    simdir = design_name + "_010"
                elif (counter == 3):
                    simdir = design_name + "_011"
                elif (counter == 4):
                    simdir = design_name + "_100"
                elif (counter == 5):
                    simdir = design_name + "_101"
                elif (counter == 6):
                    simdir = design_name + "_110"
                elif (counter == 7):
                    simdir = design_name + "_111"

                if (ext_potential_vector != None):
                    result = self.rungoldenSimAnneal(simdir, sim_mu, ext_potential_vector)
                else:
                    result = self.rungoldenSimAnneal(simdir, sim_mu)

                outputStr = str(result[0])
                find_output_regex = r"[-+\s][0-1](?=])"
                outputRes = re.search(find_output_regex, outputStr).group(0)

                resultsBuffer.append(outputRes)

                counter = counter + 1
                os.chdir(path)
        else:
            self.logger.error('Number of inputs (' + str(len(editor.inputs)) + ') not supported!')

        print("Golden Results vector is: " + str(resultsBuffer))
        self.logger.debug("ErrorSim:    Golden Results Vector: " + str(resultsBuffer))
        os.chdir(parent_dir)
        self.goldenResults = resultsBuffer
        self.logger.debug('ErrorSim:    Running Golden Simulation finished, final resultsBuffer is %s', str(resultsBuffer))
        self.logger.info('ErrorSim:    Running Golden Simulation: FINISHED')
        return resultsBuffer

    def simulateIndependentModif(self, editor, design, sim_mu, exPotVec, DBDot, type, distance):
        # goldenCopy = self.goldenDesign
        # editor = Editor(goldenCopy)
        distance_bak = -1 * distance
        resultsBuffer = []
        simInstances_num = 100
        find_output_regex = r"[-+\s][0-1](?=])"

        # ## RESOLVING ERROR TO BE INSERTED AND CREATING MODIFIED DESIGN ## #
        if (type == "x"):
            editor.modifySpecificDB(DBDot, distance, "x")
            design.overwriteDBDots()
            design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
            editor.modifySpecificDB(DBDot, distance_bak, "x")
            design.overwriteDBDots()
        elif (type == "y"):
            editor.modifySpecificDB(DBDot, distance, "y")
            design.overwriteDBDots()
            design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
            editor.modifySpecificDB(DBDot, distance_bak, "y")
            design.overwriteDBDots()
        elif (type == "yGrid"):
            (n, m, l) = DBDot.latcoord
            editor.changecoord(DBDot, int(n), int(m), int(distance))
            design.overwriteDBDots()
            design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
            if (distance == 0):
                editor.changecoord(DBDot, int(n), int(m), 1)
            if (distance == 1):
                editor.changecoord(DBDot, int(n), int(m), 0)
            design.overwriteDBDots()
        else:
            self.logger.error('ErrorSim:    simulateIndepModif: type argument invalid.')

        # ## PERMUTING INPUTS AND SIMULATING MODIFIED DESIGN ## #

        localDesign = Design("Error_" + str(self.NumErrorInserted) + ".sqd")
        localEditor = Editor(localDesign)
        numInputs = len(localEditor.inPerturber)      ## It decides how many inputs are there because i can end up deleting the green dbDot in a inputPair.

        # 1st inputperturber data
        input1_id = localEditor.inPerturber[0].layer_id
        input1_latcoord = localEditor.inPerturber[0].latcoord
        input1_physloc = localEditor.inPerturber[0].physloc
        input1_color = localEditor.inPerturber[0].color

        # 2nd inputperturber data
        input2_id = localEditor.inPerturber[1].layer_id
        input2_latcoord = localEditor.inPerturber[1].latcoord
        input2_physloc = localEditor.inPerturber[1].physloc
        input2_color = localEditor.inPerturber[1].color

        if (numInputs == 2):
            counter = 0
            for i in range(4):
                if (counter == 1):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)
                elif (counter == 2):
                    localDesign.removeDBDot(localEditor.inPerturber[0].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                elif (counter == 3):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)

                results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                while ((not results) and (simInstances_num <= 400)):
                    simInstances_num = simInstances_num + 50
                    results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                if (not results):
                    results = "NaN"
                    resultsBuffer.append(results)
                else:
                    outputStr = str(results[0])
                    outputRes = re.search(find_output_regex, outputStr).group(0)
                    resultsBuffer.append(outputRes)
                counter = counter+1

        elif (numInputs == 3):
            counter = 0
            # 3rd inputperturber data
            input3_id = localEditor.inPerturber[2].layer_id
            input3_latcoord = localEditor.inPerturber[2].latcoord
            input3_physloc = localEditor.inPerturber[2].physloc
            input3_color = localEditor.inPerturber[2].color

            for i in range(8):
                if (counter == 1):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)
                elif (counter == 2):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                elif (counter == 3):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)
                elif (counter == 4):
                    localDesign.removeDBDot(localEditor.inPerturber[0].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                    localDesign.addDBDot(input3_id, input3_latcoord, input3_physloc, input3_color)
                elif (counter == 5):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)
                elif (counter == 6):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                elif (counter == 7):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)

                results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                while ((not results) and (simInstances_num <= 400)):
                    simInstances_num = simInstances_num + 50
                    results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                if (not results):
                    results = "NaN"
                    resultsBuffer.append(results)
                else:
                    outputStr = str(results[0])
                    outputRes = re.search(find_output_regex, outputStr).group(0)
                    resultsBuffer.append(outputRes)
                counter = counter + 1
        else:
            self.logger.error('ErrorSim:    simulateIndepModif: number of inputs unsupported.')

        self.NumErrorInserted = self.NumErrorInserted + 1
        resultsBuffer.reverse()
        return resultsBuffer

    def simulatePairModif(self, editor, design, sim_mu, exPotVec, dbPair, internalExtOrAdd, axis_type, distance=0, coordenates=(0,0,0), chosenDB=0, deleteDB=0):
        distance_bak = -1 * distance
        resultsBuffer = []
        simInstances_num = 100
        find_output_regex = r"[-+\s][0-1](?=])"

        # ## RESOLVING ERROR TO BE INSERTED AND CREATING MODIFIED DESIGN ## #
        if(internalExtOrAdd == "external"):
            self.logger.debug('ErrorSim:    simulatePairModif: entered external error sim. Error number = %s , type of error is: %s', str(self.NumErrorInserted), str(axis_type))
            if (axis_type == "x"):
                editor.modifySpecificDB(dbPair[0], distance, "x")
                editor.modifySpecificDB(dbPair[1], distance, "x")
                design.overwriteDBDots()
                design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                editor.modifySpecificDB(dbPair[0], distance_bak, "x")
                editor.modifySpecificDB(dbPair[1], distance_bak, "x")
                design.overwriteDBDots()
            elif (axis_type == "y"):
                editor.modifySpecificDB(dbPair[0], distance, "y")
                editor.modifySpecificDB(dbPair[1], distance, "y")
                design.overwriteDBDots()
                design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                editor.modifySpecificDB(dbPair[0], distance_bak, "y")
                editor.modifySpecificDB(dbPair[1], distance_bak, "y")
                design.overwriteDBDots()
            elif (axis_type == "yGrid"):
                (n0, m0, l0) = copy.deepcopy(dbPair[0].latcoord)
                (n1, m1, l1) = copy.deepcopy(dbPair[1].latcoord)
                if (int(l0) == 1):
                    editor.changecoord(dbPair[0], int(n0), int(m0), 0)
                else:
                    editor.changecoord(dbPair[0], int(n0), int(m0), 1)
                if (int(l1) == 1):
                    editor.changecoord(dbPair[1], int(n1), int(m1), 0)
                else:
                    editor.changecoord(dbPair[1], int(n1), int(m1), 1)
                design.overwriteDBDots()
                design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                editor.changecoord(dbPair[0], int(n0), int(m0), int(l0))
                editor.changecoord(dbPair[1], int(n1), int(m1), int(l1))
                # if (distance == 0):
                #     editor.changecoord(dbPair[0], n0, m0, 1)
                #     editor.changecoord(dbPair[1], n1, m1, 1)
                # if (distance == 1):
                #     editor.changecoord(dbPair[0], n0, m0, 0)
                #     editor.changecoord(dbPair[1], n1, m1, 0)
                design.overwriteDBDots()
            else:
                self.logger.error('ErrorSim:    simulatePairModif: axis_type argument invalid.')

        elif(internalExtOrAdd == "internal"):
            self.logger.debug('ErrorSim:    simulatePairModif: entered internal error sim. Error number = %s , type of error is: %s',
                                    str(self.NumErrorInserted), str(axis_type))
            if (chosenDB == 0):
                chosendb = dbPair[0]
            else:
                chosendb = dbPair[1]

            if (deleteDB):
                self.logger.debug('ErrorSim:    simulatePairModif: Called for deleteDB. Error number = %s , chosendb is: %s',
                                    str(self.NumErrorInserted), str(chosenDB))
                chosendb_id = chosendb.layer_id
                chosendb_latcoord = chosendb.latcoord
                chosendb_physloc = chosendb.physloc
                chosendb_color = chosendb.color

                if (chosendb_color == "#ffff0000"):
                    self.logger.error('ErrorSim:    simulatePairModif: trying to remove OUTPUT dbDot. Bypassing...')
                    design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                else:
                    self.logger.debug('ErrorSim:    simulatePairModif: Not bypassing deletion for verif purposes...')
                    design.removeDBDot(chosendb.dbAttribs)
                    design.overwriteDBDots()
                    design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                    design.addDBDot(chosendb_id, chosendb_latcoord, chosendb_physloc, chosendb_color)
                    design.overwriteDBDots()
            else:
                if (axis_type == "x"):
                    editor.modifySpecificDB(chosendb, distance, "x")
                    design.overwriteDBDots()
                    design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                    editor.modifySpecificDB(chosendb, distance_bak, "x")
                    design.overwriteDBDots()
                elif (axis_type == "y"):
                    editor.modifySpecificDB(chosendb, distance, "y")
                    design.overwriteDBDots()
                    design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                    editor.modifySpecificDB(chosendb, distance_bak, "y")
                    design.overwriteDBDots()
                elif (axis_type == "yGrid"):
                    (n, m, l) = chosendb.latcoord
                    editor.changecoord(chosendb, int(n), int(m), int(distance))
                    design.overwriteDBDots()
                    design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
                    if (distance == 0):
                        editor.changecoord(chosendb, int(n), int(m), 1)
                    if (distance == 1):
                        editor.changecoord(chosendb, int(n), int(m), 0)
                    design.overwriteDBDots()
                else:
                    self.logger.error('ErrorSim:    simulatePairModif: type argument invalid.')

        elif(internalExtOrAdd == "add"):
            self.logger.debug('ErrorSim:    simulatePairModif: entered add error sim. Error number = %s', str(self.NumErrorInserted))
            auxDBdot = copy.deepcopy(dbPair[0])
            (n, m, l) = coordenates
            x = int(n) * 3.84
            y = int(m) * 3.84 + int(l) * 2.25

            auxDBdot.changeLatcoord(n,m,l)
            auxDBdot.changePhysloc(x,y)
            design.addDBDot(dbPair[0].layer_id, (n, m, l), (x, y), "#ffc8c8c8")   ## adding this DB as std type
            design.overwriteDBDots()
            design.save("Error_" + str(self.NumErrorInserted) + ".sqd")
            design.removeMostRecentDBDot()   ## removing most recently added dbDot
            design.overwriteDBDots()

        else:
            self.logger.error('ErrorSim:    simulatePairModif: internalExtOrAdd argument invalid.')

        # ## PERMUTING INPUTS AND SIMULATING MODIFIED DESIGN ## #

        localDesign = Design("Error_" + str(self.NumErrorInserted) + ".sqd")
        localEditor = Editor(localDesign)
        numInputs = len(localEditor.inPerturber)      ## It decides how many inputs are there because i can end up deleting the green dbDot in a inputPair.

        # 1st inputperturber data
        input1_id = localEditor.inPerturber[0].layer_id
        input1_latcoord = localEditor.inPerturber[0].latcoord
        input1_physloc = localEditor.inPerturber[0].physloc
        input1_color = localEditor.inPerturber[0].color

        # 2nd inputperturber data
        input2_id = localEditor.inPerturber[1].layer_id
        input2_latcoord = localEditor.inPerturber[1].latcoord
        input2_physloc = localEditor.inPerturber[1].physloc
        input2_color = localEditor.inPerturber[1].color

        if (numInputs == 2):
            counter = 0
            for i in range(4):
                if (counter == 1):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)
                elif (counter == 2):
                    localDesign.removeDBDot(localEditor.inPerturber[0].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                elif (counter == 3):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)

                results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                while ((not results) and (simInstances_num <= 400)):
                    simInstances_num = simInstances_num + 50
                    results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                if (not results):
                    results = "NaN"
                    resultsBuffer.append(results)
                else:
                    outputStr = str(results[0])
                    outputRes = re.search(find_output_regex, outputStr).group(0)
                    resultsBuffer.append(outputRes)
                counter = counter+1

        elif (numInputs == 3):
            counter = 0
            # 3rd inputperturber data
            input3_id = localEditor.inPerturber[2].layer_id
            input3_latcoord = localEditor.inPerturber[2].latcoord
            input3_physloc = localEditor.inPerturber[2].physloc
            input3_color = localEditor.inPerturber[2].color

            for i in range(8):
                if (counter == 1):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)
                elif (counter == 2):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                elif (counter == 3):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)
                elif (counter == 4):
                    localDesign.removeDBDot(localEditor.inPerturber[0].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                    localDesign.addDBDot(input3_id, input3_latcoord, input3_physloc, input3_color)
                elif (counter == 5):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)
                elif (counter == 6):
                    localDesign.removeDBDot(localEditor.inPerturber[1].dbAttribs)
                    localDesign.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
                elif (counter == 7):
                    localDesign.removeDBDot(localEditor.inPerturber[2].dbAttribs)

                results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                while ((not results) and (simInstances_num <= 400)):
                    simInstances_num = simInstances_num + 50
                    results = self.runSimAnneal(localDesign, sim_mu, simInstances_num, exPotVec)
                if (not results):
                    results = "NaN"
                    resultsBuffer.append(results)
                else:
                    outputStr = str(results[0])
                    outputRes = re.search(find_output_regex, outputStr).group(0)
                    resultsBuffer.append(outputRes)
                counter = counter + 1
        else:
            self.logger.error('ErrorSim:    simulatePairModif: number of inputs unsupported.')

        self.NumErrorInserted = self.NumErrorInserted + 1
        resultsBuffer.reverse()
        return resultsBuffer


# TODO : Add support for isolated DBs also
    def runSequentialModel(self, sim_mu, extPotVec, iterations):
        self.logger.info('ErrorAnalysis:    Running Sequential Model Error Insertion Simulation...')
        parent_dir = os.getcwd()
        resultsBuffer = []
        simresults = []
        num_inputs = 0
        goldenCopy = copy.deepcopy(self.goldenDesign)
        editor = Editor(goldenCopy)
        path = os.path.join(parent_dir, "sequentialModel")
        os.mkdir(path)
        os.chdir(path)

        ## Define number of inputs:
        if (len(editor.inputs) == 2):
            num_inputs = 2
        elif (len(editor.inputs) == 3):
            num_inputs = 3

        ## Classificar os DBs do design
        ## Obs: Atualmente a classificação dos pares de DBs é altamente dependente do índice no .xml. Isso quer dizer que a ordem que colocamos
        ##      os Dbs no design inicial lá no CAD importa.

        # input_perturbers = [editor.inPerturber[0].id, editor.inPerturber[1].id]
        # if(num_inputs == 3):
        #     input_perturbers.append(editor.inPerturber[2].id)
        output_perturber = editor.outPerturber
        self.logger.debug('ErrorAnalysis:    output_perturber list is: %s', str(output_perturber))
        input_perturbers = editor.inPerturber
        self.logger.debug('ErrorAnalysis:    input_perturbers list is: %s', str(input_perturbers))

        # indep_db =  AINDA POR FAZER

        # dbPairsList = []  # this list is going to contain ID info about the DBpairs
        # # append input pairs
        # dbPairsList.append([editor.inputs[0].id, editor.std[0].id])
        # dbPairsList.append([editor.inputs[1].id, editor.std[1].id])
        # if(num_inputs == 3):
        #     dbPairsList.append([editor.inputs[2].id, editor.std[2].id])
        # # append output pairs
        # last_db_index = len(editor.std) - 1
        # dbPairsList.append([editor.outputs[0], editor.std[last_db_index]])
        # # append standard db pairs
        # if (num_inputs == 2):
        #     for i in range(2, len(editor.std), 2):
        #         dbPairsList.append([editor.std[i], editor.std[i+1]])
        # if (num_inputs == 3):
        #     for i in range(3, len(editor.std), 2):
        #         dbPairsList.append([editor.std[i], editor.std[i+1]])

        dbPairsList = []  # this list is going the DBpairs identified
        stdListLength = len(editor.std)
        self.logger.debug('ErrorAnalysis:    std dbs in this design are: %s', str(editor.std))
        self.logger.debug('ErrorAnalysis:    std dbs list lenght is: %s', str(stdListLength))
        # append input pairs
        dbPairsList.append([editor.inputs[0], editor.std[0]])
        dbPairsList.append([editor.inputs[1], editor.std[1]])
        if(num_inputs == 3):
            dbPairsList.append([editor.inputs[2], editor.std[2]])
        # append output pairs
        last_db_index = len(editor.std) - 1     # This returns correct index
        dbPairsList.append([editor.outputs[0], editor.std[last_db_index]])
        self.logger.debug('ErrorAnalysis:    dbPair List after compiling output and input pairs: %s', str(dbPairsList))

        aretherestddbsremaining = len(editor.std) - (num_inputs+1)
        self.logger.debug('ErrorAnalysis:    dbs remaining to be allocated: %s', str(aretherestddbsremaining))
        if ((editor.std) and (aretherestddbsremaining >= 1)):   # checks if the entire editor.std list has been already alocated in inputs/output pairs
            # append standard db pairs
            if (num_inputs == 2):
                for i in range(2, len(editor.std), 2):
                    if(not i == stdListLength-1):       # handles the last db and do not append it since the last db in std list is always from the output pair
                        dbPairsList.append([editor.std[i], editor.std[i+1]])
            if (num_inputs == 3):
                for i in range(3, len(editor.std), 2):
                    if(not i == stdListLength-1):
                        dbPairsList.append([editor.std[i], editor.std[i+1]])
        self.logger.debug('ErrorAnalysis:    dbPair List is: %s', str(dbPairsList))


        ## Single DB error insertion -> inputs and std independent dbs
        ## Important to remember: np.random.randint(a,b) returns random integer numbers in the open interval [a,b[ !!
            ## Inputs
        for DBDot in input_perturbers:
            for i in range(iterations):
                if(np.random.randint(0,2)): # if 1 -> error in x axis if 0 -> error in y axis
                    if(np.random.randint(0,2)):   # if 1 -> dislocation to the right, if 0 -> dislocation to the left
                        dislocation = np.random.randint(1,4)
                        simresults = self.simulateIndependentModif(editor, goldenCopy, sim_mu, extPotVec, DBDot, "x", dislocation)
                    else:
                        dislocation = -1 * np.random.randint(1,4)
                        simresults = self.simulateIndependentModif(editor, goldenCopy, sim_mu, extPotVec, DBDot, "x", dislocation)
                else:
                    if(np.random.randint(0,2)):  # if 1 -> across lines. if 0 -> same grid
                        if(np.random.randint(0,2)):  # if 1 -> dislocation upwards, if 0 -> dislocation downwards
                            dislocation = -1 * np.random.randint(1,3)
                            simresults = self.simulateIndependentModif(editor, goldenCopy, sim_mu, extPotVec, DBDot, "y", dislocation)
                        else:
                            dislocation = np.random.randint(1, 3)
                            simresults = self.simulateIndependentModif(editor, goldenCopy, sim_mu, extPotVec, DBDot, "y", dislocation)
                    else:
                        (n, m, l) = DBDot.latcoord
                        l_coord = int(l)
                        if (l_coord == 1):
                            simresults = self.simulateIndependentModif(editor, goldenCopy, sim_mu, extPotVec, DBDot, "yGrid", 0)
                        elif (l_coord == 0):
                            simresults = self.simulateIndependentModif(editor, goldenCopy, sim_mu, extPotVec, DBDot, "yGrid", 1)
                        else:
                            self.logger.error('ErrorAnalysis:    ERROR:  insertErrorOnInputs not able to read DBDot latcoord properly...')
                resultsBuffer.append(simresults)

        self.logger.debug('ErrorAnalysis:    Finished error insertion in imputs. Number of iterations is: %s and current resultsBuffer is: %s', str(iterations), str(resultsBuffer))
                 # decidir eixo x ou y
                    # se for x:
                        # decidir se vai ser direita ou esquerda
                            # decidir a quantidade do deslocamento. 1 2 ou 3
                    # se for y:
                        # decidir se vai ser na mesma linha ou across lines
                            # se for across lines, decidir se e pra cima ou pra cima ou baixo.
                                # decidir a quantidade do deslocamento. 1 ou 2
                        # se for na mesma linha, checar o l da latcooord. Se for 0, mudar pra 1, se for 1, mudar pra zero.

                # appendar o buffer de resultados

            ## Outputs - adaptar pra ser pros dbs independentes. Ja que na vou inserir erros nas outputs.
        # for DBDot in output_perturber:
        #    for i in range(iterations):
                # decidir eixo x ou y
                    # se for y:
                        # decidir se vai ser na mesma linha ou across lines
                            # se for across lines, decidir se e pra cima ou pra cima ou baixo.
                                # decidir a quantidade do deslocamento. 1 ou 2
                        # se for na mesma linha, checar o l da latcooord. Se for 0, mudar pra 1, se for 1, mudar pra zero.
                    # se for x:
                        # decidir se vai ser direita ou esquerda
                            # decidir a quantidade do deslocamento. 1 2 ou 3
                # appendar o buffer de resultados

        ## Insertion of errors in DBPairs  -- nao importa qual
        for DBPair in dbPairsList:
            for i in range(iterations):
                errortype = np.random.randint(0,3)

                if (errortype == 1):  # if 1 -> internal error, if 0 -> grouped error, if 2 -> adding extra DB error
                    if (np.random.randint(0,2)):  # if 1 -> error in db[1], if 0 -> error in db[0]
                        chosendb = 1
                    else:
                        chosendb = 0
                    internalerrortype = np.random.randint(0, 3)
                    if (internalerrortype == 1):  # if 1 -> error in x axis if 0 -> error in y axis if 2 error is to delete the DB
                        if (np.random.randint(0, 2)):  # if 1 -> dislocation to the right, if 0 -> dislocation to the left
                            dislocation = np.random.randint(1, 4)
                            simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "x", dislocation, chosenDB=chosendb)
                        else:
                            dislocation = -1 * np.random.randint(1, 4)
                            simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "x", dislocation, chosenDB=chosendb)
                    elif (internalerrortype == 0):
                        if (np.random.randint(0, 2)):  # if 1 -> across lines. if 0 -> same grid
                            if (np.random.randint(0, 2)):  # if 1 -> dislocation upwards, if 0 -> dislocation downwards
                                dislocation = -1 * np.random.randint(1, 3)
                                simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "y", dislocation, chosenDB=chosendb)
                            else:
                                dislocation = np.random.randint(1, 3)
                                simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "y", dislocation, chosenDB=chosendb)
                        else:
                            (n, m, l) = DBPair[chosendb].latcoord
                            l_coord = int(l)
                            if (l_coord == 1):
                                simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "yGrid", 0, chosenDB=chosendb)
                            elif (l_coord == 0):
                                simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "yGrid", 1, chosenDB=chosendb)
                            else:
                                self.logger.error('ErrorAnalysis:    ERROR:  insertErrorDBPairs not able to read DBDot latcoord properly...')
                    elif (internalerrortype == 2):
                        simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "internal", "x", chosenDB=chosendb, deleteDB=1)
                        #updating db pair with the new recently created DBDot object -> because in this routine onde object is deleted and a new object representing the old dbdot is created
                        newdbDot = goldenCopy.dbDots[-1]
                        DBPair[chosendb] = newdbDot
                    else:
                        self.logger.error('ErrorAnalysis:    ERROR:  insertErrorDBPairs internalerrortype not valid ...')
                elif (errortype == 0):
                    if (np.random.randint(0, 2)):  # if 1 -> error in x axis if 0 -> error in y axis
                        if (np.random.randint(0, 2)):  # if 1 -> dislocation to the right, if 0 -> dislocation to the left
                            dislocation = np.random.randint(1, 4)
                            simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "external", "x", dislocation)
                        else:
                            dislocation = -1 * np.random.randint(1, 4)
                            simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "external", "x", dislocation)
                    else:
                        if (np.random.randint(0, 2)):  # if 1 -> across lines. if 0 -> same grid
                            if (np.random.randint(0, 2)):  # if 1 -> dislocation upwards, if 0 -> dislocation downwards
                                dislocation = -1 * np.random.randint(1, 3)
                                simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "external", "y", dislocation)
                            else:
                                dislocation = np.random.randint(1, 3)
                                simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "external", "y", dislocation)
                        else:
                            simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "external", "yGrid")
                elif (errortype == 2):
                    if (np.random.randint(0,2)):
                        chosendb = DBPair[1]
                    else:
                        chosendb = DBPair[0]

                    (n,m,l) = copy.deepcopy(chosendb.latcoord)
                    n_coord = int(n)
                    m_coord = int(m)
                    l_coord = int(l)

                    if (np.random.randint(0,2)): # x axis
                        if(np.random.randint(0,2)): # left or right
                            n_coord = n_coord + np.random.randint(1,3)
                        else:
                            n_coord = n_coord - np.random.randint(1, 3)
                    else: # y axis
                        if(np.random.randint(0,2)): # up
                            m_coord = m_coord - 1
                        else: # down
                            m_coord = m_coord + 1
                    if (np.random.randint(0,5) == 3): #invert l
                        if (l_coord):
                            l_coord = 0
                        else:
                            l_coord = 1
                    simresults = self.simulatePairModif(editor, goldenCopy, sim_mu, extPotVec, DBPair, "add", "x", coordenates=(n_coord, m_coord, l_coord))
                else:
                    self.logger.error('ErrorAnalysis:    ERROR:  insertErrorDBPairs errortype not set properly...')

                resultsBuffer.append(simresults)

            # decidir se vai ser um erro interno ou do par inteiro ou erro de adicionar db
                # interno:
                    # decidir em qual dos dbs do par será o erro
                        # decidir eixo x ou y
                            # se for y:
                                # decidir se vai ser na mesma linha ou across lines
                                    # se for across lines, decidir se e pra cima ou pra cima ou baixo.
                                        # decidir a quantidade do deslocamento. 1 ou 2
                                # se for na mesma linha, checar o l da latcooord. Se for 0, mudar pra 1, se for 1, mudar pra zero.
                            # se for x:
                                # decidir se vai ser direita ou esquerda
                                    # decidir a quantidade do deslocamento. 1 2 ou 3
                # appendar o buffer de resultados

                # no par inteiro:
                    #Se for erro posicional decidir eixo x ou y
                        # se for y:
                            # decidir se vai ser na mesma linha ou across lines
                                # se for across lines, decidir se e pra cima ou pra cima ou baixo.
                                    # decidir a quantidade do deslocamento. 1 ou 2
                            # se for na mesma linha, checar o l da latcooord. Se for 0, mudar pra 1, se for 1, mudar pra zero.
                        # se for x:
                            # decidir se vai ser direita ou esquerda
                                # decidir a quantidade do deslocamento. 1 2 ou 3
                # appendar o buffer de resultados

                # Se for db extra, pegar as coordenadas do par e inserir um DB extra em algum dos pontos vizinhos a no máximo 1 DB de distancia
                    # appendar o buffer de resultados

        self.NumErrorInserted = 0  # reset counter of num of errors inserted
        os.chdir(parent_dir)
        self.logger.debug(
            'ErrorAnalysis:    Finished error insertion in DBPairs. Number of iterations is: %s and final resultsBuffer is: %s',
            str(iterations), str(resultsBuffer))
        self.logger.info('ErrorAnalysis:    Running Sequential Model Error Insertion Simulation:  FINISHED')
        return resultsBuffer

    def runAssignableModel(self, design, sim_mu, inputNumber, extPotVec, iterations):
        resultsBuffer = []
        return resultsBuffer