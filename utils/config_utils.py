from imports._imports_ import (
    datetime,
    date,
    mkdir,
    join,
    isdir,
    isfile
)


def check_make_directory(base_directory):
    today = date.today()
    sub_dir = f'PROGRAM_EXPORTS'
    sub = join(base_directory, sub_dir)
    if not isdir(sub):
        mkdir(sub)

    today_dir = f'{today.month}_{today.day}_{today.year}'
    full = join(sub, today_dir)
    if not isdir(full):
        mkdir(full)
    return full


def check_make_backup_directory(base_directory):
    sub_dir = 'backups'
    sub = join(base_directory, sub_dir)
    if not isdir(sub):
        mkdir(sub)
    return sub


def get_blank_sheet_filename(directory):
    base = f'blank_RFRS_sheet'
    return _check_file_name(base, directory, '.xlsx')


def get_stand_pdf_filename(stand, directory):
    base = f'stand_report_{stand.name}'
    return _check_file_name(base, directory, '.pdf')


def get_thin_pdf_filename(thin, directory):
    name = thin.stand.name
    trg = int(thin.target)
    trg_m = thin.target_metric
    base = f'thin_report_{name}_{trg}_{trg_m}'
    return _check_file_name(base, directory, '.pdf')


def get_fvs_filename(ext):
    show = {
        '.accdb': 'accessDB',
        '.xlsx': 'excelDB',
        '.db': 'sqliteDB'
    }
    base = f'{show[ext]}_FVS{ext}'
    return base


def get_fvs_monster_name(directory):
    base = 'FVS_Thinning_Run_Summary'
    return _check_file_name(base, directory, '.pdf')


def _check_file_name(base, directory, ext):
    filename = f'{base}{ext}'
    count = 1
    while True:
        if not isfile(join(directory, filename)):
            break
        else:
            filename = f'{base}_{count}{ext}'
            count += 1
    return filename


def _add_date_zeros(val):
    return f"""{'0' * (2 - len(str(val)))}{val}"""


def f_date(dt):
    y = dt.year
    m = _add_date_zeros(dt.month)
    d = _add_date_zeros(dt.day)
    return f'{m}/{d}/{y}'


def h_date(dt):
    y = dt.year
    m = _add_date_zeros(dt.month)
    d = _add_date_zeros(dt.day)
    return f'{y}-{m}-{d}'


def get_fy(month, year):
    m = int(month)
    y = int(year)
    keep_year = [1, 2, 3, 4, 5, 6]
    if m in keep_year:
        return y
    else:
        return y + 1


def back_date(val):
    return datetime(*[int(i) for i in val.split('-')])


def f_price(value):
    if isinstance(value, str):
        value = float(value)
    else:
        value = value
    val_list = [i for i in str(round(value, 2))]
    if '.' not in val_list:
        add_to = ['.', '0', '0']
        for i in add_to:
            val_list.append(i)
    else:
        if len(val_list[-(len(val_list) - val_list.index('.')):]) < 3:
            val_list.append('0')
    temp = [i for i in reversed(val_list)]
    added = 0
    for i in range(3, len(val_list)):
        if i != 3 and i % 3 == 0:
            temp.insert(i + added, ',')
            added += 1
    return f"""${''.join([i for i in reversed(temp)])}"""


def f_round(value):
    str_list = [i for i in str(round(float(value), 1))]
    if len(str_list) <= 5:
        return ''.join(str_list)
    else:
        temp = [0]
        temp += [i for i in reversed(str_list)]
        added = 0
        for i in range(2, len(temp)):
            if i != 3 and i % 3 == 0:
                temp.insert(i + added, ',')
                added += 1
        temp.pop(0)
        return ''.join([i for i in reversed(temp)])


def f_round_or_blank(value):
    if int(value) == 0:
        return '-'
    else:
        str_list = [i for i in str(round(float(value), 1))]
        if len(str_list) <= 5:
            return ''.join(str_list)
        else:
            temp = [0]
            temp += [i for i in reversed(str_list)]
            added = 0
            for i in range(2, len(temp)):
                if i != 3 and i % 3 == 0:
                    temp.insert(i + added, ',')
                    added += 1
            temp.pop(0)
            return ''.join([i for i in reversed(temp)])


def f_pct(value):
    if value <= 1:
        return f'{round(value * 100, 1)} %'
    else:
        return f'{round(value, 1)} %'


def f_bool(value):
    if bool(int(value)):
        return 'Yes'
    else:
        return 'No'


def back_bool(value):
    if value.upper() == 'YES':
        return 1
    else:
        return 0


def is_err_check_stand_for_special_char_or_space(val, col_name=None, row=None, rfrs_stands=None):
    if rfrs_stands is not None:
        stand_names = [stand.stand for stand in rfrs_stands]
        if val.upper() in stand_names:
            return True, val.upper(), f'Stand {val.upper()} is already in database, please change name or append data to stand'
    if val == '':
        return True, val.upper(), f'{col_name.upper()} row {row} cannot be blank'
    elif ' ' in val:
        return True, val.upper(), f'Stand {val.upper()} cannot contain spaces'
    elif any([not c.isalnum() for c in val]):
        return True, val.upper(), f'Stand {val.upper()} cannot contain special characters'
    else:
        return False, val.upper(), None


def is_err_check_int_required(val, col_name=None, row=None, x=None):
    if val == '':
        return True, val, f'{col_name.upper()} row {row} cannot be blank'
    try:
        x = int(val)
        if x < 0:
            return True, x, f'{col_name.upper()} row {row} cannot be negative ({x})'
        else:
            return False, x, None
    except ValueError:
        return True, val, f'{col_name.upper()} row {row} must be a number ({val})'


def is_err_check_float_required(val, col_name=None, row=None, x=None):
    if val == '':
        return True, val, f'{col_name.upper()} row {row} cannot be blank'
    try:
        x = float(val)
        if x < 0:
            return True, x, f'{col_name.upper()} row {row} cannot be negative ({x})'
        else:
            return False, x, None
    except ValueError:
        return True, val, f'{col_name.upper()} row {row} must be a number ({val})'


def is_err_check_float_required_okaynegative(val, col_name=None, row=None, x=None):
    if val == '':
        return True, val, f'{col_name.upper()} row {row} cannot be blank'
    try:
        x = float(val)
        return False, x, None
    except ValueError:
        return True, val, f'{col_name.upper()} row {row} must be a number ({val})'


def is_err_check_float_notrequired(val, col_name=None, row=None, x=None):
    if val == '':
        return False, val, None
    try:
        x = float(val)
        if x < 0:
            return True, x, f'{col_name.upper()} row {row} cannot be negative ({x})'
        else:
            return False, x, None
    except ValueError:
        return True, val, f'{col_name.upper()} row {row} must be a number ({val})'


def is_err_fvs_int_required(val, key, stand, x=None):
    if val == '':
        return True, val, f'{stand} {key} cannot be blank'
    try:
        x = int(val)
        if x < 0:
            return True, x, f'{stand} {key} cannot be negative ({x})'
        else:
            return False, x, None
    except ValueError:
        return True, val, f'{stand} {key} must be a number ({val})'