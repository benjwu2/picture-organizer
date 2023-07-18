from zipfile import ZipFile
import os
from addressArray import array

# right click the zip file to be unzipped and select "Copy as path"
# this is what is to be pasted into command prompt when prompted

# the slice [1:-1] gets rid of the quotes around the pasted file path, as the input method
# will add another pair of quotes around what is inputted, making ZipFile unable to read the path
# address = input("property address?")
# filePath = input("Enter the file path (with quotes): ")[1:-1]

# os.mkdir("./{}".format(address))

# with ZipFile(filePath) as zObject:
#     zObject.extractall(path="./extract output")
    # pastes unzipped folder into the command prompt working directory



def returnFullAddress(streetNumber):
    matches = []
    for address in array:
        if address.split(" ")[0] == streetNumber:
            matches.append(address)
    if len(matches) == 0:
        print("There are no addresses with this street number")
    elif len(matches) < 2:
        print(matches[0])
        return matches[0]
    else:
        print("There are multiple addresses with this street number: {}".format(matches))