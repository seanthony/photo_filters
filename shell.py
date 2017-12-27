from core import FilterPhoto, is_file
import os
from time import sleep as zzzz


def welcome():
    zzzz(.2500)
    print("         _[]_/____\\__n_")
    zzzz(.2500)
    print("        |_____.--.__()_|")
    zzzz(.2500)
    print("        |S   //# \\\\    |")
    zzzz(.2500)
    print("        |T   \\\\__//    |")
    zzzz(.2500)
    print("        |A    '--'     |")
    zzzz(.2500)
    print("        '--------------'")
    zzzz(.2500)


def clear_screen():
    if os.name == 'nt':
        os.system('cls')  # windows
    else:
        os.system('clear')  # linux / mac


def sys_exit():
    clear_screen()
    print('thank you for using the software. have a nice day. :)')
    exit()


def get_filename():
    while True:
        filename = input(
            'please enter the filename (with path) of the picture you would like to filter: ').strip()
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


def get_image_file(filename):
    while True:
        try:
            image = FilterPhoto(filename)
            print("'{}' successfully loaded...\n\n".format(filename))
            return image
        except OSError:
            clear_screen()
            print('uh-oh. looks like \'{}\' is not an image file.')
            filename = get_filename()


def get_filter(filter_list):
    num_filters = len(filter_list)
    print('\n'.join(['{}. {}'.format(i, filter_list[i].get('name'))
                     for i in range(1, num_filters)]))
    while True:
        choice = input(
            '\nenter the number filter or choose \'0\' to apply no filter: ').strip().lower()
        if choice == 'q':
            sys_exit()
        elif choice.isnumeric() and int(choice) in range(num_filters):
            return int(choice)
        else:
            print('whoops. \'{}\' is an invalid option.'.format(choice))
            continue


def main():
    clear_screen()
    print('hello world. welcome to sean\'s photo editor.\n')
    welcome()
    print('\nupload a picture of your choice and choose a filter.\nenter "q" to quit.\n')
    filename = get_filename()
    image = get_image_file(filename)
    filter_index = get_filter(image.filters)
    print('Filtering...')
    image.image = image.filters[filter_index].get('filter')()
    image.save()
    image.image.show()


if __name__ == '__main__':
    main()
