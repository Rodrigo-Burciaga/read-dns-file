import linecache

from read_files_zones import read_forward_or_reverse


def check_type(line, zone):
    if 'type' in line:
        zone['type'] = line[1].split(';')[0]


def check_file(line, zone):
    if 'file' in line:
        file_ = line[1].split(';')[0]
        zone['file'] = file_[1:-1]


def check_notify(line, zone):
    if 'also-notify' in line:
        zone['notify'] = line[2].split(';')[0]


def check_allow_transfer(line, zone):
    if 'allow-transfer' in line:
        zone['allow-transfer'] = '{} {}'.format(line[2], line[3].split(';')[0])


def check_forward_zone(list_line, index, filename, forward_zones):
    if 'zone' in list_line[0] and 'in-addr.arpa' not in list_line[1]:
        zone_dict = create_zone(index, filename)
        zone_dict['main_domain'] = list_line[1][1:-1]
        forward_zones.append(zone_dict)


def check_reverse_zone(list_line, index, filename, reverse_zones):
    if 'zone' in list_line[0] and 'in-addr.arpa' in list_line[1]:
        zone_dict = create_zone(index, filename)
        zone_dict['main_domain'] = list_line[1][1:-1]
        reverse_zones.append(zone_dict)


def create_zone(index, filename):
    zone = dict()
    inner_index = index + 1
    zone['begin'] = index
    line_to_check = linecache.getline(filename, inner_index).lstrip().split()
    while line_to_check[0] != '};':
        check_type(line_to_check, zone)
        check_file(line_to_check, zone)
        check_notify(line_to_check, zone)
        check_allow_transfer(line_to_check, zone)
        inner_index += 1
        line_to_check = linecache.getline(filename, inner_index).lstrip().split()
    zone['end'] = inner_index - 1
    return zone


def print_zones(zones, case_zone):
    for i, zone in enumerate(zones):
        print('{}.- {} \n\t tipo: {}, archivo de configuracion: {}, ip esclavo: {}, allow-transfer: {}'.format(
            i + 1, zone['main_domain'], zone['type'], zone['file'], zone['notify'], zone['allow-transfer']
        ))
        print_file_ip_domain(zone['file'], case_zone, zone['main_domain'])


def print_file_ip_domain(file_zone, case_zone, main_domain):
    config_file = read_forward_or_reverse(file_zone, case_zone)
    # print('\t {}'.format(config_file))
    print('\t ttl: {}'.format(config_file['ttl']))
    if case_zone == 1:
        print('\t Dominios: ')
        for domain in config_file['domains']:
            print('\t\t {}.{} -----> {}'.format(domain['domain'], main_domain, domain['ip']))
    else:
        print('\t Ips:')
        for ip in config_file['ips']:
            print('\t\t {}.{} -----> {}'.format(ip['last_segment'], main_domain, ip['domain']))


def read_zones(file_name, forward_zones, reverse_zones):
    with open(file_name, 'r') as file:
        for index, line in enumerate(file):
            list_line = line.lstrip().split()
            if list_line:
                check_forward_zone(list_line, index, file_name, forward_zones)
                check_reverse_zone(list_line, index, file_name, reverse_zones)
