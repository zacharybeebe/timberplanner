from imports._imports_ import (
    math,
    deepcopy,
    datetime,
    perf_counter,
    Reader
)
from config import (
    FOREST_BLOCKS,
    FILTERS,
    FILTER_HEADS,
    SALES_SEARCH_HEADER,
    SALE_INFO_LABELS,
    SALE_DISPLAY_BOOL,
    TRUSTS_DICT,
    TRUSTS_REV_SPLIT,
    UNIT_HEADER,
    UNITS_TABLE_BODY,
    UNITS_TABLE_BODY_TRUST,
    SILVICULTURE,
    SILV_MONTH_YEAR,
    h_date,
    f_bool,
    f_round,
    f_price,
    f_pct,
    back_bool,
    back_date,
    get_fy
)


def timer(func):
    def wrapper(*args, **kwargs):
        now = perf_counter()
        x = func(*args, **kwargs)
        after = perf_counter()
        print(f'{func.__name__} took {round(after-now, 5)} seconds\n')
        return x
    return wrapper


def today():
    return datetime.today()


def change_readonly(app, readonly):
    if readonly == 'true':
        app.config['READONLY'] = True
        app.config['CONSTANTS']['READONLY'] = True
    else:
        app.config['READONLY'] = False
        app.config['CONSTANTS']['READONLY'] = False


# @timer
def filter_sales(sales, fy, filter_keys):
    if fy != 'all':
        sales = [sale for sale in sales if sale.fy == fy]

    current_filters = [[key, filter_keys[key]] for key in filter_keys if filter_keys[key] != 'all']
    if current_filters:
        filtered_sales = []
        for sale in sales:
            for i in current_filters:
                attr, filter = i
                if attr == 'forest':
                    if sale[attr] != filter:
                        break
                else:
                    if sale[attr] < filter[0] or sale[attr] >= (filter[1] + 1):
                        break
            else:
                filtered_sales.append(sale)
    else:
        filtered_sales = sales

    filter_ranges = _get_filter_ranges(filtered_sales)
    return_trusts = _get_trust_summary_from_sales(filtered_sales)
    return_sales = _get_sales_table(filtered_sales)
    return_totals = _get_totals(filtered_sales, fy)
    return_filters = _get_filter_dict(filter_keys, filter_ranges)

    return return_sales, return_totals, return_trusts, return_filters


def _get_filter_ranges(sales):
    filters = []
    for attr in FILTERS:
        if attr == 'forest':
            filters.append(FOREST_BLOCKS)
        else:
            step = FILTERS[attr]['step']
            vals = {math.floor(sale[attr] / step) * step for sale in sales}
            filters.append([[i, i + (step - 1)] for i in sorted(vals)])
    return filters


def _get_trust_summary_from_sales(sales):
    acres, mbf, value_trust, value_dnr = sum([sale.acres for sale in sales]), sum([sale.mbf for sale in sales]), 0, 0

    temp = {}
    for sale in sales:
        for trust in sale.trusts:
            if trust not in temp:
                if sale.trusts[trust]['acres'] > 0 and sale.trusts[trust]['mbf'] > 0:
                    temp[trust] = [0, 0, 0, 0]
            if sale.trusts[trust]['acres'] > 0 and sale.trusts[trust]['mbf'] > 0:
                val = sale.value_mbf * sale.trusts[trust]['mbf']
                vals = [sale.trusts[trust]['acres'], sale.trusts[trust]['mbf'],
                        val * (1 - TRUSTS_REV_SPLIT[trust]), val * TRUSTS_REV_SPLIT[trust]]
                for i in range(len(vals)):
                    temp[trust][i] += vals[i]
                value_trust += vals[2]
                value_dnr += vals[3]

    sort = sorted(temp)
    trusts = {}
    x = [acres, mbf, value_trust, value_dnr]
    for trust in sort:
        t = f"TRUST {'0' * (2 - len(str(trust)))}{trust}"
        trusts[t] = []
        count = 0
        for i, j in zip(temp[trust], x):
            if count > 1:
                trusts[t].append([f_price(i), f_pct(i / j)])
            else:
                trusts[t].append([f_round(i), f_pct(i / j)])
            count += 1
    trusts['TOTALS'] = []
    for i, val in enumerate(x):
        if i > 1:
            trusts['TOTALS'].append(f_price(val))
        else:
            trusts['TOTALS'].append(f_round(val))
    return trusts


