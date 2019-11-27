from add_domain import add_domain
from add_zones import add_zone, reload_bind
from read_zones import read_zones, print_zones
from remove_domain import remove_domain
from remove_zones import remove_zone_from_file


def read_file():
    forward_zones = []
    reverse_zones = []
    file_name = input('Enter absolute path where you wrote your zones: ')
    read_zones(file_name, forward_zones, reverse_zones)
    if forward_zones:
        print('Your Zones:')
        print_zones(forward_zones, 1)
        print()
    if reverse_zones:
        print('Inverse zones:')
        print_zones(reverse_zones, 2)
        print()

    return forward_zones, reverse_zones, file_name


def remove_zone():
    forward_zones, reverse_zones, file_name = read_file()
    option = input('Enter options of zone you want to remove, example: 1 1 (1-Anverse 1-#Number zone to remove): ')
    option = option.split()
    type_zone = int(option[0])
    number = int(option[1])
    if type_zone == 1:
        remove_zone_from_file(forward_zones[number - 1], file_name)
    else:
        remove_zone_from_file(reverse_zones[number - 1], file_name)


if __name__ == '__main__':
    loop = True
    while loop:
        print('\n\n****DNS reader****')
        print('1.- Read config files')
        print('2.- Add zone')
        print('3.- Remove zone')
        print('4.- Add domains')
        print('5.- Remove Domain')
        print('6.- Update Service')
        print('7.- exit')
        opt = int(input())
        loop = True if opt != 7 else False
        if opt == 1:
            read_file()
        elif opt == 2:
            add_zone()
        elif opt == 3:
            remove_zone()
        elif opt == 4:
            add_domain()
        elif opt == 5:
            remove_domain()
        elif opt == 6:
            reload_bind()
