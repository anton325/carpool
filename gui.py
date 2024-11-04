#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
gui.py
By Shanay Patel and Anton Giese

This project has been designed to facilitate the assignment of car rides for 
practice sessions of the Davis Sailing Team at UC Davis.
It processes the google response sheet the attendees have filled out and
proposes who is supposed to drive and who joins which car
However, the user has total control over who comes in which car and
who drives
Finally, the phone numbers of the people in each car are displayed
in a copy-paste friendly way, which allows the user to select and copy 
the numbers and a pre written message and start a text chain with
the Apple MacOS program "Messages".
"""

# modules
import tkinter as tk
from tkinter import StringVar, filedialog as fd
from importTable import ImportTable
from algorithm import Alogorithm
import os

"""
class App:
open the GUI for Assign rides
contains all the frames and all the functions
"""
#define class
class App:



    ####################################################################################################################################
    ##############################                     FRAME AND DISPLAY RELATED FUNCTIONS                ##############################
    ####################################################################################################################################



    """
    __init__
    initializing a bunch of things
    """
    def __init__(self):
        # get root tk instance
        self.master = tk.Tk()

        # Set geometry
        self.width = 1400
        self.height = 800
        geo = str(self.width) + "x" + str(self.height)
        self.master.geometry(geo)

        # Stop it from changing size
        # self.master.resizable(width=0, height=0)

        # how to react when closing the window
        self.master.protocol("WM_DELETE_WINDOW", self.quit_app)

        # main title
        self.master.title("Assign")
        self.current_frame = None

        self.showContinueButton = False

        self.assignmentDict = dict()

        
        # rollout mode
        # start with the first main frame
        self.set_main_frame()

        # debug mode
        # self.main_frame = tk.Frame(self.master)
        # script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        # rel_path = "responses.xlsx" #"table.xlsx"         # rel path of stocklist
        # self.filename = os.path.join(script_dir, rel_path)       # absolute path to stocklist
        # self.assignmentDict = self.process_table()
        # self.create_rides_frame()


    """
    Set_main_frame
    Will be first screen user sees and offers following functionalities
        - load google response file for this practice
        - continue if ride assignments are solveable
        - error message if too few drivers
        - edit message that will be send out to the sailors
    """
    def set_main_frame(self):
        # get main frame
        self.main_frame = tk.Frame(self.master)
        # frame management function for new frame:
        self.new_frame(self.main_frame)

        # WIDGETS
        self.selectFile_button = tk.Button(self.main_frame, text = "Select a google response file",
                                  command = self.select_file)
        # file label might need to get updated -> StringVar
        self.fileLabelString = tk.StringVar()
        self.fileLabelString.set("No file selected")
        self.fileLabel = tk.Label(self.main_frame, textvariable= self.fileLabelString )

        self.textLabel = tk.Label(self.main_frame, text = "The text message you want to send the sailors:")
        # load previously saved test message
        self.preWrittenText = self.load_messagePrePrint()

        self.messageEntry = tk.Text(self.main_frame)

        # put previous message in text field
        self.messageEntry.insert(1.0, self.preWrittenText)

        # overwrite message
        self.saveMessage_button = tk.Button(self.main_frame, text = "save edited message", command=self.saveEditedMessage)

        # quit button
        self.show_quit_button(self.main_frame)

        # Widgets position
        self.selectFile_button.grid(column = 1, row =   0, pady = (50,0), padx = (30,30)) #pady = (to the top, to the bottom)
        self.fileLabel.grid(column = 2 , row = 0, pady = (50,0), padx = (30,30))

        self.textLabel.grid(column = 1,
                            row = 1,
                            sticky = "N")
        self.messageEntry.grid(
            column = 2,
            row = 1
        )
        self.saveMessage_button.grid(
            column = 2,
            row = 2
        )

        # launch window
        self.main_frame.mainloop()


    """
    create_rides_frames
    - Shows user the assigned cars and comments.
    - If user wants they can reassign some riders using buttons located
    next to each rider in a car
    - User can change drivers
    """
    def create_rides_frame(self):
        # if user wants to assign too many people to one car (more than fit)
        # it shows error and doesn't let them proceed
        self.errorInRideAssignment = False

        self.assign_rides_frame = tk.Frame(self.master)
        self.new_frame(self.assign_rides_frame)
        self.show_quit_button(self.assign_rides_frame)

        # get information over neccesary grid size
        numberOfCars = len(self.assignmentDict.keys())
        # print(numberOfCars)
        maxNumberOfCarsPerRow = 4

        

        # fill rows them with the information about the drivers
        # i counts in which column we're currently
        i = 0
        # carCounter counts how many cars we've already looked at
        carCounter = 0

        # in case that we have more than 5 cars, we need to open a second row of cars and drivers
        # referenceRow counts up by 15 once we have reached 5 cars in one row
        referenceRow = 0
        drivers = self.assignmentDict.keys()

        # save reference to StringVars in dropdown menues
        self.shownDriver = dict()
        # save reference to the dropdown menues
        optionMenus = dict()
        # save reference to the car delete buttons
        deleteCarButtons = []

        for driver in drivers:
            # check if we've already created 5 cars for this row:
            if i >= maxNumberOfCarsPerRow:
                i = 0
                referenceRow += 15
            # create row names
            if i == 0:
                tk.Label(self.assign_rides_frame, text = "Driver: ").grid(
                    column = 0,
                    row = referenceRow + 1,
                    sticky="nswe"
                    
                )
                tk.Label(self.assign_rides_frame, text = "Available seats").grid(
                    column = 0,
                    row = referenceRow + 2,
                    sticky="nswe"
                )
                tk.Label(self.assign_rides_frame, text = "Riders: ").grid(
                    column = 0,
                    row = referenceRow + 3,
                    sticky="nswe"
                )

            # for each car put car number and driver's name in first two rows
            # there's i*numberOfCars empty columns within each car 
            # because that's where the buttons to move every rider go
            carText = "Car number "+str(carCounter+1)
            # car number goes in the very first row (one over the driver row)
            tk.Label(self.assign_rides_frame, text = carText).grid(
                column = i*numberOfCars+1,
                row = referenceRow,
                sticky="nswe"
            )
            # print("Car number "+str(carCounter+1) + " in col "+str(i*numberOfCars+1))

            # for each driver create a dropdown menu that allows to exchange 
            # him with other driver that is currently not driving

            # retrieve list of people that could drive but are currently not selected
            driverName = driver.getName()
            dropdownChoices = self.getDropdownChoices(i+1)
            
            # add driver to dropdown menu such that changing nothing also stays an option
            dropdownChoices.append(str(carCounter+1) + ":" + driverName +" ("+str(driver.getPeopleCanDrive()) +")")

            self.shownDriver[driverName] = tk.StringVar()
            self.shownDriver[driverName].set(driverName)
            self.shownDriver[driverName].set(dropdownChoices[len(dropdownChoices)-1])

            thisOptionMenu = tk.OptionMenu(
                self.assign_rides_frame, 
                self.shownDriver[driverName],
                *dropdownChoices,
                command = self.handleNewDriver
            )
            thisOptionMenu.grid(
                column = i*numberOfCars+1,
                row = referenceRow+1,
                sticky="nswe"
            )
            optionMenus[driverName] = thisOptionMenu

            # display number of available seats this driver has in total
            tk.Label(self.assign_rides_frame, text = driver.getPeopleCanDrive()).grid(
                column = i*numberOfCars+1,
                row = referenceRow+2
            )

            # every car has a delete car button:
            # each car can be deleted with the press of a button
            deleteButton = tk.Button(self.assign_rides_frame,
                                    text = "delete car",
                                    command = lambda d = driverName : self.deleteCarButton(d)
                                    )
            deleteButton.grid(
                column = i * numberOfCars + 1,
                row = referenceRow+14,
                sticky="nswe"
            )
            deleteCarButtons.append(deleteButton)                                
            i+=1
            carCounter+=1

        # create one extra column at the very right end where a new driver can be added
        tk.Label(self.assign_rides_frame,
                 text = "Add another car").grid(
                     column = i * numberOfCars + 1,
                     row = referenceRow + 3,
                    sticky="nswe"
                 )
        # print("last col: "+str(i*numberOfCars+1))
        # find all additional drivers that can be displayed in the dropdown menu
        dropdownChoices = self.getDropdownChoices(i+1)
        chosenDriver = tk.StringVar()
        chosenDriver.set(dropdownChoices[0])
        tk.OptionMenu(
                self.assign_rides_frame, 
                chosenDriver,
                *dropdownChoices,
                command = self.handleAdditionalDriver
            ).grid(
            column = i*numberOfCars+1,
            row = referenceRow + 4,
            sticky="nswe"
        )

        carCounter = 0
        referenceRow = 0
        # create the buttons that allow user to move riders between cars
        # start in column 0 (i), where information about the first car is located
        i = 0
        j = 0   # overwritten later anyways, but still important !
        # we are building a button dictionary to save all the buttons that
        # will be used to move riders to different cars
        buttonDict = dict()             # we need to keep track of the buttons
        pixelDict = dict()
        for driver in drivers:
            # check if we've filled the row
            if i >= maxNumberOfCarsPerRow:
                i = 0
                referenceRow += 15
            # create emtpy list for this particular car (key is driver)
            buttonDict[driver.getName()] = []
            pixelDict[driver.getName()] = []
            # every time we're starting in row 3 (j)
            j = 3
            numRiders = 0
            for rider in self.assignmentDict[driver]:
                if rider != driver:
                    # if too many people in car -> red border around person
                    # else just a regular label of person 
                    if numRiders >= driver.peopleCanDrive-1:
                        self.errorInRideAssignment = True
                        tk.Label(self.assign_rides_frame,
                                 text = rider.getName(),
                                 bg = "red").grid(
                        column = i*numberOfCars+1,
                        row = referenceRow + j,
                        sticky="nswe"
                    )
                    else:
                        tk.Label(self.assign_rides_frame, text = rider.getName()).grid(
                            column = i*numberOfCars+1,
                            row = referenceRow + j,
                            sticky="nswe"   
                        )
                    numRiders += 1
                    # for each rider we'll create numberOfCars-1 buttons. If user presses
                    # button 2 for person 1 in car 1, person 1 will be moved to car 2
                    buttonIndex = 0     # counts the offset between this button's respective driver's column and the button
                    buttonTextNumber = 0    # text on button -> to which car person should be assigned
                    for otherDrivers in drivers:
                        if otherDrivers != driver:
                            buttonText = str(buttonTextNumber+1)
                            thisPixel = tk.PhotoImage(width=1, height=1)
                            # button = tk.Button(root, text="", image=pixel, width=100, height=100, compound="c")
                            thisButton = tk.Button(self.assign_rides_frame,
                                      text = buttonText,
                                      image = thisPixel,
                                      width = 10,
                                      height = 10,
                                      compound = "center",
                                      command = lambda d = driver, r = rider, a = otherDrivers: self.moveRider(d,r,a))
                            thisButton.grid(
                                column = i*numberOfCars+buttonIndex+1+1,
                                row = referenceRow + j,
                                sticky="nswe"
                            )
                            # print("button in col "+str(i*numberOfCars+buttonIndex+1+1))
                            # print("button in row "+str(j))
                            buttonDict[driver.getName()].append(thisButton)
                            pixelDict[driver.getName()].append(thisPixel)
                            buttonIndex += 1
                        buttonTextNumber += 1
                    j += 1
            i+=1
            carCounter += 1
        # print(i)
        # vergebenWeight = 0
        # zaehler = 0
        
        # print(numberOfCars)
        # print("last i "+str(i*numberOfCars))
        self.assign_rides_frame.columnconfigure(0,weight=numberOfCars)
        # vergebenWeight += numberOfCars
        # zaehler +=1
        for col in range(1,i*numberOfCars+1):
            if (col%numberOfCars)  == 2:
                self.assign_rides_frame.columnconfigure(col,weight = numberOfCars)
                # vergebenWeight += numberOfCars            
                # zaehler +=1
            else:
                self.assign_rides_frame.columnconfigure(col,weight = 1)
                # zaehler +=1
                # vergebenWeight += 1
        self.assign_rides_frame.columnconfigure(i*numberOfCars+1,weight=numberOfCars)
        # zaehler +=1
        # print("zähler: "+str(zaehler))
        # vergebenWeight += numberOfCars
        # print("vergeben: "+ str(vergebenWeight))
        # self.assign_rides_frame.columnconfigure(1,weight=5)
        # self.assign_rides_frame.columnconfigure(2,weight=1)
        # self.assign_rides_frame.columnconfigure(3,weight=1)
        # self.assign_rides_frame.columnconfigure(4,weight=1)
        # self.assign_rides_frame.columnconfigure(5,weight=1)
        # self.assign_rides_frame.columnconfigure(6,weight=5)
        # self.assign_rides_frame.columnconfigure(7,weight=1)
        # self.assign_rides_frame.columnconfigure(8,weight=1)
        # self.assign_rides_frame.columnconfigure(9,weight=1)
        # self.assign_rides_frame.columnconfigure(10,weight=1)
        # self.assign_rides_frame.columnconfigure(11,weight=5)
        # self.assign_rides_frame.columnconfigure(12,weight=1)
        # self.assign_rides_frame.columnconfigure(13,weight=1)
        # self.assign_rides_frame.columnconfigure(14,weight=1)
        # self.assign_rides_frame.columnconfigure(15,weight=1)
        # self.assign_rides_frame.columnconfigure(16,weight=5)
        # self.assign_rides_frame.columnconfigure(17,weight=1)
        # self.assign_rides_frame.columnconfigure(18,weight=1)
        # self.assign_rides_frame.columnconfigure(19,weight=1)
        # self.assign_rides_frame.columnconfigure(20,weight=1)
        # self.assign_rides_frame.columnconfigure(21,weight=5)
        # self.assign_rides_frame.columnconfigure(22,weight=1)
        # self.assign_rides_frame.columnconfigure(23,weight=1)
        # self.assign_rides_frame.columnconfigure(24,weight=1)
        # self.assign_rides_frame.columnconfigure(25,weight=1)
        # self.assign_rides_frame.columnconfigure(26,weight=5)
        
        # show the comments people made on google form below the car grid
        numComments = 0             # keep track of the amount of comments
        rowComments = 0             # keep track of the row we're in right now
        myPady = (20,0)             # first comment should have nice distance to top
        tk.Label(self.assign_rides_frame, text = "Comments: ").grid(
                column = 0,
                row = referenceRow+j+15,
                pady = myPady)
        myPady = (0,0)
        for driver in drivers:
            for rider in self.assignmentDict[driver]:
                # check if there's comment to display
                if rider.getComment() != "Null":
                    thisComment = rider.getName() + " says: "+rider.getComment()
                    if numComments%2==0:
                        tk.Label(self.assign_rides_frame, text = thisComment).grid(
                                column = 0,
                                row =referenceRow + j + 15 + rowComments + 1,
                                pady = myPady,
                                columnspan = int(len(drivers) * maxNumberOfCarsPerRow/2))
                    else:
                        tk.Label(self.assign_rides_frame, text = thisComment).grid(
                                column = int(len(drivers) * maxNumberOfCarsPerRow/2),
                                row =referenceRow + j + 15 + rowComments + 1,
                                pady = myPady,
                                columnspan = int(len(drivers) * maxNumberOfCarsPerRow/2))
                        rowComments += 1
                    numComments += 1
                    

        # check if everyone is in a car
        total = 0
        for driver in drivers:
            total += len(self.assignmentDict[driver])

        if total != len(self.allSailors):
            # not everyone is in a car
            missingPeople = len(self.allSailors) - total
            self.errorInRideAssignment = True
            errorLabel = tk.Label(self.assign_rides_frame,
                         text = "Due to too few drivers, "+str(missingPeople) + " person can't be assigned to a car"
                         )
            errorLabel.grid(
                column = 0,
                row = referenceRow + j + numComments + 16,
                columnspan= int(len(drivers) * maxNumberOfCarsPerRow),
                pady = (0,0)
                )
            errorLabel.config(bg="red")    

        # if there's no error the user is allowed to proceed to next screen
        if not self.errorInRideAssignment:
            tk.Button(self.assign_rides_frame, 
                      text = "Generate text messages",
                      command = self.create_messages_frame).grid(column = 0,
                                                            row = referenceRow + j+numComments+16,
                                                            columnspan = int(len(drivers) * maxNumberOfCarsPerRow),
                                                            pady = (0,0))            
        self.assign_rides_frame.mainloop()



    """
    create_messages_frame
    Last frame of application: 
    for each car show all telephone numbers in one field that allows copy and paste
    and one field with the generated text message for this car 
    """
    def create_messages_frame(self):
        self.messages_frame = tk.Frame(self.master)
        self.new_frame(self.messages_frame)
        self.show_quit_button(self.messages_frame)
        drivers = self.assignmentDict.keys()
        self.preWrittenText = self.load_messagePrePrint()
        j = 0
        bestWidth = 0
        # find out what the best width for the telephone cell is  
        for d in self.assignmentDict:
            phoneNumberString = ""
            for r in self.assignmentDict[d]:
                phoneNumberString += r.getCell()
            if len(phoneNumberString) >= bestWidth:
                bestWidth = len(phoneNumberString)

        for driver in drivers:
            carText = "Phone numbers in car "+str(int(j/2)+1)
            messageText = "Message for them:"
            tk.Label(self.messages_frame, text = carText).grid(
                column = 0,
                row = j,
                pady = (15,0)
            )
            tk.Label(self.messages_frame, text = messageText).grid(
                column = 0, 
                row = j+1
            )

            # build telephone number string for this car
            phoneNumberString = ""
            for rider in self.assignmentDict[driver]:
                if rider == self.assignmentDict[driver][0]:
                    phoneNumberString += rider.getCell()
                else:
                    phoneNumberString += "\n"+rider.getCell()
        
            phoneNumberStringLabel = StringVar()
            phoneNumberStringLabel.set(phoneNumberString)
            phoneNumbersEntry = tk.Entry(self.messages_frame,
                           textvariable = phoneNumberStringLabel,
                           fg = "black",
                           bg = "white",
                           bd = 0,
                           state = "readonly",
                           width = bestWidth)
            phoneNumbersEntry.grid(
                column = 1,
                row = j,
                pady = (15,0)
                
            )
            preMessageVar = StringVar()

            # get first name of car's driver to personalize message
            firstname = ""
            try:
                firstname = driver.getName().split(" ")[0]
            except:
                firstname = driver.getName()

            preMessageVar.set(self.preWrittenText.replace("{name}", firstname))
            messageEntry = tk.Entry(self.messages_frame, textvariable = preMessageVar, width=bestWidth)
            messageEntry.grid(
                column = 1,
                row = j+1
            )
            j += 2
    
    ####################################################################################################################################
    ##############################                     BUTTON AND COMMAND HELPER FUNCTIONS                ##############################
    ####################################################################################################################################
        
    """
    deleteCarButton
    When the user wants to get rid of a car, they can delete the car
    as a result the driver gets removed from the driver list and added to the rider list
    Then the algorithm makes a proposal which is then displayed
    """
    def deleteCarButton(self,driverName):
        # delete this driver from list of drivers
        newDrivers = self.deleteFromList(self.assignmentDict.keys(),driverName)
        # add this driver to the riders
        allRiders = self.getAllRiders()
        newRiders = self.addToList(allRiders,driverName)

        # run algorithm and picture results
        self.assignmentDict = self.myAlgo.rideAssignment(newDrivers, newRiders)
        self.create_rides_frame()


    """
    moveRider
    function that will be called when a move rider button is pressed
    """
    def moveRider(self,driver,rider,newCar):
        self.assignmentDict[driver].remove(rider)
        self.assignmentDict[newCar].append(rider)
        self.create_rides_frame()

    """
    handleAdditionalDriver
    Now a driver isn't replaced but completely added
    Add driver to the list of drivers and remove him from the list of riders
    """
    def handleAdditionalDriver(self, driverName):
        # get new drivers name (it's slightly encoded)
        newDriver = driverName.split(":")[1]
        newDriverName = newDriver[0:len(newDriver)-4]

        # add driver to drivers list
        newDrivers = self.addToList(self.assignmentDict.keys(), newDriverName)
        
        # delete new driver from the rider list
        oldRiders = self.getAllRiders()
        newRiders = self.deleteFromList(oldRiders,newDriverName)
        
        self.assignmentDict = self.myAlgo.rideAssignment(newDrivers, newRiders)
        self.create_rides_frame()

    """
    handleNewDriver
    - selection is the string carNumber:Name(people he can drive)
      carNumber tells us, which driver is supposed to be replaced
    - old driver is replaced by new driver and old rider is replaced by new rider
    """
    def handleNewDriver(self,selection):
        # REPLACE old driver with new driver without changing order
        newDrivers = []
        index = int(selection.split(":")[0])-1
        # copy everything except replace old driver for new driver
        i = 0
        for driver in self.assignmentDict.keys():
            if i == index:
                newDriver = selection.split(":")[1]
                newDriver = newDriver[0:len(newDriver)-4]
                for all in self.allSailors:
                    if all.getName() == newDriver:
                        newDrivers.append(all)
                        break
            else:
                newDrivers.append(driver)
            i += 1
        
        # replace old rider with new rider
        newRiders = []
        for sailor in self.allSailors:
            isDriver = False
            for newDriver1 in newDrivers:
                if sailor.getName() == newDriver1.getName():
                    isDriver = True
            if not isDriver:
                newRiders.append(sailor)
        
        self.assignmentDict = self.myAlgo.rideAssignment(newDrivers, newRiders)
        self.create_rides_frame()   

    ####################################################################################################################################
    ##############################                     INFORMATION GATHER HELPER FUNCTIONS                ##############################
    ####################################################################################################################################
    
    """
    getDropdownChoices
    - create the entries that go in the dropdown menu for each driver,
      where this driver can be replaced by a different driver
    """
    def getDropdownChoices(self,carNumber):
        drivers = self.assignmentDict.keys()
        # find out who could be driving but isn't driving as of right now
        potentialDrivers = self.allSailors - drivers
        dropdownChoices = []
        for potentialDriver in potentialDrivers:
            if potentialDriver.getPeopleCanDrive() != 0:
                # create the string for this particular driver:
                # carNumber:Name(people he can drive)
                text = str(carNumber)+":"+potentialDriver.getName() + " (" + str(potentialDriver.getPeopleCanDrive()) +")"
                dropdownChoices.append(text)
        return dropdownChoices
    
    """
    findObjectToName
    sometimes when you only have the name of the person you want to get the person object
    It looks throught all the objects and returns the one where the name matches
    """
    def findObjectToName(self,name):
        for sailor in self.allSailors:
            if sailor.getName() == name:
                return sailor


    """
    deleteFromList
    takes a list and an item in the list and copies all elements except 
    the one that's supposed to be deleted
    """
    def deleteFromList(self, oldSailors, sailor):
        newList = []
        for oldD in oldSailors:
            # print(sailor)
            # print(oldD.getName())
            if sailor != oldD.getName():
                newList.append(oldD)
        return newList

    """
    addToList
    Takes a list and an element and adds it to the list
    """
    def addToList(self, oldSailors, newSailor):
        newSailors = []
        for sailor in oldSailors:
            newSailors.append(self.findObjectToName(sailor.getName()))
        newSailors.append(self.findObjectToName(newSailor))
        return newSailors

    """
    getAllRiders
    returns a list of exlusively riders (whether they are assigned to a driver or not)
    by iterating over all sailors and ignoring the ones that are drivers
    """
    def getAllRiders(self):
        riders = []
        for sailor in self.allSailors:
            if not self.checkIfDriver(sailor.getName()):
                riders.append(sailor)
        return riders

    """
    checkIfDriver
    takes a name and checks if that person is a driver or not
    """
    def checkIfDriver(self,riderName):
        for driver in self.assignmentDict.keys():
            if driver.getName() == riderName:
                return True
        return False

    """
    process_table
    check if the conitune button is already shown (e.g. from previous loaded table) and 
    destroy it if that's the case
    run assignment algorithm on newly loaded table and check if there's enough drivers.
    If not, show warning, else display button to proceed
    """
    def process_table(self):
        if self.showContinueButton:
            self.continue_button.destroy()
            self.showContinueButton = False
        myIT = ImportTable(self.filename)
        df = myIT.fetchTable(myIT.path)
        sailors = myIT.processTable(df)
        self.allSailors = sailors.copy()
        self.myAlgo = Alogorithm(sailors)
        
        if self.myAlgo.checkEnoughDrivers():
            # if enough drivers
            self.showContinueButton = True
            drivers,riders = self.myAlgo.getDrivers()
            self.continue_button = tk.Button(self.main_frame, text = "Assign Rides for this practice", command = self.create_rides_frame)
            self.continue_button.grid(column = 2, row = 4, pady = 300)
            return self.myAlgo.rideAssignment(drivers,riders)
        else :
            # not enough drivers
            warningLabel = tk.Label(self.main_frame, text = "Not enough drivers for this many sailors!")
            warningLabel.grid(
                row = 4,
                column = 2 
            )
            warningLabel.config(font=("Courier", 20))
            warningLabel.config(bg="red")
            warningLabel.after(4000, lambda: warningLabel.destroy())
            return None


    ####################################################################################################################################
    ################################                     FILE HANDLING HELPER FUNCTIONS                #################################
    ####################################################################################################################################

    """
    saveEditedMessage
    edit message sent out to sailors and save it so it'll be
    available next time
    Shows self destroying confirmation message
    """
    def saveEditedMessage(self):
        # get message
        newMessage = self.messageEntry.get("1.0",'end-1c')
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "textmessage.txt"         # rel path of file to load
        messagePath = os.path.join(script_dir, rel_path)       # absolute path to file to load
        f = open(messagePath, 'w')
        f.write(newMessage)
        f.close()
        # show and set timer on confirmation label
        self.confirmLabel = tk.Label(self.main_frame, text = "Message saved!")
        self.confirmLabel.grid(
            column = 2,
            row = 3
        )
        self.confirmLabel.after(2000, lambda: self.confirmLabel.destroy())


    """
    select_file
    window to select appropriate google response sheet
    runs ride assign algorithm on loaded information
    """
    def select_file(self):
        filetypes=(("excel files", "*.xls"), ("excel files", "*.xlsx"), ("all files", "*.*"))
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.filename = filename
        self.fileLabelString.set(self.filename)
        # run algorithm
        self.assignmentDict = self.process_table()
        
    """
    load_messagePrePrint
    load saved message from file
    """
    def load_messagePrePrint(self):
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "textmessage.txt"         # rel path of stocklist
        messagePath = os.path.join(script_dir, rel_path)       # absolute path to stocklist
        f = open(messagePath)
        message = f.read()
        f.close()
        return message

    ####################################################################################################################################
    ###############################                     FRAME AND WINDOW HELPER FUNCTIONS                ###############################
    ####################################################################################################################################




    """
    new_frame
    Handles frame management
    When there is a new frame we delete the old frame and set new frame as current
    """
    def new_frame(self,new):
        # destroy old frame (if any)
        if not (self.current_frame is None):
            self.current_frame.destroy()
        # set new frame as current
        self.current_frame = new
        #pack new frame
        self.current_frame.pack()


    """
    """
    def show_quit_button(self,frame):
        self.quit_button = tk.Button(frame, text = "Quit", command = self.quit_app)
        self.quit_button.grid(column = 1, row = 100, pady = 0)
        
    def quit_app(self):
        # print("Programm beendet")
        self.master.destroy()


#App ausführen (Instanz der Klasse App erstellen)
app = App()