def _get_sales_table(sales):
    master = [[SALES_SEARCH_HEADER[key]['head'] for key in SALES_SEARCH_HEADER]]
    for sale in sales:
        data = []
        for key in SALES_SEARCH_HEADER:
            if key == 'checkbox':
                data.append(key)
            else:
                func = SALES_SEARCH_HEADER[key]['func']
                data.append(func(sale[key]))
        master.append(data)
    return master


def _get_totals(filtered_sales, fy):
    if fy == 'all':
        t = 'TOTALS ALL FISCAL YEARS'
    else:
        t = f'TOTALS FISCAL YEAR {fy}'

    mbf = sum([sale.mbf for sale in filtered_sales])
    acres = sum([sale.acres for sale in filtered_sales])
    value = sum([sale.value for sale in filtered_sales])
    if acres == 0:
        mbf_ac = 0
        value_ac = 0
    else:
        mbf_ac = mbf / acres
        value_ac = value / acres
    if mbf == 0:
        value_mbf = 0
    else:
        value_mbf = value / mbf

    data = [mbf, acres, mbf_ac, value_mbf, value, value_ac]
    func_keys = ['mbf', 'acres', 'mbf_ac', 'value_mbf', 'value', 'value_ac']
    master = [t]
    for d, key in zip(data, func_keys):
        master.append(SALES_SEARCH_HEADER[key]['func'](d))
    return master


def _get_filter_dict(filter_keys, filter_ranges):
    master = {}
    for head, key, rngs in zip(FILTER_HEADS, filter_keys, filter_ranges):
        if key == 'forest':
            val = filter_keys[key]
            master[head] = {
                'val': val,
                'show_val': 'all' if val == 'all' else val,
                'attr': key,
                'rngs': rngs,
                'show_rngs': rngs
            }
        else:
            func1, func2 = FILTERS[key]['funcs']
            val = filter_keys[key]
            master[head] = {
                'val': val,
                'show_val': 'all' if val == 'all' else f"""{func1(val[0])} - {func2(val[1])}""",
                'attr': key,
                'rngs': rngs,
                'show_rngs': [f"""{func1(rng[0])} - {func2(rng[1])}""" for rng in rngs]
            }
    return master


def delete_sales(orm, sales, request_form):
    deleted_sales = []
    sales_dict = {sale.sale_name: sale for sale in sales}
    for key in request_form:
        if key[:3] == 'cbx':
            sale = sales_dict[key.split('_')[1]]
            for u in sale.units:
                unit = sale.units[u]
                orm.delete(unit.__class__, unit.ref)
                del unit
            orm.delete(sale.__class__, sale.ref)
            deleted_sales.append(sale.sale_name)
            del sale
    new_sales = orm.select_all_sales()
    deleted_sales = ', '.join(deleted_sales)
    fys = {sale.fy for sale in new_sales}
    return new_sales, deleted_sales, fys


def delete_units(orm, sale, request_form):
    deleted_units = []
    for key in request_form:
        if key[:3] == 'cbx':
            unit_num = int(key.split('_')[1])
            deleted_units.append(str(unit_num))
            unit = sale.units[unit_num]
            orm.delete(unit.__class__, unit.ref)
            del sale.units[unit_num]
    if len(deleted_units) > 1:
        flash = f"""Units {', '.join(deleted_units)} have been deleted <br>"""
    else:
        flash = f"""Unit {deleted_units[0]} has been deleted <br>"""
    return get_units_table_from_sale(sale), flash


def swap(orm, sales, sale1_name, sale2_name):
    sales_dict = {sale.sale_name: sale for sale in sales}
    sale_1 = sales_dict[sale1_name]
    sale_2 = sales_dict[sale2_name]

    sale_1_date = (sale_1.due_date,)
    sale_1.due_date = sale_2.due_date
    sale_1.update_after_edit()

    sale_2.due_date = sale_1_date[0]
    sale_2.update_after_edit()
    return orm.select_all_sales()


