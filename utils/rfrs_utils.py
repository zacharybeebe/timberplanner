from imports._imports_ import (
    math,
    join,
    mean,
    iterdecode,
    Workbook,
    load_workbook,
    get_column_letter,
    open_workbook,
    reader,
    excel,
    deepcopy,
    ThinTPA,
    ThinBA,
    ThinRD,
    FVS,
    TargetDensityError
)
from config import (
    RFRS_ALL_SPECIES_NAMES,
    RFRS_SHEET_HEADER,
    RFRS_DNR_HEADS,
    RFRS_FVS_HEADS,
    RFRS_ERROR_HOLDER,
    RFRS_ERR_CHECK,
    FVS_ERR_CHECK,
    FVS_SHEETS,
    FVS_SHEET_PARAMS,
    check_make_directory,
    get_fvs_filename
)
from models.rfrs_stand import RfrsStand
from models.rfrs_table import RfrsTable
from utils.html_utils import *


def export_blank_RFRS_sheet(filename):
    wb = Workbook()
    ws = wb.active
    ws.title = 'RFRS Template'
    for i, met in enumerate(RFRS_SHEET_HEADER, 1):
        ws.column_dimensions[get_column_letter(i)].width = 18
        ws.cell(1, i, met)
    wb.save(filename)


def get_table_from_sheet(file, from_dnr=False):
    if from_dnr:
        try:
            data = _read_dnr(file)
        except ValueError:
            return True, None, None, 'Error with imported sheet, did you import a regular sheet from the DNR cruise sheet button?'
    else:
        if file.filename[-4:] == '.csv':
            data = _read_csv(file)
        else:
            data = _read_excel(file)
    try:
        error, table = _convert_sheet_to_table(data)
        if error:
            return error, None, None, 'Imported Sheet Stand Name(s) contain spaces or special characters, please modify the Stand Name(s) and re-import'
        else:
            return error, table, _get_added_stands(data), None
    except IndexError:
        return True, None, None, 'Error with imported sheet, did you import a DNR Cruise sheet from the regular add sheet button?'


def get_table_from_previous_stand(stand):
    master = []
    for i, row in enumerate(stand.table_data):
        temp = []
        for j, col in enumerate(row):
            holder = deepcopy(RFRS_ERROR_HOLDER)
            holder['name_id'] = f'rfrs_{RFRS_SHEET_HEADER[j]}_{i + 1}'
            if col is None:
                holder['val'] = ''
            else:
                holder['val'] = col
            temp.append(holder)
        master.append(temp)
    return master


def _read_csv(file):
    master = []
    convert = iterdecode(file.stream, 'utf-8')
    read = reader(convert, dialect=excel)
    next(read)
    for row in read:
        if row:
            temp = []
            for col in row:
                if col == '':
                    temp.append(None)
                else:
                    temp.append(col)
            master.append(temp)
    return master


def _read_excel(file):
    wb = load_workbook(file, data_only=True)
    ws = wb.active
    master = []
    for row in ws.iter_rows(min_row=2):
        temp = []
        for col in row:
            temp.append(col.value)
        master.append(temp)
    return master


def _read_dnr(file):
    wb = load_workbook(file, data_only=True)
    ws = wb.active
    master = []

    heads = [i.value.upper() for i in ws[1] if i.value]
    indexes = [heads.index(i) for i in RFRS_DNR_HEADS]

    for row in ws.iter_rows(min_row=2):
        temp = []
        for idx in indexes:
            if row[idx].value == 'MA':
                temp.append('BM')
            else:
                temp.append(row[idx].value)
        master.append(temp)
    return master


def _get_added_stands(data):
    all_stands = {row[0] for row in data}
    added_stands = {}
    for i, stand in enumerate(all_stands):
        added_stands[i] = []
        for j in range(2):
            holder = deepcopy(RFRS_ERROR_HOLDER)
            if j == 0:
                holder['name_id'] = f'add_{i}_name'
                holder['val'] = stand
            else:
                holder['name_id'] = f'add_{i}_pf'
                holder['val'] = ''
            added_stands[i].append(holder)
    return added_stands


