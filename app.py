print('TimberPlanner v1.2 STARTING...\n')
from imports._imports_ import (
    register,
    deepcopy,
    Timer,
    getcwd,
    join,
    Path,
    Flask,
    request,
    render_template,
    redirect,
    url_for
)
from config import (
    SALE_INFO_LABELS,
    UNIT_HEADER,
    RFRS_SHEET_HEADER,
    GET_SILV_LIST_KEYS,
    FOREST_BLOCKS
)
from utils.config_utils import (
    f_date,
    check_make_directory,
    get_blank_sheet_filename,
    get_stand_pdf_filename,
    get_thin_pdf_filename,
    get_fvs_monster_name
)

from utils.app_utils import (
    change_readonly,
    filter_sales,
    delete_sales,
    delete_units,
    check_sale_edits,
    check_unit_edits,
    swap,
    keep_create_sale_edits,
    get_units_from_shp,
    get_units_table_from_sale,
    get_units_table_from_dict,
    get_units_table_header,
    get_initial_create_sale_info,
    get_silviculture_options,
    process_silviculture_report,
    is_err_calculate_lrm_vol,
    update_presales
)
from utils.rfrs_utils import (
    export_blank_RFRS_sheet,
    append_stand_from_sheet,
    get_table_from_sheet,
    get_table_from_previous_stand,
    check_form_data,
    check_thin_form_data,
    check_fvs_form_data,
    keep_fvs_stand_info,
    process_stands_from_table,
    process_fvs_form,
    process_fvs_monster_sheet,
    html_report_output,
    thin_stand
)
from utils.internal_utils import (
    open_browser,
    check_backup,
    check_make_copy_directory_for_local_db,
    copy_local_db_to_main,
    get_desktop_path
)
from utils.pdf_utils import PDF
from models.orm import ORM
from models.sale import Sale
from models.unit import Unit
from models.rfrs_stand import RfrsStand
from models.rfrs_table import RfrsTable
from models.silviculture import Silviculture
from models.presale import Presale


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if request.form['editable'] == 'yes':
            app.config['READONLY'] = False
            app.config['CONSTANTS']['READONLY'] = False
        return redirect(url_for('sales', fy='all'))
    return render_template('home.html', const=app.config['CONSTANTS'])


@app.route('/sales_<fy>', methods=['POST', 'GET'])
def sales(fy):
    flash = None
    if fy != 'all':
        fy = int(fy)

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.form['delete_on'] == 'on':
            app.config['TIMBERSALES'], deleted_sales, app.config['CONSTANTS']['FISCAL_YEARS'] = delete_sales(app.config['ORM'], app.config['TIMBERSALES'], request.form)
            flash = f"""{deleted_sales} and units deleted successfully"""
        elif request.form['swap_on'] == 'on':
            sale1_name, sale2_name = [key.split('_')[1] for key in request.form if key[:3] == 'cbx']
            app.config['TIMBERSALES'] = swap(app.config['ORM'], app.config['TIMBERSALES'], sale1_name, sale2_name)
            flash = f"""{sale1_name} successfully swapped with {sale2_name}"""
        else:
            for key in request.form:
                if key not in ['delete_on', 'swap_on']:
                    if request.form[key] == 'all' or key == 'forest':
                        app.config['FILTERS'][key] = request.form[key]
                    else:
                        app.config['FILTERS'][key] = [int(i.strip("'")) for i in request.form[key].strip("[]'").split(', ')]

    sales_table, totals, trust_summary, filters = filter_sales(app.config['TIMBERSALES'], fy, app.config['FILTERS'])
    return render_template('sales.html', const=app.config['CONSTANTS'], fy=fy, flash=flash, sales_table=sales_table,
                           totals=totals, trust_summary=trust_summary, filters=filters)


