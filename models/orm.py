from imports._imports_ import (
    connect,
    dumps,
    loads
)


class ORM(object):
    args = None
    exclude = None
    primary_key = None
    foreign_key = None

    def __init__(self, db, ref=None):
        self.db = db
        self.ref = ref
        # self.conn = connect(self.db, check_same_thread=False)
        # self.cur = self.conn.cursor()

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def connect_db(self):
        conn = connect(self.db)
        cur = conn.cursor()
        return conn, cur

    def sale_name_exists(self, old_sale_name, sale_name):
        if old_sale_name == sale_name:
            return False
        else:
            conn, cur = self.connect_db()
            sql = f"""SELECT sale_name FROM sales WHERE sale_name = ?"""
            cur.execute(sql, [sale_name])
            x = cur.fetchone()
            conn.close()
            if x is None:
                return False
            else:
                return True

    def get_last_primary(self, cls):
        conn, cur = self.connect_db()
        table = f'{cls.__name__.lower()}s'
        primary_key = cls.primary_key
        sql = f"""SELECT {primary_key} FROM {table}"""
        cur.execute(sql)
        data = cur.fetchall()
        conn.close()
        return data[-1][0]

    def select(self, cls: object, primary_value: object) -> object:
        conn, cur = self.connect_db()
        table = f'{cls.__name__.lower()}s'
        primary_key = cls.primary_key
        sql = f"""SELECT * FROM {table} WHERE {primary_key} = ?"""
        cur.execute(sql, [primary_value])
        data = cur.fetchone()
        conn.close()
        args = [self.db]
        for i in data:
            if isinstance(i, bytes):
                args.append(loads(i))
            else:
                args.append(i)
        return_class = cls(*args)
        return return_class

    def select_all_sales(self):
        conn, cur = self.connect_db()
        cls = {i.__name__: i for i in ORM.__subclasses__()}['Sale']
        sql = f"""SELECT * FROM sales"""
        cur.execute(sql)
        sales = cur.fetchall()
        conn.close()
        master = []
        for s in sales:
            args = [self.db]
            for i in s:
                if isinstance(i, bytes):
                    args.append(loads(i))
                else:
                    args.append(i)
            sale = cls(*args)
            sale.set_other_attrs()
            sale.set_sale_info()
            sale.set_presales()
            master.append(sale)
        master = sorted(master, key=lambda x: x.auction_date)
        return master

    def select_all_rfrs_stands(self):
        conn, cur = self.connect_db()
        stand_cls = {i.__name__: i for i in ORM.__subclasses__()}['RfrsStand']
        table_cls = {i.__name__: i for i in ORM.__subclasses__()}['RfrsTable']
        sql = f"""SELECT * FROM rfrsstands"""
        cur.execute(sql)
        stands = cur.fetchall()

        master = []
        for stand_args in stands:
            args = [self.db] + list(stand_args)
            stand = stand_cls(*args)
            sql = f"""SELECT * FROM rfrstables WHERE ref_stand = ?"""
            cur.execute(sql, [stand.ref_stand])
            tables = cur.fetchall()
            stand.table_rows = []
            stand.table_data = []
            for table_args in tables:
                t_args = [self.db] + list(table_args)
                table = table_cls(*t_args)
                table.set_table_row()
                stand.table_rows.append(table)
                stand.table_data.append(table.table_row)
            master.append(stand)
        conn.close()
        master = sorted([i for i in master], key=lambda x: x.ref, reverse=True)
        return master

    def delete(self, cls, primary_value):
        conn, cur = self.connect_db()
        table = f'{cls.__name__.lower()}s'
        primary_key = cls.primary_key

        sql = f"""DELETE FROM {table} WHERE {primary_key} = ?"""
        cur.execute(sql, [primary_value])
        conn.commit()
        conn.close()

    def insert_self(self):
        conn, cur = self.connect_db()
        table = f'{self.__class__.__name__.lower()}s'
        args = [i for i in self.args if i not in self.exclude]
        d = self.__dict__
        vals = []
        for key in d:
            if key not in self.exclude:
                if self.args[key] == 'BLOB':
                    vals.append(dumps(d[key]))
                else:
                    vals.append(d[key])
        sql = f"""INSERT into {table} ({', '.join(args)}) VALUES ({', '.join(['?' for _ in vals])})"""
        cur.execute(sql, vals)
        conn.commit()
        conn.close()

    def update_self(self):
        conn, cur = self.connect_db()
        table = f'{self.__class__.__name__.lower()}s'
        primary_key = self.primary_key
        args = [i for i in self.args if i not in self.exclude]
        d = self.__dict__
        vals = []
        for key in d:
            if key not in self.exclude:
                if self.args[key] == 'BLOB':
                    vals.append(dumps(d[key]))
                else:
                    vals.append(d[key])
        sql = f"""UPDATE {table}
                  SET ({', '.join(args)}) = ({', '.join(['?' for _ in vals])})
                  WHERE {primary_key} = ?;"""
        vals.append(self[primary_key])
        cur.execute(sql, vals)
        conn.commit()
        conn.close()

    @staticmethod
    def create_tables(db):
        conn = connect(db)
        cur = conn.cursor()
        subs = sorted(ORM.__subclasses__(), key=lambda x: x.__name__)
        print(subs)
        for cls in subs:
            table = f'{cls.__name__.lower()}s'
            fk = cls.foreign_key
            if fk:
                add = f""" , FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]} ({fk[2]})"""
            else:
                add = ''
            cols = f"""({', '.join([f'{key} {cls.args[key]}' for key in cls.args])}, PRIMARY KEY ({cls.primary_key}){add});"""
            sql = f"""CREATE TABLE {table} {cols}"""
            print(sql)
            cur.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def create_table(db, cls):
        conn = connect(db)
        cur = conn.cursor()
        table = f'{cls.__name__.lower()}s'
        fk = cls.foreign_key
        if fk:
            add = f""" , FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]} ({fk[2]})"""
        else:
            add = ''
        cols = f"""({', '.join([f'{key} {cls.args[key]}' for key in cls.args])}, PRIMARY KEY ({cls.primary_key}){add});"""
        sql = f"""CREATE TABLE {table} {cols}"""
        print(sql)
        cur.execute(sql)
        conn.commit()
        conn.close()






