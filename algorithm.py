"""
algorithm
heart piece of the car assign algorithm
"""

from person import Person

class Alogorithm:
    def __init__(self, PracticeAttendees):
        self.PracticeAttendees = PracticeAttendees
        
    """
    checkEnoughDrivers
    check if everybody gets to practive
    """
    def checkEnoughDrivers(self):
        totalSailors = len(self.PracticeAttendees)
        totalPeopleCanTake = 0
        for sailor in self.PracticeAttendees:
            canTake = sailor.peopleCanDrive
            totalPeopleCanTake += canTake
        return totalSailors <= totalPeopleCanTake


    """
    rideAssignment
    assign rides with following procedure:
    - assign people with same pickup preference as driver to them as long as car is not full
    - fill up cars randomly until everybody is assigned to a car
    """
    def rideAssignment(self, drivers, riders):
        assignmentDict = dict()
        for driver in drivers:
            driversLocation = driver.getLocation()
            addedRiders = 1
            assignedRiders = [driver]
            for rider in riders:
                if addedRiders >= driver.peopleCanDrive:
                    # car full
                    break
                if rider.getLocation() == driversLocation:
                    # same pickup preferences
                    assignedRiders.append(rider)
                    addedRiders += 1
                    riders.remove(rider)
            assignmentDict[driver] =  assignedRiders.copy()
        
        # fill up non-full cars
        for k in assignmentDict.keys():
            while len(assignmentDict[k]) < k.peopleCanDrive:
                if len(riders) == 0:
                    break
                assignmentDict[k].append(riders.pop(0))
            
        return assignmentDict



    """
    getDrivers
    sort all drivers based on how many people they can take and select drivers using 
    greedy selection -> select drivers based on minimizing the number of drivers
    """
    def getDrivers(self):
        driverList = []
        riderList= []
        sortedList = []
        totalSeats = len(self.PracticeAttendees)

        # sort drivers
        for i in range(totalSeats):
            maxVal = 0
            for j in range(len(self.PracticeAttendees)):
                if self.PracticeAttendees[j].peopleCanDrive >= maxVal:
                    maxVal = self.PracticeAttendees[j].peopleCanDrive
                    pos = j
            sortedList.append(self.PracticeAttendees[pos])
            self.PracticeAttendees.pop(pos)
        
        availableSeats = 0
        iter = 0
        # select drivers greedily
        while availableSeats < totalSeats:
            driverList.append(sortedList[iter])
            availableSeats = sortedList[iter].peopleCanDrive + availableSeats
            iter = iter + 1
        
        riderList = sortedList[iter:]

        
        return driverList,riderList