@app.route('/sale_<sale_name>', methods=['POST', 'GET'])
def sale(sale_name):
    flash_main = ''
    flash_sale = None
    flash_unit = None
    sale_name_change_check = (sale_name, )

    sale = {s.sale_name: s for s in app.config['TIMBERSALES']}[sale_name]
    sale_info = deepcopy(sale.info)
    units_table = get_units_table_from_sale(sale)

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.form['delete_on'] == 'on':
            flash_main = delete_units(app.config['ORM'], sale, request.form)
        else:
            if request.files['shp_file'].filename != '':
                files = request.files.getlist('shp_file')
                file_dict = {file.filename[-3:]: file for file in files}
                unit_attrs = get_units_from_shp(file_dict['shp'].stream, file_dict['dbf'].stream)
                for u in unit_attrs:
                    if u in sale.units:
                        for sub in unit_attrs[u]:
                            sale.units[u][sub] = unit_attrs[u][sub]
                        sale.units[u].update_after_edit()
                    else:
                        unit = Unit(db=app.config['DB'], sale_ref=sale.ref, **unit_attrs[u])
                        unit.insert_self()
                flash_main += 'Units have been updated<br>'
            else:
                no_unit_errors, units_table, unit_attrs, flash_unit = check_unit_edits(request.form)
                if no_unit_errors:
                    for u in unit_attrs:
                        if u not in sale.units:
                            new_unit = Unit(db=app.config['DB'], sale_ref=sale.ref, **unit_attrs[u])
                            new_unit.insert_self()
                        else:
                            for sub in unit_attrs[u]:
                                sale.units[u][sub] = unit_attrs[u][sub]
                            sale.units[u].update_after_edit()
                    flash_main += 'Units have been updated<br>'

        no_sale_errors, sale_info, flash_sale = check_sale_edits(app.config['ORM'], sale.sale_name, request.form)
        if no_sale_errors:
            for attr in sale_info:
                sale[attr] = sale_info[attr]['val']
            flash_main += 'Sale has been updated<br>'
            sale.update_after_edit()

        units_table = get_units_table_from_sale(sale)
        app.config['TIMBERSALES'] = app.config['ORM'].select_all_sales()
        app.config['CONSTANTS']['FISCAL_YEARS'] = {sale.fy for sale in app.config['TIMBERSALES']}

        if sale.sale_name != sale_name_change_check[0]:
            return redirect(url_for('sale', sale_name=sale.sale_name))

    return render_template('sale.html', const=app.config['CONSTANTS'], sale=sale, sale_info=sale_info, units_table=units_table,
                           flash_main=flash_main, flash_sale=flash_sale, flash_unit=flash_unit)


@app.route('/swap_sales', methods=['POST', 'GET'])
def swap_sales():
    flash = None
    sales = app.config['TIMBERSALES']
    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        sale1_name, sale2_name = request.form['sale_1'], request.form['sale_2']
        if sale1_name == sale2_name:
            flash = f"""Cannot swap {sale1_name} for {sale2_name} because they are the same sale"""
        else:
            app.config['TIMBERSALES'] = swap(app.config['ORM'], sales, sale1_name, sale2_name)
            flash = f"""{sale1_name} successfully swapped with {sale2_name}"""

    sales_list = [[sale.sale_name, f_date(sale.due_date)] for sale in app.config['TIMBERSALES']]
    return render_template('swap_sales.html', const=app.config['CONSTANTS'], flash=flash, sales=sales_list)


@app.route('/create_sale', methods=['POST', 'GET'])
def create_sale():
    flash_main = ''
    flash_sale = None
    flash_unit = None

    sale_info = get_initial_create_sale_info()
    units_table = {'header': get_units_table_header()}

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.files['shp_file'].filename != '':
            files = request.files.getlist('shp_file')
            file_dict = {file.filename[-3:]: file for file in files}
            unit_attrs = get_units_from_shp(file_dict['shp'].stream, file_dict['dbf'].stream)
            units_table = get_units_table_from_dict(unit_attrs)
            sale_info = keep_create_sale_edits(request.form)
        else:
            no_unit_errors, units_table, unit_attrs, flash_unit = check_unit_edits(request.form)
            no_sale_errors, sale_info, flash_sale = check_sale_edits(app.config['ORM'], None, request.form)

            if no_sale_errors and no_unit_errors and request.form['create_sale'] == 'yes':
                s = Sale(db=app.config['DB'])
                for key in sale_info:
                    s[key] = sale_info[key]['val']
                s.insert_self()
                s.ref = app.config['ORM'].get_last_primary(Sale)

                for u_num in unit_attrs:
                    u = Unit(db=app.config['DB'], sale_ref=s.ref)
                    for attr in unit_attrs[u_num]:
                        u[attr] = unit_attrs[u_num][attr]
                    u.insert_self()
                s.update_after_edit()
                p = Presale(db=app.config['DB'], sale_ref=s.ref)
                p.insert_self()

                app.config['TIMBERSALES'] = app.config['ORM'].select_all_sales()
                app.config['CONSTANTS']['FISCAL_YEARS'] = {sale.fy for sale in app.config['TIMBERSALES']}

                flash_main = f'Successfully created  "{s.sale_name}"'
                sale_info = get_initial_create_sale_info()
                units_table = {'header': get_units_table_header()}

    return render_template('create_sale.html', const=app.config['CONSTANTS'], sale_info=sale_info, units_table=units_table,
                           flash_main=flash_main, flash_sale=flash_sale, flash_unit=flash_unit)


