from configDictionary import config
from zipfile import ZipFile
import importlib
import infoArrays
array = getattr(infoArrays, config["arrayToUse"])
purposeArray = getattr(infoArrays, "purposeArray")
personArray = getattr(infoArrays, "personArray")

from PIL import Image
from PIL.ExifTags import TAGS
from monthDictionary import monthDictionary

import os
import sys



# returns a full address from the array of addresses in addressArray.py (array) that has a
# street number that matches the passed number. If there are multiple addresses in array
# that start with the same street number, the user is prompted to select the address that
# they want to use
def returnFullAddress(streetNumber):
    if streetNumber == "cancel":
        sys.exit("\nCanceled by user")

    # array to accumalate matching addresses
    matches = []

    # iterates through the array looking for addresses that have a street number that matches the input
    for address in array:
        # address.split(" "[0]) isolates the street number from the current address "selected"
        # in the array of addresses
        if address.split(" ")[0] == streetNumber:
            matches.append(address)
    
    # number of matches logic
    if len(matches) == 0:
        print("\nThere are no addresses with this street number")
        retry = input("Enter the street number (enter \"cancel\" to exit): ")

        # recursion
        return returnFullAddress(retry)
    
    # if there is only one match, return it
    elif len(matches) < 2:
        print("Corresponding full address: {}".format(matches[0]))
        return matches[0]
    else:
        labeledMatches = appendNumberLabel(copyArray(matches))
        print("\nThere are multiple addresses with this street number: {}".format(labeledMatches))
        selector = None

        # making sure the number inputted by the user corresponds to one of the matching addresses i.e. 1 for the first match
        # 2 for the second, etc.

        # selector is the *valid* option picked by the user. userInput is the possibly invalid option picked.
        # if userInput passes the check, it is set as the value of selector
        while selector == None:
            userInput = int(input("Select one of the matches by entering the corresponding number \"1\" for the first option, \"2\" for the second, etc: "))
            if (userInput) == "cancel":
                sys.exit("Canceled by user")
            elif (userInput > 0 and userInput <= len(matches)):
                selector = userInput
            else:
                print("\nEnter a valid number (enter \"cancel\" to exit)")

        address = matches[selector-1]

        print("\nYou selected {}".format(address))
        return(matches[selector-1])

# returns a copy of the inputted array
def copyArray(array):
    newArray = []
    for element in array:
        newArray.append(element)
    return newArray

# takes an inputted array and appends ascending numbers
# to the start of the element i.e 1 to the first element, 2 to the second, etc.
def appendNumberLabel(array):
    for index, element in enumerate(array):
        array[index] = "({}) {}".format(index+1, element)
    return array

# returns a writen date based on the metadata of the image file whose path is passed as an argument
def extractDateTime(filepath):
    img = Image.open(filepath)

    # checks if there is a DateTimeKey metadata value
    if not(306 in img.getexif()):
        sys.exit("no metadata, rename folder manually")

    print("\n[EXTRACTED DATE]")
    print("Raw date: " + img.getexif()[306])
    rawDate = img.getexif()[306]

    # "rawDate.split(":")[1]" outputs the month part of the raw date (e.g. the 07 from 2023:07:13 14:37:25)
    # monthDictionary has these two digit codes as keys to values which are the month names that correspond to these codes
    # e.g. {"02": February}
    Month = rawDate.split(":")[1]
    # there has to be a better way to do this
    Day = rawDate.split(" ")[0].split(":")[2]
    Year = rawDate.split(" ")[0].split(":")[0]

    processedDate = "{}.{}.{}".format(Month, Day, Year)

    print("Processed date: " + processedDate)
    return processedDate

# returns the file path for the first image in the folder whose file path
# is passed as an argument in folder
def getFirstImagePath(folder):
    fileList = os.listdir(folder)

    filename = fileList[0]

    print("\n[FILEPATH FOR IMAGE USED TO EXTRACT DATE]")
    print("Image file: " + fileList[0])

    print("Image filepath: {}/{}".format(folder,filename))
    return "{}/{}".format(folder,filename)

# Extracts the files from "extractFile" into a newly made folder
# NB: this method must be called before getFirstImagePath in the code, as it creates
# the folder in the working directory whose path is used in getFirstImagePath.
# extractTarget and destFile are strings containing file paths
def extractFiles(extractTarget, destFile):

    # make a folder at destFile and extract files from folder at extractFile to destFile
    os.mkdir(destFile)
    with ZipFile(extractTarget) as zObject:
        zObject.extractall(destFile)
    
    fileList = os.listdir(destFile)
    numFiles = len(fileList)
    word = "are" if numFiles > 1 else "is"
    plural = "s" if word == "are" else ""

    if numFiles == 0:
        sys.exit("Empty folder, canceling")

    print("\n[FOLDER INFORMATION]")
    print("There {} {} file{} in the folder: {}".format(word, numFiles, plural, fileList))
    checkFileTypes(config["preferredFileType"], config["defaultDest"])

