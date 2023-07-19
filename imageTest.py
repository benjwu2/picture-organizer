from PIL import Image
from PIL.ExifTags import TAGS

img = Image.open("C:/Users/benjw/Downloads/PXL_20230713_183725567.jpg")

# creates a dictionary of tags and their respective values for the opened image
metadata = {}
for tag, value in img.getexif().items():
    if tag in TAGS:
        metadata[TAGS[tag]] = value

print(img.getexif())

# TAGS is a dictionary of image metadata tags and their numerical ids, with the 
# ids being the key and the tags being the value of the dictionary

# the full list of tags and their respective number ids
print(TAGS)

# img.exif() is a dictionary of metadata number ids and the value of the associated metadata tag
# e.g. Modelkey: Pixel 4a

for key in img.getexif():
    print('tag: {}\n'.format(TAGS[key] + "key: {}".format(key)))

# prints the tag followed by the value of the image
for key in img.getexif():
    print('tag: {}\n'.format(TAGS[key] + "key: {}".format(img.getexif()[key])))
