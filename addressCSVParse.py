fileAddress = input("enter the file path for the CSV file to be parsed (with quotes): ")[1:-1]

# Takes the CSV file whose file path is inputted and converts
# it into an array written out in a newly created Python file
with open("addressArray.py", 'w') as AA:
    with open(fileAddress) as file:

        # convert the file contents into a string
        contents = file.read()

        # splits the file string into array elements on line breaks
        # since each entry is on a separate line in the string
        addressArray = contents.split("\n")

        # writes this array into the addressArray.py file
        AA.write("{}".format(addressArray))