# returns the element of purposeArray that the user selected
def returnPurpose():
    labeledArray = appendNumberLabel(copyArray(purposeArray))
    selection = input("Enter the number corresponding to the purpose of the work order {}: ".format(labeledArray))

    return purposeArray[int(selection) - 1]

def returnPerson():
    printLabeledArray(personArray)
    selection = input("Enter the number corresponding to the person completing the work order: ")

    return personArray[int(selection) - 1]

# takes an inputted array as an argument and prints
# the elements on separate lines prepended by numbers
def printLabeledArray(array):
    numberedTuple = enumerate(array)

    for index, value in numberedTuple:
        print("({}) {}".format(index + 1, value))

# take a folder whose file path is inputted and rename it according to inputs from the
# user and the date information extracted from the images inside
def returnFolderName(folder):

    date = extractDateTime(getFirstImagePath(folder))
    streetAddress = returnFullAddress(input("\n\n\nEnter the street number: "))
    purpose = returnPurpose()
    person = returnPerson()

    print("\n\n\n[FOLDER NAME]")
    print("Date: " + date)
    print("Street address used: " + streetAddress)
    print("Purpose: " + purpose)
    print("Person: " + person)
    
    
    folderName = "{} {} {} - {}".format(date, streetAddress, purpose, person)
    

    print("\n" + "="*(len(folderName)))
    print(folderName)
    print("="*(len(folderName)) + "\n")
    return folderName

# renames the folder specified by the file path provided as an argument to the name generated by newFolderName
def renameFolder(folder):
    newFolderName = returnFolderName(folder)
    os.rename(folder, newFolderName)

# accepts a file path and returns True if the file is of the type fileType (no ".", e.g. jpg),
# False if not
def checkFile(file, fileType):
    if file.split(".")[1] == fileType:
        return True
    else:
        return False

# accepts a folder and checks the files for whether they are the inputted
# filetype or not
# lists non-inputted file types and files if there are any
# If all files are non-inputted files, then the program exits
# NOTES - checkFileTypes only works on unzipped files
def checkFileTypes(fileType, checkFolder):
    badFiles = []
    badFileTypes = []

    print("\nChecking for file types besides {}...".format(fileType))

    # iterates through array of file names checking if they are jpg files
    for file in os.listdir(checkFolder):
        # isolate the file extension, as the split after the last period should be it
        if file.split(".")[-1] != fileType:
            badFiles.append(file)
            if not file.split(".")[-1] in badFileTypes:
                badFileTypes.append(file.split(".")[-1])
    

    # Response based on number of bad files
    if len(badFiles) == len(os.listdir(checkFolder)):
        sys.exit("There are only files of the type {} in the folder, cancelling".format(badFileTypes))

    if len(badFiles) > 0:
        # making error message grammatically correct based on the number of bad files and file types
        wordFileTypes = "is" if len(badFileTypes) == 1 else "are"
        numberFileTypes = len(badFileTypes)
        pluralFileTypes = "" if len(badFileTypes) == 1 else "s"

        wordFiles = "is" if len(badFiles) == 1 else "are"
        numberFiles = len(badFiles)
        pluralFiles = "" if len(badFiles) == 1 else "s"
        print("WARNING - There {} {} file type{} in the folder besides {}:\n File types: {}\nThere {} {} file{} with bad file types: {}".format(wordFileTypes, numberFileTypes, pluralFileTypes, fileType, badFileTypes, wordFiles, numberFiles, pluralFiles, badFiles))
        
        # option to quit program if there are bad file types
        userInput = input("\nContinue? Enter Y or N: ")
        while(userInput != "Y" and userInput != "N"):
            userInput = input("\nBad input, enter Y or N: ")
            if (userInput == "N"):
                sys.exit("Canceled by user")
            elif (userInput == "Y"):
                break
            else:
                continue

    else:
        print("All files are {}s as expected :)".format(fileType))


renameFolder(input("Input the file path for the folder to be renamed (with quotes): ")[1:-1])


# getImageInfo(r"C:\Users\benjw\Downloads\Photos-001 (1).zip")

# right click the zip file to be unzipped and select "Copy as path"
# this is what is to be pasted into command prompt when prompted

# the slice [1:-1] gets rid of the quotes around the pasted file path, as the input method
# will add another pair of quotes around what is inputted, making ZipFile unable to read the path
# filePath = input("Enter the file path (with quotes): ")[1:-1]

# os.mkdir("./{}".format(address))

# with ZipFile(filePath) as zObject:
#     zObject.extractall(path="./extract output")
    # pastes unzipped folder into the command prompt working directory

