def remove_domain():
    file_name = input('Enter reverse or forward filename: ')
    with open(file_name, 'r') as file:
        lines = file.readlines()
        list_domains = []
        for index, line in enumerate(lines):
            check_line = line.split()
            if check_line and 'IN' in check_line and '@' not in check_line:
                list_domains.append(dict(index=index, ip=check_line[-1], domain=check_line[0]))
    if list_domains:
        for index, domain in enumerate(list_domains):
            print('{}.- {} -------- {} '.format(index + 1, domain['domain'], domain['ip']))
    number = int(input('Enter number of domain to delete: '))
    with open(file_name, 'w') as file:
        for index, line in enumerate(lines):
            if list_domains[number - 1]['index'] != index:
                file.write(line)
