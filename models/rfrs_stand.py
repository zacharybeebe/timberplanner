from imports._imports_ import (
    mean,
    Stand,
    Plot,
    TimberQuick
)
from models.orm import ORM
from models.rfrs_table import RfrsTable


class RfrsStand(ORM):
    args = {
        'ref': 'INTEGER',
        'stand': 'TEXT',
        'ref_stand': 'TEXT',
        'plot_factor': 'REAL'
    }

    exclude = (
        'ref',
        'db',
        'conn',
        'cur',
        'table_rows',
        'table_data'
    )

    primary_key = 'ref'

    foreign_key = None

    def __init__(self, db=None, ref=None, stand=None, ref_stand=None, plot_factor=None):
        super().__init__(db, ref)
        self.stand = stand.upper()
        self.ref_stand = ref_stand #Unique
        self.plot_factor = plot_factor

        self.table_rows = None
        self.table_data = None

    def select_rfrs_stand(self, stand_name):
        conn, cur = self.connect_db()
        sql = f"""SELECT * FROM {f'{RfrsStand.__name__.lower()}s'} WHERE stand = ?"""
        cur.execute(sql, [stand_name])
        args = [self.db] + list(cur.fetchone())

        stand = RfrsStand(*args)
        sql = f"""SELECT * FROM rfrstables WHERE ref_stand = ?"""
        cur.execute(sql, [stand.ref_stand])
        tables = cur.fetchall()
        conn.close()

        stand.table_rows = []
        stand.table_data = []
        for table_args in tables:
            t_args = [self.db] + list(table_args)
            table = RfrsTable(*t_args)
            table.set_table_row()
            stand.table_rows.append(table)
            stand.table_data.append(table.table_row)
        return stand

    def create_tt_stand(self):
        stand = Stand(self.stand, self.plot_factor)
        hdr = mean([row[-1] / (row[-2] / 12) for row in self.table_data if row[-1]])

        plot = Plot()
        for i, row in enumerate(self.table_data):
            if i > 0:
                if row[1] != self.table_data[i-1][1]:
                    stand.add_plot(plot)
                    plot = Plot()
            if row[-1]:
                args = [self.plot_factor] + row[3:]
            else:
                args = [self.plot_factor] + row[3:-1] + [round((row[-2] / 12) * hdr, 1)]
            plot.add_tree(TimberQuick(*args))
        stand.add_plot(plot)
        return stand