@app.route('/rfrs', defaults={'flash_code': None}, methods=['POST', 'GET'])
@app.route('/rfrs_<flash_code>', methods=['POST', 'GET'])
def rfrs(flash_code):
    table_body = None
    if flash_code:
        flash = 'RFRS Stand successfully deleted'
    else:
        flash = None
    process_data_vis = 'hidden'
    added_stands = None

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.form['data_from_sheet_text'] == 'yes' or request.form['data_from_sheet_dnr'] == 'yes':
            if request.form['data_from_sheet_text'] == 'yes':
                file = request.files['data_file']
                dnr = False
            else:
                file = request.files['data_dnr']
                dnr = True
            error, table_body, added_stands, flash = get_table_from_sheet(file, from_dnr=dnr)
            if not error:
                process_data_vis = 'visible'

        elif request.form['data_from_sheet_fvs'] == 'yes':
            fvs_runs, missing_no_mgt = process_fvs_monster_sheet(request.files['data_fvs'])
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.compile_fvs_report(fvs_runs, missing_no_mgt)

            directory = check_make_directory(app.config['BASE_DIR'])
            filename = get_fvs_monster_name(directory)
            file = join(directory, filename)
            pdf.output(file, 'F')
            flash = f'Successfully created FVS Thinning Report at [ {file} ]'

        else:
            if request.form['data_from_previous_stand'] == 'yes':
                return redirect(url_for('rfrs_stand', stand_ref=request.form['stand_select']))
            elif request.form['export_blank_sheet_text'] == 'yes':
                directory = check_make_directory(app.config['BASE_DIR'])
                filename = get_blank_sheet_filename(directory)
                file = join(directory, filename)
                export_blank_RFRS_sheet(file)
                flash = f'Successfully created Blank RFRS Sheet at [ {file} ]'

            else:
                no_form_errors, table_body, added_stands, flash = check_form_data(request.form, rfrs_stands=app.config['RFRS_STANDS'])
                if no_form_errors:
                    app.config['RFRS_STANDS'] = process_stands_from_table(app.config['ORM'], table_body, added_stands)
                    flash = f'Added Stands Successfully, you can now select the stand in the Previous Stands dropdown below'
                    process_data_vis = 'hidden'
                    added_stands = None
                else:
                    process_data_vis = 'visible'

    return render_template('rfrs.html', const=app.config['CONSTANTS'], table_body=table_body, process_data_vis=process_data_vis,
                           rfrs_stands=app.config['RFRS_STANDS'], added_stands=added_stands, flash=flash)


@app.route('/rfrs_stand_<stand_ref>', methods=['POST', 'GET'])
def rfrs_stand(stand_ref):
    stand = {stand.ref_stand: stand for stand in app.config['RFRS_STANDS']}[stand_ref]
    tt_stand = stand.create_tt_stand()

    flash = None
    table_body = None
    report = None

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.form['data_from_sheet_text'] == 'yes':
            error, flash = append_stand_from_sheet(request.files['data_file'], stand)
            if not error:
                app.config['RFRS_STANDS'] = app.config['ORM'].select_all_rfrs_stands()
                stand = {stand.ref_stand: stand for stand in app.config['RFRS_STANDS']}[stand_ref]
                flash = f'Stand {stand.stand} successfully appended'
                table_body = get_table_from_previous_stand(stand)
        else:
            if request.form['view_plot_data_text'] == 'yes':
                table_body = get_table_from_previous_stand(stand)

            elif request.form['view_report_text'] == 'yes':
                report = html_report_output(tt_stand)

            elif request.form['delete_stand_text'] == 'yes':
                for table in stand.table_rows:
                    app.config['ORM'].delete(RfrsTable, table.ref)
                app.config['ORM'].delete(RfrsStand, stand.ref)
                del stand
                app.config['RFRS_STANDS'] = app.config['ORM'].select_all_rfrs_stands()
                return redirect(url_for('rfrs', flash_code=1))

            elif request.form['pdf_report_text'] == 'yes':
                directory = check_make_directory(app.config['BASE_DIR'])
                filename = get_stand_pdf_filename(tt_stand, directory)
                tt_stand.pdf_report(filename, directory=directory)
                flash = f'Successfully created Stand Report at [ {join(directory, filename)} ]'

            elif request.form['update_stand_text'] == 'yes':
                no_form_errors, table_body, _, flash = check_form_data(request.form)
                if no_form_errors:
                    prev_length = len(stand.table_data)
                    for i, row in enumerate(table_body):
                        if i >= prev_length:
                            kwargs = {app.config['CONSTANTS']['RFRS_HEADER'][j].lower().replace(' ', '_'): row[j]['val']
                                      for j in range(len(row))}
                            table = RfrsTable(db=app.config['DB'], ref_stand=stand.ref_stand, **kwargs)
                            table.insert_self()
                        else:
                            table = stand.table_rows[i]
                            for j, col in enumerate(row):
                                key = app.config['CONSTANTS']['RFRS_HEADER'][j].lower().replace(' ', '_')
                                table[key] = col['val']
                            table.update_self()
                    app.config['RFRS_STANDS'] = app.config['ORM'].select_all_rfrs_stands()
                    stand = {stand.ref_stand: stand for stand in app.config['RFRS_STANDS']}[stand_ref]
                    flash = f'Stand {stand.stand} successfully updated'

    return render_template('rfrs_stand.html', const=app.config['CONSTANTS'], stand=stand, table_body=table_body, report=report, flash=flash)


