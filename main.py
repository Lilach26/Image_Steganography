import Steganography as stegano


def main():
    print("Welcome to the Image Steganography project!")
    print("We hope you'll enjoy it and feel like a secret agent for a while!\nSo, let's get started:\n")
    mode_text = int(input("What kind of action would you like to do?  1. encode / 2. decode: "))

    if mode_text == 1:
        choice = int(input("Enter the mode: 1.Text 2.Image: "))

        if choice == 1:
            password = input("Please enter the password: ")
            text = input("Please input the text you want to hide: ")
            data = password + '@' + text
            stegano.encode_text(data)
        else:
            stegano.encode_image()

    elif mode_text == 2:
        choice = int(input("Enter the mode: 1.Text 2.Image: "))

        if choice == 1:
            print("The hidden text is: " + stegano.decode_text())
        else:
            stegano.decode_image()

    else:
        raise Exception("Invalid input!")


# Run the main function of program
if __name__ == "__main__":
    main()
