# description

The objective of this project is to be able to take downloaded pictures of the real estate properties, which will come in a zip folder, and extract them into a folder which is named appropriately for uploading to Synology. The folder will be named with the address that the pictures were taken at and the date that the pictures were taken, in a format that is to be determined.

# TO-DO

- [ ] Make Python look at one of the picture files in the extracted folder to get the date

# methods

This project is coded in Python

## modules and techniques list

1. [[zipfile module]]
2. [[os module]]
3. [[sys module]]
4. [[PIL module]]
5. [[recursion]]

## making a folder

This is done using the [[os module]], specifically the [[os.mkdir method]]

## extracting files

This is done with the [[zipfile module]]

## determining address

The address will be determined using an [[input method]] prompt asking the user to input the numerical portion of the address. This is both for efficiency and because the pictures will not come with the full address: an image of the mailbox with the numerical part of the address is the only way to identify what property is shown in a set of images.

### returning address based on user input

A function then searches an [[#setting up the address array|array of addresses]] for an address with a matching numerical portion to the one inputted will return such an address. If there are multiple addresses with the same numerical portions, the user will be asked to select the correct address using another [[input method]].

## setting up the address array

This is done using the built-in file [[write() method]] and [[open function|open() function]].
First, a spreadsheet of addresses will be converted into a [[csv]] file. Then, line by line, the contents of the file will be added into a Python array on a separate file using the [[write() method]].

This file will be created using the [[open function|open() function]].

This code was made without my having to look up any online documentation.

# future improvements

## automated download of files

A future iteration could possibly figure out which pictures belong in a group and download them using the [[PyDrive module]] [Uploading files on Google Drive using Python - GeeksforGeeks](https://www.geeksforgeeks.org/uploading-files-on-google-drive-using-python/)

## automated upload of folder to [[Synology]]

## automatically parse picture metadata to determine the date that should be used in the folder name

## find a better way of parsing the raw date metadata into a written out date than using the [[split() method|split method]] a billion times

i.e. from something like `2023:07:13 14:37:25` to `July 13, 2023`

# Challenges

One thing that confounds me is when I paste in a string containing a file path as an argument for a function call for usage by Image.open() or some other method, I get the following error:

```md
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
```

But when I paste in the same address as the input for the [[input method]], like this:

```Python
imageAddress = input("input image file path: ")[1:-1]
```

And use the stored input in the same way, I don't get an error

# New techniques

First usage of the [[sys module]]