@app.route('/rfrs_stand_thin_<stand_ref>', methods=['POST', 'GET'])
def rfrs_stand_thin(stand_ref):
    stand = {stand.ref_stand: stand for stand in app.config['RFRS_STANDS']}[stand_ref]
    tt_stand = stand.create_tt_stand()
    stand_metrics = html_report_output(tt_stand, metrics_only=True)
    species = {table.species for table in stand.table_rows}

    flash = None
    report = None

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.form['export_report_pdf'] == 'yes':
            directory = check_make_directory(app.config['BASE_DIR'])
            thin = app.config['REPORTS']['thin']
            filename = get_thin_pdf_filename(thin, directory)
            thin.pdf_report(filename, directory=directory)
            flash = f'Successfully created Thinning Report at [ {join(directory, filename)} ]'
        else:
            no_form_errors, thinning_params, flash = check_thin_form_data(request.form)
            if no_form_errors:
                app.config['REPORTS']['thin'], report, flash = thin_stand(tt_stand, thinning_params)

    return render_template('rfrs_stand_thin.html', const=app.config['CONSTANTS'], stand=stand, species=species, stand_metrics=stand_metrics,
                           report=report, flash=flash)


@app.route('/rfrs_fvs', methods=['POST', 'GET'])
def rfrs_fvs():
    flash = None
    stand_info = None

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        dbs = request.form.getlist('dbs_to_create')
        if not dbs:
            flash = 'Please Select at least one Database Type'
            stand_info = keep_fvs_stand_info(request.form)
        else:
            error, stand_info, flash = check_fvs_form_data(request.form)
            if not error:
                flash = process_fvs_form(dbs, stand_info, app.config['RFRS_STANDS'], app.config['BASE_DIR'])
                stand_info = None

    return render_template('rfrs_fvs.html', const=app.config['CONSTANTS'], rfrs_stands=app.config['RFRS_STANDS'],
                           stand_info=stand_info, flash=flash)


@app.route('/silviculture_<sale_name>', methods=['POST', 'GET'])
def silviculture(sale_name):
    flash = None
    contract_years = 2
    sale = {s.sale_name: s for s in app.config['TIMBERSALES']}[sale_name]
    sale_units = [sale.units[u].unit_name for u in sale.units if sale.units[u].harvest == 'VRH']

    if sale.silv_report is not None:
        silv = [True, sale.silv_report.silv_report_formatted]
    else:
        silv = [False, get_silviculture_options(sale)]

    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        if request.form['rerun_report_text'] == 'yes':
            contract_years = int(request.form['contract_years'])
            silv = [False, get_silviculture_options(sale, contract_years=contract_years)]

        elif request.form['new_report_text'] == 'yes':
            contract_years = 2
            silv = [False, get_silviculture_options(sale, contract_years=contract_years)]

        else:
            mul_lists = {key: request.form.getlist(key)
                         for key in request.form
                         if key in GET_SILV_LIST_KEYS or key.split('_')[0] == 'regen=mul|units'}
            report, contract_years = process_silviculture_report(sale, request.form, mul_lists)

            if sale.silv_report is not None:
                sr = sale.silv_report
                sr.silv_report = report
                sr.silv_report_formatted = sr.format_silv_report()
                sr.update_self()
            else:
                sr = Silviculture(db=app.config['DB'], sale_ref=sale.ref, contract_years=contract_years, silv_report=report)
                sr.insert_self()
                sale.silv_report = sr

            silv = [True, sale.silv_report.silv_report_formatted]

    return render_template('silviculture.html', const=app.config['CONSTANTS'], sale=sale, silv=silv, sale_units=sale_units,
                           contract_years=contract_years, flash=flash)


