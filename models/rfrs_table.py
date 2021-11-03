from models.orm import ORM


class RfrsTable(ORM):
    args = {
        'ref': 'INTEGER',
        'ref_stand': 'INTEGER',
        'stand': 'TEXT',
        'plot': 'INTEGER',
        'tree': 'INTEGER',
        'species': 'TEXT',
        'dbh': 'REAL',
        'total_height': 'REAL'
    }

    exclude = (
        'ref',
        'db',
        'conn',
        'cur',
        'table_row'
    )

    primary_key = 'ref'

    foreign_key = ('ref_stand', 'rfrs_stands', 'ref_stand')

    def __init__(self, db=None, ref=None, ref_stand=None, stand=None, plot=None, tree=None, species=None, dbh=None, total_height=None):
        super().__init__(db, ref)
        self.ref_stand = ref_stand
        self.stand = stand
        self.plot = plot
        self.tree = tree
        self.species = species
        self.dbh = dbh
        self.total_height = total_height

        self.table_row = None

    def set_table_row(self):
        self.table_row = [self.__dict__[key] for key in self.__dict__ if key not in self.exclude and key != 'ref_stand']