def keep_create_sale_edits(request_form):
    si = deepcopy(SALE_INFO_LABELS)
    sale_info = {key: si[key] for key in si if si[key]['editable']}
    for field in request_form:
        if field[:2] == 'S_':
            key = field[2:]
            sale_info[key]['val'] = request_form[field]
    return sale_info


def get_initial_create_sale_info():
    sale_info = {key: dict(SALE_INFO_LABELS[key]) for key in SALE_INFO_LABELS if SALE_INFO_LABELS[key]['editable']}
    for key in sale_info:
        if key in SALE_DISPLAY_BOOL:
            sale_info[key]['val'] = 'No'
        else:
            if key == 'due_date':
                sale_info[key]['val'] = h_date(today())
            else:
                sale_info[key]['val'] = ''
    return sale_info


def check_sale_edits(orm, sale_name, request_form):
    flash = ''
    si = deepcopy(SALE_INFO_LABELS)
    sale_info = {key: si[key] for key in si if si[key]['editable']}

    for field in request_form:
        if field[:2] == 'S_':
            key = field[2:]
            val = request_form[field]

            if val == '':
                flash += f"""<br>{sale_info[key]['head']} cannot be blank"""
                sale_info[key]['val'] = ''
                sale_info[key]['err'] = True
            else:
                if key == 'sale_name':
                    new_name = val.upper()
                    if orm.sale_name_exists(sale_name, new_name):
                        flash += f'<br>Sale Name "{new_name}" already exists'
                        sale_info[key]['val'] = sale_name
                        sale_info[key]['err'] = True
                    elif '_' in new_name:
                        flash += f'<br>Sale Name cannot contain the underscore "_" character'
                        sale_info[key]['val'] = new_name
                        sale_info[key]['err'] = True
                    else:
                        sale_info[key]['val'] = new_name
                elif key == 'due_date':
                    sale_info[key]['val'] = back_date(val)
                elif key == 'value_mbf':
                    x = val
                    try:
                        x = float(val)
                        if x < 0:
                            flash += '<br>$ PER MBF cannot be negative'
                            sale_info[key]['err'] = True
                        sale_info[key]['val'] = x
                    except ValueError:
                        flash += '<br>$ PER MBF must be a number'
                        sale_info[key]['val'] = x
                        sale_info[key]['err'] = True
                else:
                    if key in SALE_DISPLAY_BOOL:
                        if val.upper() not in ['YES', 'NO']:
                            flash += f"""<br>{sale_info[key]['head']} must be 'Yes' or 'No'"""
                            sale_info[key]['val'] = val
                            sale_info[key]['err'] = True
                        else:
                            sale_info[key]['val'] = back_bool(val)
                    else:
                        sale_info[key]['val'] = val
    if flash != '':
        if flash[:4] == '<br>':
            flash = flash[4:]
        return False, _convert_sale_info_to_html(sale_info), flash
    else:
        return True, sale_info, flash


def _convert_sale_info_to_html(sale_info):
    for key in sale_info:
        if key == 'due_date':
            sale_info[key]['val'] = h_date(sale_info[key]['val'])
        else:
            if key in SALE_DISPLAY_BOOL:
                if isinstance(sale_info[key]['val'], int):
                    sale_info[key]['val'] = f_bool(sale_info[key]['val'])
    return sale_info


