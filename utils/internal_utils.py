from imports._imports_ import (
    copyfile,
    getctime,
    environ,
    expanduser,
    listdir,
    mkdir,
    exists,
    isfile,
    join,
    datetime,
    timedelta,
    open_new,
    Path
)
from utils.config_utils import check_make_backup_directory


def open_browser():
    open_new('http://localhost:5000/')


def get_last_backup_time(base_directory):
    sub = join(base_directory, 'backups')
    filepath = join(sub, 'backup.db')
    if isfile(filepath):
        created = getctime(filepath)
        dt = datetime.fromtimestamp(created)
        return f'{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute}'
    else:
        return f'No current database backup, open the TimberPlanner program and one will be created automatically'


def check_backup(main_directory, db_to_backup):
    today = datetime.today()
    sub = check_make_backup_directory(main_directory)
    filepath = join(sub, f'backup_{today.month}_{today.day}_{today.year}.db')
    if not isfile(filepath):
        file_dates = [datetime.fromtimestamp(getctime(Path(join(sub, f)))) for f in listdir(sub) if isfile(join(sub, f))]
        if file_dates:
            last_backup_date = max(file_dates)
            if today - timedelta(days=4) >= last_backup_date:
                copyfile(db_to_backup, filepath)
        else:
            copyfile(db_to_backup, filepath)


def restore_backup(base_directory, db_to_restore):
    sub = check_make_backup_directory(base_directory)
    filepath = join(sub, 'backup.db')
    copyfile(filepath, db_to_restore)


def check_make_copy_directory_for_local_db(main_db_path):
    dir_path = join(environ['APPDATA'], 'TimberPlanner')
    if not exists(dir_path):
        mkdir(dir_path)
    file_path = Path(join(dir_path, 'TIMBER_DB.db'))
    copyfile(main_db_path, file_path)
    return file_path


def copy_local_db_to_main(local_db_path, main_db_path):
    copyfile(local_db_path, main_db_path)


def get_desktop_path():
    return Path(join(expanduser('~'), 'desktop'))








