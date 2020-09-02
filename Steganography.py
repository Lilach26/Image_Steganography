# Steganography project, assigned by:
# Lilach Naor - id: 313588352, Sapir Shemesh - id: 311342794
# Course lecturer - Yakir Menahem


import numpy as np
import cv2
import random
from PIL import Image


# The function will get string and convert it to ASCII and then to 8-bit binary list.
def convert_int_2binary(text):
    binary = [format(ord(value), '08b') for value in text]
    return binary


# The function will get pixels and modify those according to the algorithm describes
def modify_pixels(pixels, text):
    # variable declaration
    binary_list = convert_int_2binary(text)
    length_text = len(binary_list)
    image_data = iter(pixels)

    # Iterate over the list of binary representation for the text
    for i in range(length_text):
        # Extracting 3 pixels at a time
        pixels - [j for j in image_data.__next__()[:3] + image_data.__next__()[:3] +
                  image_data.__next__()[:3]]

        # pixels values should be modified - odd for bit 1 and even for bit 0
        # 8 iterations for the first 8 pixels
        for j in range(0 , 8):
            if binary_list[i][j] == '0' and pixels[j] % 2 != 0:
                pixels[j] -= 1

            elif binary_list[i][j] == '1' and pixels[j] % 2 == 0:
                # check if the pixel is not 0 to prevent exceed from the range
                if pixels[j] != 0:
                    pixels[j] -= 1
                else:
                    pixels[j] +=1

        # in the last pixels we will check if there are more data to read
        # 0 - if there any message to read or 1 - if no.
        if i == length_text - 1:
            if pixels[-1] % 2 == 0:
                # check if the pixel is not 0 to prevent exceed from the range
                if pixels[-1] != 0:
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1

        # else - there is another data to read
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        # change the pixels to tuple to protect from changes
        pixels = tuple(pixels)
        # yield for treat separate in every section
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


# The function gets a copy of original image, then changes the pixels
# with the modify_pixels function above
def new_image_pixels(new_image, text):
    width = new_image.size[0] # image.size returns image width, height and color
    (x, y) = (0, 0) # x=0 rows, y=0 column

    # the for loop run in the pixels section of the new image
    for pixel in modify_pixels(new_image.getData(), text):
        # Putting modified pixels in the new image
        new_image.putpixel((x, y), pixel)
        if x == width - 1: # if we are in the last row
            x = 0
            y += 1
        else:
            x += 1


def encode_text(text):
    img_name = input("Enter image name(with extension - png only): ")
    image = Image.open(img_name, 'r') # Opening the given image for reading

    # Check if the text is empty
    if len(text) == 0:
        raise ValueError('You entered nothing') # valueError is a specific exception

    # Make a copy of the input image, so that the original wouldn't change
    new_image = image.copy()
    # call the new_image_pixels function to modify the image copy
    new_image_pixels(new_image, text)

    new_img_name = input("Enter the name of new image(with extension - png only): ")
    new_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    # ^Split the new image name after '.', and save it as the given extension in Upper case


def main():
    type = input("Enter the mode: 1.Text 2.Image: ")

    if type == 1:
        modeText = input("Want to 1. encode / 2. decode: ")

        if modeText == 1:
            text = input("Please input the text you want to encode: ")
            encode_text(text)
        else:
            print("The hidden text is: " + decode_text())

    elif type == 2:
        modeImage = input("Want to 1.encode / 2.decode: ")
        if modeImage == 1:
            encode_image()
        else:
            decode_image()

    else:
        raise Exception("Invalid input!")


# Run the main function of Steganography
if __name__ == "__main__":
    main()