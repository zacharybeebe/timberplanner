
hiddenimports = []
with open('_imports_.py', 'r') as f:
    look_line = False
    mod = None
    for line in f.readlines():
        if line[:6] == 'import':
            hiddenimports.append(f"'{line[7:-1]}'")
        elif line[:4] == 'from':
            mod_bucket = []
            for i in line[5:]:
                if i == ' ':
                    break
                else:
                    mod_bucket.append(i)
            mod = ''.join(mod_bucket)
            if '(' not in line:
                sub_bucket = []
                for i in reversed(line):
                    if i == ' ':
                        break
                    else:
                        if i.isalnum() or i == '_':
                            sub_bucket.append(i)
                sub = ''.join([i for i in reversed(sub_bucket)])
                hiddenimports.append(f"'{mod}.{sub}'")
        else:
            if ')' not in line:
                sub_bucket = [i for i in line if i.isalnum() or i == '_']
                if sub_bucket:
                    sub = ''.join(sub_bucket)
                    hiddenimports.append(f"'{mod}.{sub}'")

with open('hook-data.py', 'w') as h:
    h.write('hiddenimports = [\n')
    for i in hiddenimports:
        h.write(f'\t{i},\n')
    h.write(']')

print('COMPLETED TRANSFERRING IMPORTS TO hook-data.py')
