from core import FilterPhoto
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
        elif core.is_file(filename):
            return filename
        elif filename == '':
            return 'moto.jpg'
        else:
            clear_screen()
            print(
                "no file with filename '{}' found. please try again.\n".format(filename))


def main():
    clear_screen()
    print('hello world.\n\nwelcome to sean\'s photo editor.\nupload a picture of your choice and apply the filter of your choice.\nenter "q" to quit.\n')
    filename = get_filename()
    try:
        image = FilterPhoto(filename)
    except FileNotFoundError:
        clear_screen()
        print(
            "no file with filename '{}' found. please try again.\n".format(filename))


if __name__ == '__main__':
    main()
