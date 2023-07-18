from zipfile import ZipFile
import os


# right click the zip file to be unzipped and select "Copy as path"
# this is what is to be pasted into command prompt when prompted

# the slice [1:-1] gets rid of the quotes around the pasted file path, as the input method
# will add another pair of quotes around what is inputted, making ZipFile unable to read the path
address = input("property address?")
filePath = input("Enter the file path: ")[1:-1]

os.mkdir("./{}".format(address))

with ZipFile(filePath) as zObject:
    zObject.extractall(path="./extract output")
    # pastes unzipped folder into the command prompt working directory