def check_unit_edits(request_form):
    unit_nums = sorted({int(key[2:].split('_')[1]) for key in request_form if key[:2] == 'U_'})
    blank_units = get_blank_units_table_body(unit_nums)

    flash = ''
    for u in blank_units:
        name_key = blank_units[u]['unit_name']['name']
        harv_key = blank_units[u]['harvest']['name']
        blank_units[u]['unit_name']['val'] = request_form[name_key]
        blank_units[u]['harvest']['val'] = request_form[harv_key]

        if request_form[name_key] == '':
            flash += f'<br>U{u} NAME cannot be blank'
            blank_units[u]['unit_name']['err'] = True
        elif request_form[name_key][:1].upper() != 'U' or not request_form[name_key][1:].isdigit():
            flash += f'<br>"{request_form[name_key]}" is not a valid Unit Name'
            blank_units[u]['unit_name']['err'] = True

        if request_form[harv_key] == '':
            flash += f'<br>U{u} HARVEST cannot be blank'
            blank_units[u]['harvest']['err'] = True
        elif request_form[harv_key] not in ['VRH', 'VDT', 'CT', 'ROW', 'YARDING']:
            flash += f'<br>Incorrect HARVEST "{request_form[harv_key]}" for U{u}'
            blank_units[u]['harvest']['err'] = True

        for t in blank_units[u]['trusts']:
            t_name = t['name']
            t_split = t_name.split('_')
            trust = int(t_split[-2])
            key = t_split[-1]

            x = request_form[t_name]
            if x == '':
                val = 0.0
            else:
                val = x
            try:
                val = float(val)
                t['val'] = val
                if val < 0:
                    flash += f'<br>U{u} TRUST {trust} {key.upper()} cannot be negative'
                    t['err'] = True
            except ValueError:
                flash += f'<br>U{u} TRUST {trust} {key.upper()} has to be a number'
                t['val'] = val
                t['err'] = True

    if flash != '':
        if flash[:4] == '<br>':
            flash = flash[4:]
        units_table = {
            'header': get_units_table_header(),
            'body': [blank_units[u] for u in blank_units]
        }
        return False, units_table, None, flash
    else:
        units_table = {
            'header': get_units_table_header(),
            'body': sorted([blank_units[u] for u in blank_units], key=lambda x: int(x['unit_name']['val'][1:]))
        }
        return True, units_table, _convert_unit_check_edits_to_attrs(blank_units), flash


def _convert_unit_check_edits_to_attrs(check_edits):
    unit_attrs = {}
    for u in check_edits:
        unit_attrs[u] = {
            'unit_name': check_edits[u]['unit_name']['val'],
            'harvest': check_edits[u]['harvest']['val'],
            'trusts': {}
        }
        for t in check_edits[u]['trusts']:
            t_name = t['name']
            t_split = t_name.split('_')
            trust = int(t_split[-2])
            key = t_split[-1]
            if trust not in unit_attrs[u]['trusts']:
                unit_attrs[u]['trusts'][trust] = {}
            if key not in unit_attrs[u]['trusts'][trust]:
                unit_attrs[u]['trusts'][trust][key] = t['val']
    return unit_attrs


def get_units_table_header():
    header1 = []
    header2 = []
    for key in UNIT_HEADER:
        if key == '':
            header1.append('checkbox')
            header2.append('checkbox')
        else:
            if isinstance(key, str):
                header1.append(UNIT_HEADER[key]['head'])
                header2.append('blank')
            else:
                header1.append(UNIT_HEADER[key]['head'])
                for i in range(2):
                    header2.append(UNIT_HEADER[key]['subs'][i])
    return [header1, header2]


def get_blank_units_table_body(units_list):
    body = {}
    for u in units_list:
        data = deepcopy(UNITS_TABLE_BODY)
        for key in data:
            if key in ['checkbox', 'unit_name', 'harvest']:
                data[key]['name'] = data[key]['name'].format(u)
            else:
                for trust in TRUSTS_DICT:
                    for key in ['acres', 'mbf']:
                        sub = deepcopy(UNITS_TABLE_BODY_TRUST)
                        sub['name'] = sub['name'].format(u, trust, key)
                        data['trusts'].append(sub)
        body[u] = data
    return body


def get_units_table_from_sale(sale):
    body = []
    for u in sale.units:
        unit = sale.units[u]
        data = deepcopy(UNITS_TABLE_BODY)
        for key in data:
            if key in ['checkbox', 'unit_name', 'harvest']:
                data[key]['name'] = data[key]['name'].format(u)
                if key != 'checkbox':
                    data[key]['val'] = unit[key]
            else:
                for trust in unit.trusts:
                    for key in ['acres', 'mbf']:
                        sub = deepcopy(UNITS_TABLE_BODY_TRUST)
                        sub['name'] = sub['name'].format(u, trust, key)
                        sub['val'] = round(unit.trusts[trust][key], 1)
                        data['trusts'].append(sub)
        body.append(data)

    units_table = {
        'header': get_units_table_header(),
        'body': body
    }
    return units_table


