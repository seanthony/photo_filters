from core import FilterPhoto
import os


def clear_screen():
    os.system('cls')  # windows
    os.system('clear')  # linux / mac


def sys_exit():
    print('thank you for using the software. have a nice day.')
    exit()


def main():
    clear_screen()
    print('hello world.\nwelcome to sean\'s photo editor.\nupload a picture of your choice and apply the filter of your choice.\nenter "q" to quit.')
    while True:
        filename = input(
            'please enter the filename with path of the picture you are filtering: ').strip()
        if filename.lower() == 'q':
            sys_exit()
        elif filename == '':
            image = FilterPhoto('moto.jpg')
            break
        else:
            image = FilterPhoto(filename)


if __name__ == '__main__':
    main()
