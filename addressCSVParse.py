fileAddress = input("enter the file path for the CSV file to be parsed (with quotes): ")[1:-1]

# return one plus the number of times an array that has a name starting
# with "array" is used in addressArray.py
def getArrayNum():
    with open("addressArray.py") as file:
        contents = file.read()

        # if the file is blank, then the array should just be called "array" with no added number
        if contents == "": return ""
        
        # the number of times "array" appears in the file is equal to the number
        # of elements in the array made of the string split on "array," minus 1
        return len(contents.split("array"))


# returns the name inputted by the user or a default one
# based on how many arrays with a name starting with "array" there area in adressArray.py
# The default name is generated if the user skips the naming by pressing enter
def getArrayName():    
    if input("Name for new array? (press Enter to skip): ") == "":
        return "array{}".format(getArrayNum())



# Takes the CSV file whose file path is inputted and converts
# it into an array written out in a newly created Python file
with open("addressArray.py", 'a') as AA:
    AA.write("{} = ".format(getArrayName()))
    with open(fileAddress) as file:

        # convert the file contents into a string
        contents = file.read()

        # splits the file string into array elements on line breaks
        # since each entry is on a separate line in the string
        addressArray = contents.split("\n")

        # writes this array into the addressArray.py file
        AA.write("{}\n".format(addressArray))