def get_units_table_from_dict(units_dict):
    body = []
    for u in units_dict:
        data = deepcopy(UNITS_TABLE_BODY)
        for key in data:
            if key in ['checkbox', 'unit_name', 'harvest']:
                data[key]['name'] = data[key]['name'].format(u)
                if key != 'checkbox':
                    data[key]['val'] = units_dict[u][key]
            else:
                for trust in units_dict[u]['trusts']:
                    for key in ['acres', 'mbf']:
                        sub = deepcopy(UNITS_TABLE_BODY_TRUST)
                        sub['name'] = sub['name'].format(u, trust, key)
                        sub['val'] = round(units_dict[u]['trusts'][trust][key], 1)
                        data['trusts'].append(sub)
        body.append(data)

    units_table = {
        'header': get_units_table_header(),
        'body': body
    }
    return units_table


def get_units_from_shp(shp_path, dbf_path):
    shp = Reader(shp=shp_path, dbf=dbf_path)

    formatted_shp = False
    if [i[0] for i in shp.fields[1:]] == ['TIMBER_TRU', 'UNIT_NM', 'ACRES1', 'MBF', 'MBF_AC']:
        formatted_shp = True

    units = {}
    if not formatted_shp:
        acres = shoelace_theorem(shp)
        for i, ac in enumerate(acres):
            u = i + 1
            if u not in units:
                units[u] = {'unit_name': f'U{u}',
                            'harvest': 'VRH',
                            'trusts': {j: {'acres': 0.0,
                                           'mbf': 0.0} for j in [1, 3, 6, 7, 8, 9, 10, 11, 12, 77]}}
            units[u]['trusts'][1]['acres'] = ac
            units[u]['trusts'][1]['mbf'] = 1.0
    else:
        for i in shp.records():
            u = int(i[1][1:])
            if u not in units:
                units[u] = {'unit_name': i[1],
                            'harvest': 'VRH',
                            'trusts': {j: {'acres': 0.0,
                                           'mbf': 0.0} for j in [1, 3, 6, 7, 8, 9, 10, 11, 12, 77]}}
            trust = int(i[0])
            units[u]['trusts'][trust]['acres'] += float(i[2])
            units[u]['trusts'][trust]['mbf'] += float(i[3])

    sort = sorted(units)
    sorted_units = {u_num: units[u_num] for u_num in sort}
    return sorted_units


def shoelace_theorem(shp):
    shapes = shp.shapes()
    pts = [shapes[i].points for i in range(len(shapes))]
    areas = []

    #SHOELACE THEOREM FOR FINDING AREA OF IRREGULAR POLYGONS
    for pt in pts:
        LEFT = 0
        RIGHT = 0
        for i, p in enumerate(pt):
            if i == len(pt) - 1:
                left_last = pt[0][1]
                right_last = pt[0][0]
            else:
                left_last = pt[i+1][1]
                right_last = pt[i+1][0]

            left_first = p[0]
            right_first = p[1]

            LEFT += (left_first * left_last)
            RIGHT -= (right_first * right_last)

        area = round(abs(0.5 * (LEFT+RIGHT)) / 43560, 1)
        areas.append(area)
    return areas


def get_silviculture_options(sale, contract_years=2):
    units = [sale.units[u].unit_name for u in sale.units if sale.units[u].harvest == 'VRH']
    fy = sale.fy

    master = deepcopy(SILVICULTURE)
    for key in master:
        month = SILV_MONTH_YEAR[key]['month']
        day = SILV_MONTH_YEAR[key]['day']
        year = fy + contract_years + SILV_MONTH_YEAR[key]['year_adj']
        master[key]['lab|target_date'] = f'{month}/{day}/{year}'
        master[key]['lab|fiscal_year'] = get_fy(month, year)
        if 'mul|units' in master[key]:
            master[key]['mul|units'] = units
        if 'mul|units_1' in master[key]:
            master[key]['mul|units_1'] = units
    return master