def keep_fvs_stand_info(request_form):
    stands = {key.split('_')[-1] for key in request_form if key.split('_')[0] in RFRS_FVS_HEADS}
    master = {}
    for stand in stands:
        master[stand] = [RFRS_FVS_HEADS]
        temp = []
        for key in RFRS_FVS_HEADS:
            holder = deepcopy(RFRS_ERROR_HOLDER)
            holder['name_id'] = f'{key}_{stand}'
            holder['val'] = request_form[f'{key}_{stand}']
            temp.append(holder)
        master[stand].append(temp)
    return master


def check_fvs_form_data(request_form):
    stands = {key.split('_')[-1] for key in request_form if key.split('_')[0] in RFRS_FVS_HEADS}

    master = {}
    flash_bucket = []

    for stand in stands:
        variant = request_form[f'Variant_{stand}']
        master[stand] = [RFRS_FVS_HEADS]
        temp = []
        for key in FVS_ERR_CHECK:
            holder = deepcopy(RFRS_ERROR_HOLDER)
            holder['name_id'] = f'{key}_{stand}'

            err, val, flash = FVS_ERR_CHECK[key](request_form[f'{key}_{stand}'], key, stand, variant)
            holder['val'] = val
            if err:
                holder['err'] = True
                if flash:
                    flash_bucket.append(flash)
            temp.append(holder)
        master[stand].append(temp)

    if flash_bucket:
        flash = '<br>'.join(flash_bucket)
        return True, master, flash
    else:
        return False, master, None


def process_fvs_form(dbs, stand_info, rfrs_stands, base_directory):
    directory = check_make_directory(base_directory)
    fvs = FVS()
    rfrs_stands_all = {stand.stand: stand for stand in rfrs_stands}

    flash_bucket = []
    for stand in stand_info:
        args = [rfrs_stands_all[stand].create_tt_stand()] + [i['val'] for i in stand_info[stand][1]]
        fvs.set_stand(*args)
        if 'ACCESS' in dbs:
            filename = get_fvs_filename('.accdb')
            fvs.access_db(filename, directory)
            flash_bucket.append(f'Successfully created Access Database and LOC file at [ {join(directory, filename)} ]')
        if 'EXCEL' in dbs:
            filename = get_fvs_filename('.xlsx')
            fvs.excel_db(filename, directory)
            flash_bucket.append(f'Successfully created Excel Database at [ {join(directory, filename)} ]')
        if 'SQLITE' in dbs:
            filename = get_fvs_filename('.db')
            fvs.sqlite_db(filename, directory)
            flash_bucket.append(f'Successfully created SQLite Database at [ {join(directory, filename)} ]')

    flash_bucket = list(set(flash_bucket))
    return '<br>'.join(flash_bucket)


def _convert_sheet_to_table(sheet_rows):
    master = []
    err = False
    for i, row in enumerate(sheet_rows):
        temp = []
        for j, col in enumerate(row):
            if j == 0:
                if any([not c.isalnum() for c in col]):
                    err = True
                    break
            holder = deepcopy(RFRS_ERROR_HOLDER)
            holder['name_id'] = f'rfrs_{RFRS_SHEET_HEADER[j]}_{i + 1}'
            if col is None:
                holder['val'] = ''
            else:
                holder['val'] = col
            temp.append(holder)
        master.append(temp)
    if err:
        return err, None
    else:
        return err, master


def append_stand_from_sheet(file, stand):
    if file.filename[-4:] == '.csv':
        data = _read_csv(file)
    else:
        data = _read_excel(file)

    name_same_index = 0
    for row in data:
        if row[0].upper() == stand.stand:
            kwargs = {sub.lower().replace(' ', '_'): row[j] for j, sub in enumerate(RFRS_SHEET_HEADER)}
            if name_same_index >= len(stand.table_rows):
                table = RfrsTable(db=stand.db, ref_stand=stand.ref_stand, **kwargs)
                #table.set_db(stand.db)
                table.insert_self()
            else:
                table = stand.table_rows[name_same_index]
                for j, sub in enumerate(RFRS_SHEET_HEADER):
                    table[sub.lower().replace(' ', '_')] = row[j]
                table.update_self()
            name_same_index += 1
    if name_same_index == 0:
        return True, f'Could not find Stand Name ({stand.stand}) in the sheet'
    else:
        return False, None


