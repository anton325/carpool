"""
main.py
previously the main module of auto assign project.
Now gui.py is being used for this purpose
"""


import importTable as it
import algorithm as algo
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "table.xlsx"         # rel path of stocklist
    abs_file_path = os.path.join(script_dir, rel_path)       # absolute path to stocklist

    myIT = it.ImportTable(abs_file_path)
    df = myIT.fetchTable(myIT.path)
    sailors = myIT.processTable(df)

    myAlgo = algo.Alogorithm(sailors)

    drivers,riders = myAlgo.getDrivers()

    print("drivers:")
    [x.toString() for x in drivers]
    print("riders:")
    [x.toString() for x in riders]

    myAlgo.rideAssignment(drivers,riders)