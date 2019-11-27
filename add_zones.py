import subprocess


def add_zone():
    filename = input('Filename to append the zone: ')
    create_adverse(filename)


def create_adverse(filename):
    domain = input('domain name: ')
    type_ = input('type [master|slave]: ')
    notify = input('slave to notify (ip): ')
    file_zone = input('path with filename of the forward zone: ')
    file_zone_reverse = input('path with filename of the reverse zone: ')
    inverse_domain = input('enter your inverse domain: ')
    write_zones(filename, domain, file_zone, type_, notify)
    write_zones(filename, domain, file_zone_reverse, type_, notify, inverse_domain)
    records = input_records()
    create_forward_or_reverse_file(file_zone, domain, records)
    create_forward_or_reverse_file(file_zone_reverse, domain, records, reverse=True)
    print('\n\nYour zones were added succesfully!\n')


def input_records():
    value = input('Would wou like to write new DNS Record y/n: ')
    write_ip = True if value == 'y' else False
    list_records = []
    while write_ip:
        new_domain = input('name of domain: ')
        ip = input('ip: ')
        list_records.append(dict(new_domain=new_domain, ip=ip))
        value = input('Would wou like to write new DNS Record y/n: ')
        write_ip = True if value == 'y' else False
    return list_records


def write_zones(filename, domain, file_zone, type_, notify, inverse_domain=None):
    with open(filename, 'a+') as file:
        if inverse_domain:
            file.write('\nzone "{}.in-addr.arpa" in {{ \n'.format(inverse_domain))
        else:
            file.write('\n\nzone "{}" in {{ \n'.format(domain))
        file.write('\ttype {};\n'.format(type_))
        file.write('\tfile "{}";\n'.format(file_zone))
        file.write('\tallow-transfer { key master; };\n')
        file.write('\tallow-query { any; };\n')
        file.write('\talso-notify {{ {}; }};\n'.format(notify))
        file.write('\tnotify yes;\n')
        file.write('};\n')


def create_forward_or_reverse_file(file_zone, domain, records, reverse=None):
    with open(file_zone, 'a+') as file:
        file.write('$TTL 604800\n')
        file.write('@	IN	SOA	pri.{}. root.{}. (\n'.format(domain, domain))
        file.write('\t\t1 ; Serial\n')
        file.write('\t\t604800 ; Refresh\n')
        file.write('\t\t86400 ; Retry\n')
        file.write('\t\t2419200	; Expire\n')
        file.write('\t\t 604800 ) ; Minimum TTL\n')
        file.write(';\n')
        if reverse:
            file.write('@\t\tIN\tNS\t\tlocalhost.\n')
            for record in records:
                file.write('{}\t\tIN\tPTR\t\t{}\n'.format(record['ip'].split('.')[-1], record['new_domain']))
        else:
            file.write('@\t\tIN\tNS\t\tpri.{}.\n'.format(domain))
            file.write('pri\t\tIN\tA\t\t127.0.0.1\n')
            for record in records:
                file.write('{}\t\tIN\tA\t\t{}\n'.format(record['new_domain'], record['ip']))


def reload_bind():
    res = subprocess.check_output(["/etc/init.d/bind9", "reload"])
    for line in res.splitlines():
        print(line, '********')