def check_form_data(request_form, rfrs_stands=None, stand=None):
    temp = {}
    flash_bucket = []
    req_form_list = list(request_form)
    added_stands = {}
    for i, key in enumerate(req_form_list):
        holder = deepcopy(RFRS_ERROR_HOLDER)
        if key [:3] == 'add':
            d = {
                'name': 'Name',
                'pf': 'Plot Factor'
            }
            split = key.split('_')
            row = int(split[1])
            if row not in added_stands:
                added_stands[row] = []
            val = request_form[key]
            holder['name_id'] = key
            if val == '':
                flash_bucket.append(f'Stand {d[split[-1]]} Row {int(split[1]) + 1} cannot be blank')
                holder['val'] = val
                holder['err'] = True
            else:
                if split[-1] == 'name':
                    holder['val'] = val
                else:
                    try:
                        x = float(val)
                        holder['val'] = x
                    except ValueError:
                        holder['val'] = val
                        holder['err'] = True
                        flash_bucket.append(f'Stand Plot Factor Row {int(split[1]) + 1} has to be a number')
            added_stands[row].append(holder)

        if key[:4] == 'rfrs':
            holder = deepcopy(RFRS_ERROR_HOLDER)
            holder['name_id'] = key
            val = request_form[key]

            split = key.split('_')
            col_name = split[1]
            row = int(split[2])

            if col_name == 'STAND' and val == '':
                if request_form[req_form_list[i + 1]] == '':
                    break

            if row not in temp:
                temp[row] = []
            err, checked_val, flash = RFRS_ERR_CHECK[col_name](val, col_name, row, rfrs_stands)
            if err:
                holder['err'] = err
                flash_bucket.append(flash)
            holder['val'] = checked_val
            temp[row].append(holder)

    master = [temp[i] for i in temp]
    if flash_bucket:
        flash_bucket = list(set(flash_bucket))
        return False, master, added_stands, '<br>'.join(flash_bucket)
    else:
        if master:
            return True, master, added_stands, None
        else:
            if stand:
                master = get_table_from_previous_stand(stand)
                return True, master, added_stands, None
            else:
                return False, None, None, f'Please enter some data before processing'


def check_thin_form_data(request_form):
    flash_bucket = []
    thinning_params = {}

    for key in request_form:
        if key not in ['export_report_pdf']:
            if key == 'species_to_cut':
                if key not in thinning_params:
                    thinning_params[key] = request_form.getlist('species_to_cut')
            else:
                thinning_params[key] = request_form[key]

    if 'species_to_cut' not in request_form:
        thinning_params['species_to_cut'] = []

    key_list = list(thinning_params)
    for key in key_list:
        flash_val = ' '.join([i.capitalize() for i in key.split('_')])
        if key not in ['species_to_cut', 'thinning_type']:
            try:
                x = int(thinning_params[key])
                if x < 0:
                    flash_bucket.append(f'{flash_val} cannot be negative')
                thinning_params[key] = x
            except ValueError:
                if thinning_params[key] == '':
                    if key == 'min_dbh_to_cut':
                        thinning_params[key] = 0
                    elif key == 'max_dbh_to_cut':
                        thinning_params[key] = 999
                    else:
                        flash_bucket.append(f'{flash_val} cannot be blank')
                else:
                    flash_bucket.append(f'{flash_val} has to be a number')
        else:
            if key == 'species_to_cut':
                if not thinning_params[key]:
                    flash_bucket.append(f'{flash_val} needs at least one Species selected')

    if flash_bucket:
        return False, thinning_params, '<br>'.join(flash_bucket)
    else:
        return True, thinning_params, None


def process_stands_from_table(orm, table_data, added_stands):
    for i in added_stands:
        stand_name = added_stands[i][0]['val']
        plot_factor = added_stands[i][1]['val']
        stand = RfrsStand(db=orm.db, stand=stand_name, plot_factor=plot_factor)
        stand.insert_self()
        stand.ref = orm.get_last_primary(RfrsStand)
        stand.ref_stand = f'{stand.ref}_{stand.stand}'
        stand.update_self()

        for row in table_data:
            if row[0]['val'] == stand_name:
                kwargs = {col['name_id'].split('_')[1].lower().replace(' ', '_'): col['val'] for col in row}
                table = RfrsTable(db=orm.db, ref_stand=stand.ref_stand, **kwargs)
                table.insert_self()
                table.set_table_row()
    return orm.select_all_rfrs_stands()


