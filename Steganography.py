# Steganography project, assigned by:
# Lilach Naor - id: 313588352, Sapir Shemesh - id: 311342794
# Course lecturer - Yakir Menahem
# please install the following libraries: pip install cv2 , numpy , PIL


import numpy as np
import cv2
import random
from PIL import Image


def encode_image():
    image1_name = input("Enter name of the first image: ")
    image2_name = input("Enter name of the second image: ")

    # Image2 is hidden inside image1
    image1 = cv2.imread(image1_name)
    image2 = cv2.imread(image2_name)

    if image2.size[0] > image1.size[0] or image2.size[1] > image2.size[1]:
        raise Exception('Image 2 should be smaller or equal to image1!')

    # The 3 for loops iterate over image1 and image2, convert
    # each pixel of the both images into 8-bit binary representation
    # Then - take the 4 MSB of each binary string, concatenating
    # them, and input the new pixel into image1
    for i in range(image2.shape[0]):
        for j in range(image2.shape[1]):
            for k in range(3):
                binary_image1 = format(image1[i][j][k], '08b')
                binary_image2 = format(image2[i][j][k], '08b')

                new_pixel_binary = binary_image1[:4] + binary_image2[:4]
                image1[i][j][k] = int(new_pixel_binary, 2) # modify the image1's pixels

    new_image_name = input("Enter the name for merged images: ")
    cv2.imwrite(new_image_name, image1)


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
        # Extracting 3 pixels at a time ( 9 RGB value)
        pixels = [j for j in image_data.__next__()[:3] + image_data.__next__()[:3] +
                  image_data.__next__()[:3]]

        # pixels values should be modified - odd for bit 1 and even for bit 0
        # 8 iterations for the first 8 pixels
        for j in range(0, 8):
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
    for pixel in modify_pixels(new_image.getdata(), text):
        # Putting modified pixels in the new image
        new_image.putpixel((x, y), pixel)
        if x == width - 1: # if we are in the last row
            x = 0
            y += 1
        else:
            x += 1


# the function get text and encode it into a new image
def encode_text(text):
    img_name = input("Enter image name(with extension - png only): ")
    image = Image.open(img_name, 'r') # Opening the given image for reading
    image_size = image.size[0] * image.size[1] * 3 # How many pixels the image contains

    # Check if the text is empty
    if len(text) == 0:
        raise ValueError('You entered nothing') # valueError is a specific exception

    # check if the input text is larger than the image's dimensions * pixels
    if len(text) > image_size:
        raise Exception('Enter less data, or bigger image!')

    # Make a copy of the input image, so that the original wouldn't change
    new_image = image.copy()
    # call the new_image_pixels function to modify the image copy
    new_image_pixels(new_image, text)

    new_img_name = input("Enter the name of new image(with extension - png only): ")
    new_image.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    # ^Split the new image name after '.', and save it as the given extension in Upper case


# the function decode hidden text from image
def decode_text():
    img_name = input("Enter image name(with extension - png only): ")
    image = Image.open(img_name, 'r')  # Opening the given image for reading
    password_input = input("Please enter the password: ")

    # hidden text - for appending the chars in the image
    hidden_text = ''
    # img_data became object which we can iterate over it
    img_data = iter(image.getdata())

    while True:
        # extracting 3 pixels at a time ( 9 RGB value)
        pixels = [i for i in img_data.__next__()[:3] + img_data.__next__()[:3] +
                  img_data.__next__()[:3]]

        # string of binary - representation of each char
        binary = ''

        # update the binary string with 0 when the pixel is even and 1 when the pixel is odd.
        for i in pixels[:8]:
            # if the pixel is even ,add 0 bit to the binary string
            if i % 2 == 0:
                binary += '0'
            else:
                binary += '1'

        # convert the binary number to int and then to char and update the hidden text string
        hidden_text += chr(int(binary, 2))

        # check if there is finish to read the hidden text , if yes - we can return the hidden text.
        if pixels[-1] % 2 != 0:
            password = (hidden_text.split('@')[0])  # split the password string from the input
            if password_input == password:
                return hidden_text.split('@')[1] # return the string without the password
            else:
                raise Exception('Incorrect password!') # if the input password different from the encryption password


def main():
    type = int(input("Enter the mode: 1.Text 2.Image: "))

    if type == 1:
        mode_text = int(input("Want to 1. encode / 2. decode: "))

        if mode_text == 1:
            text = input("Please input the password + @ and then the text: ")
            encode_text(text)
        else:
            print("The hidden text is: " + decode_text())

    elif type == 2:
        mode_image = input("Want to 1.encode / 2.decode: ")
        if mode_image == 1:
            encode_image()
        else:
            decode_image()

    else:
        raise Exception("Invalid input!")


# Run the main function of Steganography
if __name__ == "__main__":
    main()