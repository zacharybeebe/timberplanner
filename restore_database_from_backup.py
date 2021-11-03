from os import (
    getcwd,
    mkdir
)
from os.path import (
    join,
    isfile,
    isdir,
    getctime
)
from datetime import datetime
from shutil import copyfile


def get_last_backup_time(base_directory):
    sub = join(base_directory, 'backups')
    filepath = join(sub, 'backup.db')
    if isfile(filepath):
        created = getctime(filepath)
        dt = datetime.fromtimestamp(created)
        return False, f'{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute}'
    else:
        return True, f'No current database backup, open the TimberPlanner program and one will be created automatically'


def check_make_backup_directory(base_directory):
    sub_dir = 'backups'
    sub = join(base_directory, sub_dir)
    if not isdir(sub):
        mkdir(sub)
    return sub


def restore_backup(base_directory, db_to_restore):
    sub = check_make_backup_directory(base_directory)
    filepath = join(sub, 'backup.db')
    copyfile(filepath, db_to_restore)


if __name__ == '__main__':
    current_dir = getcwd()
    main_database = join(current_dir, 'TIMBER_DB.db')
    error, last_backup_time = get_last_backup_time(current_dir)

    if error:
        print(f'\n{last_backup_time}')
    else:
        print(f'\nLast Backup created at {last_backup_time}')

        run_restore = input(f'\nWould you like to restore the main database from this backup (y/n) [n]?:  ')

        if run_restore.upper() == 'Y':
            restore_backup(current_dir, main_database)
            flash = f'\nMain Database successfully restored from backup ({last_backup_time})\n.'
        else:
            flash = '\nMain Database not backed up\n'

        print(flash)
    input('\nPress any key to exit')