def thin_stand(tt_stand, thinning_params):
    kwargs = {key: thinning_params[key] for key in thinning_params if key not in ['thinning_type', 'export_report_pdf']}
    try:
        if thinning_params['thinning_type'] == 'tpa':
            thin = ThinTPA(tt_stand, **kwargs)
        elif thinning_params['thinning_type'] == 'ba':
            thin = ThinBA(tt_stand, **kwargs)
        else:
            thin = ThinRD(tt_stand, **kwargs)
        html = html_report_thinning(thin.summary_thin)
        return thin, html, thin.report_message.replace('\n', '<br>')

    except TargetDensityError:
        if thinning_params['thinning_type'] != 'tpa':
            param = thinning_params['thinning_type'] + '_ac'
        else:
            param = thinning_params['thinning_type']
        td = thinning_params['target_density']
        return None, None, f"""Target Density Error: Stand {param.upper().replace('_', '/')} ({round(tt_stand[param], 1)}) 
        is less than the Target Density of {td} {param.upper().replace('_', '/')}. Please modify thinning parameters"""


def html_report_output(stand, metrics_only=False):
    ps = 3
    html = _html_report_output_species(stand.summary_stand)
    if metrics_only:
        return html
    else:
        for i in range(ps):
            html += tag_one_line(1, 'p', '&emsp;', True)
        html += _html_report_output_logs(stand.summary_logs)
        for i in range(ps):
            html += tag_one_line(1, 'p', '&emsp;', True)
        html += _html_report_stand_stats(stand.summary_stats)
        return html


def _html_report_output_species(stand_summary):
    DIVS = [[1, 'div', False, True, {'cls': 'form-group'}],
            [2, 'div', False, True, {'cls': 'table-responsive'}]]
    html = tags_from_list(DIVS)
    html += tag_one_line(3, 'h5', 'STAND METRICS', True)

    html += tag(3, 'table', False, True, cls='table table-striped table-sm')
    TABLE_HEAD = [[4, 'thead', False, True, {}],
                  [5, 'tr', False, True, {}]]
    html += tags_from_list(TABLE_HEAD)

    for i in stand_summary[0]:
        html += tag_one_line(6, 'th', i, True, cls='text-center', style='width: auto;')
    html += tags_close_from_list(TABLE_HEAD)

    html += tag(4, 'tbody', False, True)
    for i, row in enumerate(stand_summary[1:], 1):
        html += tag(5, 'tr', False, True)
        for j, col in enumerate(row):
            if i == len(stand_summary) - 1:
                if j == 0:
                    html += tag_one_line(6, 'td', col, True, style='font-weight: bold;')
                else:
                    html += tag_one_line(6, 'td', col, True, cls='text-center', style='font-weight: bold;')
            else:
                if j == 0:
                    html += tag_one_line(6, 'td', col, True)
                else:
                    html += tag_one_line(6, 'td', col, True, cls='text-center')

        html += tag_close(5, 'tr')
    html += tag_close(4, 'tbody')
    html += tag_close(3, 'table', True)
    html += tags_close_from_list(DIVS)
    return html


def _html_report_output_logs(logs_summary):
    DIVS = [[1, 'div', False, True, {'cls': 'form-group'}],
            [2, 'div', False, True, {'cls': 'table-responsive'}]]
    html = tags_from_list(DIVS)
    html += tag_one_line(3, 'h5', 'LOG METRICS', True)

    for i, tab in enumerate(logs_summary):
        if i > 0:
            html += tag_one_line(3, 'p', '&emsp;', True)
        html += tag_one_line(3, 'h6', tab, True)

        for j, species in enumerate(logs_summary[tab]):
            table = logs_summary[tab][species]
            html += tag(3, 'table', False, True, cls='table table-striped table-sm text-center')
            html += tag(4, 'thead', False, True)
            html += tag(5, 'tr', False, True)
            html += tag_one_line(6, 'th', species, True, colspan=len(table[0]), style='font-weight: bold;')
            html += tag_close(5, 'tr')
            html += tag(5, 'tr', False, True)
            for data in table[0]:
                html += tag_one_line(6, 'th', data, True, style='font-weight: bold;')
            html += tag_close(5, 'tr')
            html += tag_close(4, 'thead')

            html += tag(4, 'tbody', False, True)
            for k, data in enumerate(table[1:], 1):
                html += tag(5, 'tr', False, True)
                for l in data:
                    if k == len(table) - 1:
                        html += tag_one_line(6, 'td', l, True, style='font-weight: bold;')
                    else:
                        html += tag_one_line(6, 'td', l, True)
                html += tag_close(5, 'tr')
            html += tag_close(4, 'tbody')
            html += tag_close(3, 'table')
    return html


