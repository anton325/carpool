class Person:
    def __init__(self,email, name, cell, peopleCanDrive, location, comment):
        self.email = email
        self.name = name
        self.cell = cell
        self.peopleCanDrive = peopleCanDrive
        self.location = location
        self.comment = comment
        

    def getName(self):
        return self.name

    def getCell(self):
        return self.cell
    
    def getLocation(self):
        return self.location

    def getComment(self):
        return self.comment
    
    def getEmail(self):
        return self.email

    def getPeopleCanDrive(self):
        return self.peopleCanDrive

    def toString(self):
        print("Sailor name "+str(self.name)+ " can drive people to practice: "+str(self.peopleCanDrive) +
              " wants to get picked up in : "+str(self.location) + " comment: "+str(self.comment))



