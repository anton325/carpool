"""
importTable
read google sheet and create the appropriate object for each person
"""

from person import Person
import pandas as pd
import math

class ImportTable:
    def __init__(self, path):
        self.path = path

    def fetchTable(self, path):
        self.df = pd.read_excel(path, engine = "openpyxl")
        return self.df

    def processTable(self, df):
        # list of sailors where objects will be iteratively added
        sailors = []
        for index, row in df.iterrows():
            email = row['Email Address']
            name = row['Name']
            cell = self.cellNumberProcess(str(row['Cell number']))

            # process information how many they can take to practice
            peopleCanDrive = row['How many people can you drive to practice including yourself?']
            if peopleCanDrive == "None":
                peopleCanDrive = 0
            elif peopleCanDrive == "Only myself":
                peopleCanDrive = 1
            elif peopleCanDrive == "More than 5":
                peopleCanDrive = 6
            else:
                # check if it's a float NaN
                if pd.isna(peopleCanDrive):
                    peopleCanDrive = 0
                else:
                    peopleCanDrive = int(peopleCanDrive)

            location = row['Pickup Location']

            # some people have made comments, some have not
            # first of all check if the comment column still exists
            comment = ""
            try:
                comment = row['Anything else we should know?']
            except:
                # it doesnt exist
                comment = "Null"

            try:
                math.isnan(row['Anything else we should know?'])
                comment = "Null"
            except:
                pass
            thisPerson = Person(email, name, cell, peopleCanDrive, location, comment)
            sailors.append(thisPerson)
        return sailors
            
    """
    cellNumberProcess
    they should be in a certain format
    """
    def cellNumberProcess(self,number):
        newNumber = number
        if number[0] != "+":
            newNumber = "+1"+ str(newNumber).split('.')[0]
        return newNumber
