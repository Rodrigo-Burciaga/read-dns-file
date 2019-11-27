def find_ttl(list_line, config_file):
    if list_line:
        if '$TTL' in list_line[0]:
            config_file['ttl'] = list_line[1]


def find_domains_or_ips(list_line, case, list_ips, list_domains):
    if list_line:
        if ';' not in list_line[0] and 'IN' in list_line and list_line[-1] != '(' and list_line[0] != '@':
            if case == 1:
                domain = dict(domain=list_line[0], ip=list_line[-1])
                list_domains.append(domain)
            else:
                ip = dict(last_segment=list_line[0], domain=list_line[-1])
                list_ips.append(ip)


def read_forward_or_reverse(filename, case):
    config_file = dict()
    list_domains = []
    list_ips = []
    with open(filename, 'r') as file:
        for line in file:
            list_line = line.split()
            find_ttl(list_line, config_file)
            find_domains_or_ips(list_line, case, list_ips, list_domains)
    if list_domains:
        config_file['domains'] = list_domains
    if list_ips:
        config_file['ips'] = list_ips

    return config_file