def _html_report_stand_stats(stats_summary):
    html = tag_one_line(1, 'h5', 'STAND STATISTICS', True)

    for species in stats_summary:
        table = stats_summary[species]
        DIVS = [[1, 'div', False, True, {'cls': 'form-group'}],
                [2, 'div', False, True, {'cls': 'table-responsive'}]]
        html += tags_from_list(DIVS)

        html += tag(3, 'table', False, True, cls='table table-striped table-sm text-center')
        html += tag(4, 'thead', False, True)

        html += tag(5, 'tr', False, True)
        html += tag_one_line(6, 'th', species, True, colspan=len(table[0]), style='font-weight: bold;')
        html += tag_close(5, 'tr')

        html += tag(5, 'tr', False, True)
        for data in table[0]:
            html += tag_one_line(6, 'th', data, True, style='font-weight: bold;')
        html += tag_close(5, 'tr')
        html += tag_close(4, 'thead')

        html += tag(4, 'tbody', False, True)
        for k, data in enumerate(table[1:], 1):
            html += tag(5, 'tr', False, True)
            for l in data:
                html += tag_one_line(6, 'td', l, True)
            html += tag_close(5, 'tr')

        html += tag_close(4, 'tbody')
        html += tag_close(3, 'table')
        html += tags_close_from_list(DIVS)
    return html


def html_report_thinning(summary_thin):
    html = tag_one_line(1, 'h5', 'THINNING RESULTS', True)

    for condition in summary_thin:
        html += tag_one_line(1, 'p', '&emsp;', True)
        DIVS = [[1, 'div', False, True, {'cls': 'form-group'}],
                [2, 'div', False, True, {'cls': 'table-responsive'}]]
        html += tags_from_list(DIVS)

        html += tag_one_line(3, 'h6', condition, True)
        html += tag(3, 'table', False, True, cls='table table-striped table-sm text-center')
        html += tag(4, 'thead', False, True)

        table = summary_thin[condition]
        html += tag(5, 'tr', False, True)
        for j in table[0]:
            html += tag_one_line(6, 'th', j, True, style='font-weight: bold;')
        html += tag_close(5, 'tr')
        html += tag_close(4, 'thead')

        html += tag(4, 'tbody', False, True)
        for i, row in enumerate(table[1:], 1):
            html += tag(5, 'tr', False, True)
            for item in row:
                if i == len(table) - 1:
                    html += tag_one_line(6, 'td', item, True, style='font-weight: bold;')
                else:
                    html += tag_one_line(6, 'td', item, True)
            html += tag_close(5, 'tr')
        html += tag_close(4, 'tbody')
        html += tag_close(3, 'table')
        html += tags_close_from_list(DIVS)
    return html


