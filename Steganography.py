import numpy as np
import cv2
import random
from PIL import Image


# the function will get string and convert it to ASCII and than to binary in 8 bits.
def convert_int_2binary(text):
    binary = [format(ord(value), '08b') for value in text]
    return binary


# the function will get pixels and modify those according to the algorithm
def modify_pixels(pixels , text):
    binary_list = convert_int_2binary(text)
    length_text = len(binary_list)
    image_data = iter(pixels)

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
        # there is another data to read
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        # change the pixels to tuple to protect from changes
        pixels = tuple(pixels)
        # yield for treat separate in every section
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]



def main():
    type = input("Enter the mode: 1.Text 2.Image: ")

    if type == 1:
        modeText = input("Want to 1. encode / 2. decode: ")

        if modeText == 1:
            text = input("Please input the text you want to encode: ")
            encodeText()
        else:
            print("The hidden text is: " + decodeText())
    elif type == 2:
        modeImage = input("Want to 1.encode / 2.decode: ")
        if modeImage == 1:
            encodeImage()
        else:
            decodeImage()

    else:
        raise Exception("Invalid input!")


if __name__ == "__main__":
    main()