def add_domain():
    file_name = input('Enter your filename of forward or reverse zone: ')
    opt = int(input('Type 1.- Anverse 2.- Reverse: '))
    if opt == 1:
        domain = input('Enter domain: ')
        ip = input('Enter ip: ')
        with open(file_name, 'a+') as file:
            file.write('\n{}\t\tIN\tA\t\t{}\n'.format(domain, ip))
    else:
        segment = input('Enter last segment ip: ')
        domain = input('Enter full domain: ')
        with open(file_name, 'a+') as file:
            file.write('{}\t\tIN\tPTR\t\t{}\n'.format(segment, domain))