def process_fvs_monster_sheet(file):
    file.seek(0)
    wb = open_workbook(file_contents=file.read())

    info_sheet = wb.sheet_by_name(FVS_SHEETS[0])
    tree_sheet = wb.sheet_by_name(FVS_SHEETS[1])
    summary_sheet = wb.sheet_by_name(FVS_SHEETS[2])
    cut_sheet = wb.sheet_by_name(FVS_SHEETS[3])
    atr_sheet = wb.sheet_by_name(FVS_SHEETS[4])

    info_csi = [i for i, x in enumerate(info_sheet[0]) if x.value == 'CaseID'][0]
    keyfile_csi = [i for i, x in enumerate(info_sheet[0]) if x.value == 'KeywordFile'][0]
    all_cases = [row[info_csi].value for i, row in enumerate(info_sheet) if i > 0]
    all_key_files = [row[keyfile_csi].value for i, row in enumerate(info_sheet) if i > 0]

    cases_key_file_dict = {case: key for case, key in zip(all_cases, all_key_files)}

    cut_csi = [i for i, x in enumerate(cut_sheet[0]) if x.value == 'CaseID'][0]
    cut_cases = list({row[cut_csi].value for i, row in enumerate(cut_sheet) if i > 0})

    if sorted(all_cases) == sorted(cut_cases):
        missing_no_mgt_run = True
        no_mgt_case = all_cases[0]
    else:
        missing_no_mgt_run = False
        no_mgt_case = [case for case in all_cases if case not in cut_cases][0]

    yri_summ = [i for i, x in enumerate(summary_sheet[0]) if x.value == 'Year'][0]
    start_year = summary_sheet[1][yri_summ].value

    current_table, stand_min_dbh, stand_max_dbh = _get_monster_summary_tables(tree_sheet, no_mgt_case, target_year=start_year)
    current_dfc = _get_monster_dfc_year(summary_sheet, no_mgt_case)
    current_dfc_table, _, _ = _get_monster_summary_tables(tree_sheet, no_mgt_case, target_year=current_dfc)

    if not missing_no_mgt_run:
        runs = {
            'no_mgmt': {
                'titles': {
                    'CASE': 'NO MANAGEMENT'
                },
                'tables': {
                    'CURRENT CONDITIONS': current_table,
                    'DFC CONDITIONS': [f'YEAR: {int(current_dfc)}'] + current_dfc_table
                },
                'ignore_for_sort': 0
            }
        }
    else:
        runs = {
            'no_mgmt': {
                'titles': {
                    'UNABLE TO FIND "NO MANAGEMENT" SCENARIO': ''
                },
                'ignore_for_sort': 0
            }
        }

    for case in cut_cases:
        runs[case] = {
            'titles': {
                'FVS CASE ID': case,
                'FVS KEY FILE NAME': cases_key_file_dict[case]
            },
            'params': {
                'CUTTING PARAMETERS': '',
                'Min DBH': None,
                'Max DBH': None,
                'Thinning Type': None,
                'Density Target': None,
                'Spacing Target': None
            },
            'tables': {
                'CURRENT CONDITIONS': current_table,
                'REMOVALS': None,
                'RESIDUAL CONDITIONS': None,
                'DFC CONDITIONS': None
            },
            'ignore_for_sort': None
        }
        for key, sheet in [['removals', cut_sheet], ['residuals', atr_sheet]]:
            table, min_dbh, max_dbh = _get_monster_summary_tables(sheet, case)
            if key == 'removals':
                dfc = _get_monster_dfc_year(summary_sheet, case)
                dfc_table, _, _ = _get_monster_summary_tables(tree_sheet, case, target_year=dfc)
                thinning_type, min_dbh_text, max_dbh_text = _get_thinning_type(stand_min_dbh, stand_max_dbh, min_dbh, max_dbh)
                runs[case]['params']['Min DBH'] = min_dbh_text
                runs[case]['params']['Max DBH'] = max_dbh_text
                runs[case]['params']['Thinning Type'] = thinning_type
                runs[case]['tables']['REMOVALS'] = table
                runs[case]['tables']['DFC CONDITIONS'] = [f'YEAR: {int(dfc)}'] + dfc_table
            else:
                thinning_target, spacing = _get_thinning_target_and_spacing(table[-1])
                runs[case]['params']['Density Target'] = thinning_target
                runs[case]['params']['Spacing Target'] = spacing
                runs[case]['tables']['RESIDUAL CONDITIONS'] = table
                runs[case]['ignore_for_sort'] = table[-1][1]

    sort_cases_by_removal = sorted([case for case in runs], key=lambda x: runs[x]['ignore_for_sort'])
    master = {case: runs[case] for case in sort_cases_by_removal}
    for case in master:
        del master[case]['ignore_for_sort']

    return master, missing_no_mgt_run


def _get_monster_dfc_year(summary_sheet, case):
    case_index = [i for i, x in enumerate(summary_sheet[0]) if x.value == 'CaseID'][0]
    year_index = [i for i, x in enumerate(summary_sheet[0]) if x.value == 'Year'][0]
    dfc_params = ['BA', 'QMD']
    dfc_idxs = [i for i, x in enumerate(summary_sheet[0]) if x.value in dfc_params]
    dfc = None
    for i, row in enumerate(summary_sheet):
        if i > 0:
            if row[case_index].value == case:
                if row[dfc_idxs[0]].value >= 300 and row[dfc_idxs[1]].value >= 21:
                    dfc = row[year_index].value
                    break
    return dfc


