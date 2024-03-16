import sys

# patch /usr/src/mytonctrl/mypylib/mypylib.py
def patch_mypylib_timestamp(service_path):
    with open(service_path, 'r') as f:
        code = f.read()

    lines = code.split('\n')

    new_lines = []
    for idx, line in enumerate(lines):
        new_line = line
        if line == '	startTimestampMonotonic = int(startTimestampMonotonic) / 10**6':
            new_line = '	startTimestampMonotonic = int(startTimestampMonotonic) / 10**6 if startTimestampMonotonic is not None else 0'
        new_lines.append(new_line)

    new_code = '\n'.join(new_lines)
    with open(service_path, 'w') as f:
        f.write(new_code)

# patch /usr/src/mytonctrl/mypylib/mypylib.py
def patch_mypylib_network(service_path):
    with open(service_path, 'r') as f:
        code = f.read()

    lines = code.split('\n')

    new_lines = []
    skipping = False
    for idx, line in enumerate(lines):
        new_line = line
        if line.startswith('def GetInternetInterfaceName():'):
            new_lines.append(line)
            new_lines.append('\treturn "eth0"')
            skipping = True

        if line.startswith('#end define'):
            skipping = False
        if not skipping:
            new_lines.append(new_line)

    new_code = '\n'.join(new_lines)
    with open(service_path, 'w') as f:
        f.write(new_code)

# patch /etc/systemd/system/validator.service
def patch_validator(service_path):
    with open(service_path, 'r') as f:
        code = f.read()

    lines = code.split('\n')

    new_lines = []
    for idx, line in enumerate(lines):
        new_line = line
        
        if line.startswith('User ='):
            new_line = 'User = root'
        if line.startswith('Group ='):
            new_line = 'Group = root'
        if line.startswith('ExecStart ='):
            new_line = 'ExecStart = /usr/bin/ton/validator-engine/validator-engine --threads 3 --daemonize --global-config /usr/bin/ton/global.config.json --db /var/ton-work/db/ --logname /var/ton-work/log --state-ttl 604800 --verbosity 3'

        new_lines.append(new_line)

    new_code = '\n'.join(new_lines)
    with open(service_path, 'w') as f:
        f.write(new_code)

def main():
    patch_validator('/etc/systemd/system/validator.service')
    patch_mypylib_network('/usr/src/mytonctrl/mypylib/mypylib.py')
    patch_mypylib_timestamp('/usr/src/mytonctrl/mypylib/mypylib.py')

if __name__ == "__main__":
    sys.exit(main())