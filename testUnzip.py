from zipfile import ZipFile
from addressArray import array
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
        # address.split(" "[0]) isolates the street number from the current address
        if address.split(" ")[0] == streetNumber:
            matches.append(address)
    if len(matches) == 0:
        print("\nThere are no addresses with this street number")
        retry = input("Enter the street number (enter \"cancel\" to exit): ")

        # recursion
        return returnFullAddress(retry)
    
    # if there is only one match, return it
    elif len(matches) < 2:
        return matches[0]
    else:
        print("\nThere are multiple addresses with this street number: {}".format(matches))
        selector = None

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

        return(matches[selector-1])
            
def returnDateTime(imagePath):
    img = Image.open(imagePath)
    print(img.getexif()[306])
    rawDate = img.getexif()[306]

    # "rawDate.split(":")[1]" outputs the month part of the raw date (e.g. the 07 from 2023:07:13 14:37:25)
    # monthDictionary has these two digit codes as keys to values which are the month names that correspond to these codes
    # e.g. {"02": February}
    Month = monthDictionary[rawDate.split(":")[1]]
    # there has to be a better way to do this
    Day = rawDate.split(" ")[0].split(":")[2]
    Year = rawDate.split(" ")[0].split(":")[0]

    processedDate = "{} {}, {}".format(Month, Day, Year)

    print(processedDate)
    return processedDate


imageAddress = input("input image file path: ")[1:-1]
print(imageAddress)
returnDateTime(imageAddress)
# right click the zip file to be unzipped and select "Copy as path"
# this is what is to be pasted into command prompt when prompted

# the slice [1:-1] gets rid of the quotes around the pasted file path, as the input method
# will add another pair of quotes around what is inputted, making ZipFile unable to read the path

fullAddress = returnFullAddress(input("\n\n\nEnter the street number: "))

# filePath = input("Enter the file path (with quotes): ")[1:-1]

# os.mkdir("./{}".format(address))

# with ZipFile(filePath) as zObject:
#     zObject.extractall(path="./extract output")
    # pastes unzipped folder into the command prompt working directory



print(fullAddress)