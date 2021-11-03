from imports._imports_ import deepcopy
from config import TRUSTS_DICT
from models.orm import ORM


class Unit(ORM):
    args = {'ref': 'INTEGER',
            'sale_ref': 'INTEGER',
            'unit_name': 'TEXT',
            'harvest': 'TEXT',
            'trusts': 'BLOB'}

    exclude = (
        'ref',
        'sales_ref',
        'db',
        'conn',
        'cur',
        'acres',
        'mbf',
        'mbf_ac'
    )

    primary_key = 'ref'

    foreign_key = ('sale_ref', 'sales', 'ref')

    def __init__(self, db=None, ref=None, sale_ref=None, unit_name=None, harvest=None, trusts=deepcopy(TRUSTS_DICT)):
        super().__init__(db, ref)
        self.sale_ref = sale_ref
        self.unit_name = unit_name
        self.harvest = harvest
        self.trusts = trusts

        self.db = None
        self.acres = self.calc_acres()
        self.mbf = self.calc_mbf()
        self.mbf_ac = self.calc_mbf_ac()

    def calc_acres(self):
        acres = 0
        for trust in self.trusts:
            acres += self.trusts[trust]['acres']
        return acres

    def calc_mbf(self):
        mbf = 0
        for trust in self.trusts:
            mbf += self.trusts[trust]['mbf']
        return mbf

    def calc_mbf_ac(self):
        if self.acres != 0:
            return self.mbf / self.acres
        else:
            return 0

    def calc_all_stats(self):
        acres, mbf = 0, 0
        for trust in self.trusts:
            acres += self.trusts[trust]['acres']
            mbf += self.trusts[trust]['mbf']

        self.acres = acres
        self.mbf = mbf
        if self.acres != 0:
            self.mbf_ac = self.mbf / self.acres
        else:
            self.mbf_ac = 0

    def update_after_edit(self):
        self.calc_all_stats()
        self.update_self()