def _get_monster_summary_tables(sheet, case, target_year=None):
    case_index = [i for i, x in enumerate(sheet[0]) if x.value == 'CaseID'][0]
    year_index = [i for i, x in enumerate(sheet[0]) if x.value == 'Year'][0]
    param_indexes = [i for i, x in enumerate(sheet[0]) if x.value in FVS_SHEET_PARAMS]

    current_mets = []
    if target_year:
        for i, row in enumerate(sheet):
            if i > 0:
                if row[year_index].value == target_year and row[case_index].value == case:
                    current_mets.append([row[i].value for i in param_indexes])
    else:
        for i, row in enumerate(sheet):
            if i > 0:
                if row[case_index].value == case:
                    current_mets.append([row[i].value for i in param_indexes])
    BLANK = {
        'tpa': [],
        'ba': [],
        'rd': [],
        'hgt': [],
        'bf': []
        }
    species = {
        'totals': deepcopy(BLANK)
    }
    min_dbh = None
    max_dbh = None
    for row in current_mets:
        spp = row[0]
        if spp not in species:
            species[spp] = deepcopy(BLANK)

        tpa, dbh, hgt, bf = row[1:]
        min_dbh, max_dbh = _min_max_check(min_dbh, max_dbh, dbh)

        ba = (dbh ** 2 * 0.005454) * tpa
        rd = ba / math.sqrt(dbh)
        w_bf = bf * tpa
        temp = [tpa, ba, rd, hgt, w_bf]

        for i, key in enumerate(species[spp]):
            species[spp][key].append(temp[i])
            species['totals'][key].append(temp[i])

    for spp in species:
        for key in species[spp]:
            if key == 'hgt':
                species[spp][key] = mean(species[spp][key])
            else:
                species[spp][key] = sum(species[spp][key])

    for spp in species:
        species[spp]['qmd'] = math.sqrt((species[spp]['ba'] / species[spp]['tpa']) / 0.005454)
        species[spp]['hdr'] = species[spp]['hgt'] / (species[spp]['qmd'] / 12)
        species[spp]['bf'] = species[spp]['bf'] / 1000

    heads = [['tpa', 'TPA'], ['ba', 'BA'], ['qmd', 'QMD'], ['rd', 'RD'], ['hgt', 'AVG HGT'], ['hdr', 'HDR'], ['bf', 'MBF']]
    master = [['SPECIES'] + [i[1] for i in heads]]
    for spp in species:
        if spp == 'totals':
            master.append(['TOTALS'] + [species[spp][key[0]] for key in heads])
        else:
            master.append([RFRS_ALL_SPECIES_NAMES[spp]] + [species[spp][key[0]] for key in heads])

    master.append(master.pop(1))
    return master, min_dbh, max_dbh


def _get_thinning_type(stand_min, stand_max, case_min, case_max):
    if case_min == stand_min and case_max == stand_max:
        return f'Thin evenly throughout diameter range', 'No Minimum', 'No Maximum'
    elif case_min == stand_min:
        return f'Thin from below', 'No Minimum DBH', f'{math.floor(case_max)} inches'
    elif case_max == stand_max:
        return f'Thin from above', f'{math.floor(case_min)} inches', 'No Maximum'
    else:
        return f'Thin throughout diameter limits', f'{math.floor(case_min)} inches', f'{math.floor(case_max)} inches'


def _get_thinning_target_and_spacing(totals_row):
    targets = ['TPA', 'Basal Area', 'Relative Density']
    target_metrics = [totals_row[i] for i in [1, 2, 4]]
    tpa = totals_row[1]

    for i, col in enumerate(target_metrics):
        margin = .025
        under = math.floor(col + margin)
        over = math.ceil(col - margin)
        if under == over:
            if under % 10 == 0 or under % 5 == 0:
                target_text = f'{under} {targets[i]}'
                break
    else:
        target_text = ' or '.join([f'{math.floor(col)} {target}' for col, target in zip(target_metrics, targets)])

    spacing = math.floor(math.sqrt(43560 / tpa))
    return target_text, f'{spacing} x {spacing} feet'


def _min_max_check(min_dbh, max_dbh, dbh):
    if min_dbh:
        if dbh < min_dbh:
            min_dbh = dbh
    else:
        min_dbh = dbh

    if max_dbh:
        if dbh > max_dbh:
            max_dbh = dbh
    else:
        max_dbh = dbh

    return min_dbh, max_dbh










