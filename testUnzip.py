from zipfile import ZipFile
from addressArray import array
import os
import sys


def returnFullAddress(streetNumber):
    if streetNumber == "cancel":
        sys.exit("Canceled by user")
    matches = []
    for address in array:
        if address.split(" ")[0] == streetNumber:
            matches.append(address)
    if len(matches) == 0:
        print("There are no addresses with this street number")
        retry = input("Enter the street number (enter cancel to exit): ")

        return returnFullAddress(retry)
    elif len(matches) < 2:
        print(matches[0])
        return matches[0]
    else:
        print("There are multiple addresses with this street number: {}".format(matches))


# right click the zip file to be unzipped and select "Copy as path"
# this is what is to be pasted into command prompt when prompted

# the slice [1:-1] gets rid of the quotes around the pasted file path, as the input method
# will add another pair of quotes around what is inputted, making ZipFile unable to read the path
address = returnFullAddress(input("Enter the street number: "))
# filePath = input("Enter the file path (with quotes): ")[1:-1]

# os.mkdir("./{}".format(address))

# with ZipFile(filePath) as zObject:
#     zObject.extractall(path="./extract output")
    # pastes unzipped folder into the command prompt working directory



print(address)