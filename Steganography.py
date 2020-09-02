import numpy as np
import cv2
import random
from PIL import Image


def convert_int_2binary(text):
    binary = [format(ord(value), '08b') for value in text]
    return binary


def main():
    type = input("Enter the mode: 1.Text 2.Image: ")

    if type == 1:
        modeText = input("Want to 1. encode / 2. decode: ")

        if modeText == 1:
            text = input("Please input the text you want to encode: ")
            encode()
        else:
            print("The hidden text is: " + decode())
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