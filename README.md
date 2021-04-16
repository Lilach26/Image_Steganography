# Image Steganography - LSB Encryption Method

Image steganography is the process of hiding data into an image.
In this project, we focused on hiding text within image, and image inside image - using the LSB method for hiding text inside image.

Modules include:
1. Numpy
2. Pillow
3. CV2
4. Random
5. Matplotlib

Limitations:
1. This progam was developed in Python 3.5.
2. This program will ONLY work with PNG images. JPEG images have a specific compression issue that screws with the encryption algorithim.
You can only encrypt a specific amount of characters within an image. The exact amount is based off the size of the image (3 pixels is dedicated to each character).

For more details about the project and the implementation, read the PDF file.