def process_silviculture_report(sale, reqeust_form, mul_lists):
    ignore_base = ['rerun_report_text', 'new_report_text', 'contract_years']
    master = deepcopy(SILVICULTURE)
    request_keys = list({key.split('=')[0] for key in reqeust_form if key not in ignore_base})
    ignore_keys = ignore_base + list(mul_lists)

    deleted_keys = [key for key in master if key not in request_keys]

    for key in deleted_keys:
        del master[key]

    for field in reqeust_form:
        if field not in ignore_keys:
            key, sub = field.split('=')
            if sub != 'ignore':
                master[key][sub] = reqeust_form[field]
    for field in mul_lists:
        key, sub = field.split('=')
        if key not in deleted_keys:
            master[key][sub] = mul_lists[field]

    contract_years = int(reqeust_form['contract_years'])
    for key in master:
        month = SILV_MONTH_YEAR[key]['month']
        day = SILV_MONTH_YEAR[key]['day']
        year = sale.fy + contract_years + SILV_MONTH_YEAR[key]['year_adj']
        master[key]['lab|target_date'] = f'{month}/{day}/{year}'
        master[key]['lab|fiscal_year'] = get_fy(month, year)
    master['regen'] = _sort_regen(master['regen'])
    return master, contract_years


def _sort_regen(regen):
    l = list(regen)
    start_index = None
    for i, key in enumerate(l):
        if key[-1] == '1':
            start_index = i
            break
    first = l[:start_index]
    last = l[start_index:]
    sort_keys = {
        'mul|units': 1,
        'addsel|species': 2,
        'addsel|stock type': 3,
        'inpt|target tpa': 4
    }
    sort = sorted(last, key=lambda x: int(f"{x[-1]}{sort_keys[x.replace('_', ' ')[:-2]]}"))
    return {key: regen[key] for key in first + sort}


def is_err_calculate_lrm_vol(sale, target, con_pct):
    if target == '':
        flash = 'Please enter a Target Volume'
        return True, target, None, flash
    else:
        try:
            x = float(target)
            if x < 0:
                flash = f'Target Volume cannot be negative ({x})'
                return True, target, None, flash
        except ValueError:
            flash = f'Target Volume must be a number ({target})'
            return True, target, None, flash

    target_volume = float(target)
    prop = target_volume / sale.mbf

    units = []
    for u in sale.units:
        unit = sale.units[u]
        temp = [f'{unit.harvest} {unit.unit_name}', int(prop * unit.mbf * (con_pct / 100)), int(prop * unit.mbf * ((100 - con_pct) / 100))]
        if temp[2] == 0:
            temp[2] = 1
            temp[1] -= 1
        if temp[1] == 0:
            temp[1] = 1
            temp[2] -= 1
        units.append(temp)

    sums = sum([sum(i[1:]) for i in units])
    if sums != target_volume:
        diff = target_volume - sums
        if diff < 0:
            change = -1
        else:
            change = 1
        while diff != 0:
            for i in units:
                if diff == 0:
                    break
                i[2] += change
                diff -= change

    units.append(['TOTALS', sum([i[1] for i in units]), sum([i[2] for i in units])])
    return False, target, units, None


def update_presales(presales, request_form):
    args = [key for key in presales.args if key not in ['ref', 'sale_ref']]
    form_transform = {'_'.join([i.lower() for i in key.split(' ')[:-1]]): int(key.split()[-1]) for key in request_form}
    for key in args:
        if key not in form_transform:
            presales[key] = -1
        else:
            presales[key] = form_transform[key]
    presales.update_self()
    presales.set_info()








if __name__ == '__main__':
    # db = 'TIMBER_DB.db'
    # sales = ORM.select_all_sales(db)
    #
    # fkeys = {'mbf': 'all',
    #          'mbf_ac': [20, 24],
    #          'value_mbf': 'all',
    #          'value': 'all',
    #          'value_ac': 'all'}
    #
    # f_sale, filters = filter_sales(sales, 'all', fkeys)
    #
    # _print(filters)
    #
    # [print(i) for i in f_sale]

    # x = 4562.2555215
    # print(f_round(x))
    pass


