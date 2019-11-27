import os


def remove_zone_from_file(zone, file_name):
    print(zone)
    with open(file_name, 'r') as file:
        lines = file.readlines()
    with open(file_name, 'w') as file:
        for index, line in enumerate(lines):
            if index < zone['begin'] or index > zone['end']:
                file.write(line)

    os.remove(zone['file'])
    print('\n\nYour zone have been removed!\n')