@app.route('/lrm_vol_<sale_name>', methods=['POST', 'GET'])
def lrm_vol(sale_name):
    flash = None
    sale = {s.sale_name: s for s in app.config['TIMBERSALES']}[sale_name]
    target = ''
    con_pct = None
    units = None
    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        con_pct = int(request.form['con_pct'])
        error, target, units, flash = is_err_calculate_lrm_vol(sale, request.form['target_volume'], con_pct)

    return render_template('lrm_vol.html', const=app.config['CONSTANTS'], sale=sale, flash=flash, target=target,
                           units=units, con_pct=con_pct)


@app.route('/presales_<sale_name>', methods=['POST', 'GET'])
def presales(sale_name):
    flash = None
    sale = {s.sale_name: s for s in app.config['TIMBERSALES']}[sale_name]
    if request.method == 'POST':
        if 'readonly' in request.form:
            change_readonly(app, request.form['readonly'])
            return redirect(request.url)
        update_presales(sale.presales, request.form)
        flash = 'Activities Updated Successfully'

    return render_template('presales.html', const=app.config['CONSTANTS'], sale=sale, flash=flash)


@app.route('/exit_and_save')
def exit_and_save():
    try:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is not None:
            func()
    except RuntimeError:
        pass
    return 'Server is shutting down...<br /><br />You can exit the browser'


def shutdown():
    app.config['ORM'].conn.close()
    print(f"\nLOCAL DATABASE CONNECTION IS CLOSED")
    if not app.config['DEBUG'] and not app.config['READONLY']:
        if MAIN_DB is not None:
            copy_local_db_to_main(app.config['DB'], MAIN_DB)
            print(f"LOCAL DATABASE COPIED UP TO MAIN DATABASE")
    print('EXITING...')


if __name__ == '__main__':
    debug = False

    app.config['DEBUG'] = debug
    app.config['READONLY'] = True

    if debug:
        # TESTING
        MAIN_DIR = None
        MAIN_DB = None
        BASE_DIR = Path(getcwd())
        LOCAL_DB = Path(join(BASE_DIR, 'TIMBER_DB.db'))

    else:
        # TRY CONNECTING TO J: DRIVE
        try:
            # PRODUCTION
            MAIN_DIR = Path('J:/SHARED/TimberSales/Snoqualmie/TIMBER_PLANNER/') # HARDCODED
            MAIN_DB = join(MAIN_DIR, 'TIMBER_DB.db')################################################# CHANGE 1
            BASE_DIR = get_desktop_path()
            LOCAL_DB = check_make_copy_directory_for_local_db(MAIN_DB)
            print(f"MAIN DATABASE COPIED DOWN TO LOCAL DATABASE")
        except FileNotFoundError:
            print('CONNECTION ERROR, COULD NO CONNECT TO THE J: DRIVE.\nPLEASE CONNECT TO THE INTERNET AND/OR VPN AND TRY AGAIN.')
            input('\nPress any key to exit...')
            exit()

    # REGISTERING AT-EXIT FUNCTION
    register(shutdown)

    app.config['BASE_DIR'] = BASE_DIR
    app.config['DB'] = LOCAL_DB
    app.config['ORM'] = ORM(LOCAL_DB)

    print(f"CONNECTED TO LOCAL DATABASE\n")

    if not debug:
        check_backup(MAIN_DIR, app.config['DB'])

    app.config['TIMBERSALES'] = app.config['ORM'].select_all_sales()
    app.config['RFRS_STANDS'] = app.config['ORM'].select_all_rfrs_stands()
    app.config['CONSTANTS'] = {
        'FISCAL_YEARS': {sale.fy for sale in app.config['TIMBERSALES']},
        'UNIT_HEADER': UNIT_HEADER,
        'SALE_INFO_LABELS': SALE_INFO_LABELS,
        'RFRS_HEADER': RFRS_SHEET_HEADER,
        'FOREST_BLOCKS': FOREST_BLOCKS,
        'SILV_IGNORE_KEYS': ['contract_expires', 'surv_assess', 'stocking', 'veg_comp'],
        'READONLY': app.config['READONLY']
    }
    app.config['FILTERS'] = {
        'forest': 'all',
        'mbf': 'all',
        'mbf_ac': 'all',
        'value_mbf': 'all',
        'value': 'all',
        'value_ac': 'all'
    }
    app.config['REPORTS'] = {
        'stand': None,
        'thin': None
    }

    if debug:
        # TESTING
        app.run(debug=debug)
    else:
        # PRODUCTION
        Timer(1, open_browser).start()

        host = '0.0.0.0'
        app.run(host=host, port=5000, debug=debug)

