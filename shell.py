from core import FilterPhoto, is_file
import os


def clear_screen():
    if os.name == 'nt':
        os.system('cls')  # windows
    else:
        os.system('clear')  # linux / mac


def sys_exit():
    clear_screen()
    print('thank you for using the software. have a nice day.')
    exit()


def get_filename():
    while True:
        filename = input(
            'please enter the filename with path of the picture you are filtering: ').strip()
        if filename.lower() == 'q':
            sys_exit()
        elif is_file(filename):
            return filename
        elif filename == '':
            return 'moto.jpg'
        else:
            clear_screen()
            print(
                "oops! no file with filename '{}' found. please try again.\n".format(filename))


def check_image_file(filename):
    while True:
        try:
            return FilterPhoto(filename)
        except OSError:
            clear_screen()
            print('uh-oh. looks like \'{}\' is not an image file.')
            filename = get_filename()


def main():
    clear_screen()
    print('hello world.\n\nwelcome to sean\'s photo editor.\nupload a picture of your choice and apply the filter of your choice.\nenter "q" to quit.\n')
    filename = get_filename()
    image = check_image_file(filename)


if __name__ == '__main__':
    main()
