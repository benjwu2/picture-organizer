from configDictionary import config
from zipfile import ZipFile
import importlib
import addressArray
array = getattr(addressArray, config["arrayToUse"])
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
    Month = monthDictionary[rawDate.split(":")[1]]
    # there has to be a better way to do this
    Day = rawDate.split(" ")[0].split(":")[2]
    Year = rawDate.split(" ")[0].split(":")[0]

    processedDate = "{} {}, {}".format(Month, Day, Year)

    print("Processed date: " + processedDate)
    return processedDate

# returns the file path for the first image in the folder whose file path
# is passed as an argument
def getFirstImagePath():
    fileList = os.listdir("./tempFolderName")

    filename = fileList[0]

    print("\n[FILEPATH FOR IMAGE USED TO EXTRACT DATE]")
    print("Image file: " + fileList[0])

    print("Image filepath: ./tempFolderName/{}".format(filename))
    return "./tempFolderName/{}".format(filename)

# extracts the files from "extractFile" into a newly made folder
# NB: this method must be called before getFirstImagePath in the code, as it creates
# the folder in the working directory whose path is used in getFirstImagePath
def extractFiles(extractFile):
    os.mkdir("./tempFolderName")
    with ZipFile(extractFile) as zObject:
        zObject.extractall("./tempFolderName")
    
    fileList = os.listdir("./tempFolderName")
    numFiles = len(fileList)
    word = "are" if numFiles > 1 else "is"
    plural = "s" if word == "are" else ""

    if numFiles == 0:
        sys.exit("Empty folder, canceling")

    print("\n[FOLDER INFORMATION]")
    print("There {} {} file{} in the folder: {}".format(word, numFiles, plural, fileList))
    checkFileTypes(config["preferredFileType"], config["defaultDest"])

    
# based on address and image metadata, assembles a suitable name for the
# folder of extracted images
# the date used is from the metadata of the first image in the folder
# the address is selected by the user inputting the street number of the desired address
def returnFolderName():
    extractFiles(input("\n\n\ninput image zip folder file path: ")[1:-1])

    streetAddress = returnFullAddress(input("\n\n\nEnter the street number: "))
    date = extractDateTime(getFirstImagePath())

    print("\n\n\n[FOLDER NAME]")
    print("Street address used: "+ streetAddress)
    print("Date: " + date)
    
    folderName = "{} - {}".format(streetAddress, date)
    finalPrint = folderName

    print("\n" + "="*(len(finalPrint)))
    print(finalPrint)
    print("="*(len(finalPrint)) + "\n")
    return folderName

# renames the folder to the name generated by newFolderName
def renameFolder():
    newFolderName = returnFolderName()
    os.rename("./tempFolderName", newFolderName)

# accepts a folder and checks the files for whether they are the inputted
# filetype or not
# lists non-inputted file types and files if there are any
# If all files are non-inputted files, then the program exits
# NOTES - checkFileTypes only works on unzipped files
def checkFileTypes(fileType, checkFile):
    badFiles = []
    badFileTypes = []

    print("\nChecking for file types besides {}...".format(fileType))

    # iterates through array of file names checking if they are jpg files
    for file in os.listdir(checkFile):
        # isolate the file extension, as the split after the last period should be it
        if file.split(".")[-1] != fileType:
            badFiles.append(file)
            if not file.split(".")[-1] in badFileTypes:
                badFileTypes.append(file.split(".")[-1])
    

    # Response based on number of bad files
    if len(badFiles) == len(os.listdir(checkFile)):
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


renameFolder()


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

