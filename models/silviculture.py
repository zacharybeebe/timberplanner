from imports._imports_ import deepcopy
from models.orm import ORM


class Silviculture(ORM):
    args = {
        'ref': 'INTEGER',
        'sale_ref': 'INTEGER',
        'contract_years': 'INTEGER',
        'silv_report': 'BLOB'
    }

    exclude = (
        'ref',
        'db',
        'conn',
        'cur',
        'silv_report_formatted'
    )

    primary_key = 'ref'

    foreign_key = ('sale_ref', 'sales', 'ref')

    def __init__(self, db=None, ref=None, sale_ref=None, contract_years=None, silv_report=None):
        super().__init__(db, ref)
        self.sale_ref = sale_ref
        self.contract_years = contract_years
        self.silv_report = silv_report
        if silv_report:
            self.silv_report_formatted = self.format_silv_report()
        else:
            self.silv_report_formatted = None

    def format_silv_report(self):
        silv_report = deepcopy(self.silv_report)
        master = {}
        for key in silv_report:
            master[key] = {}
            for sub in silv_report[key]:
                if isinstance(silv_report[key][sub], list):
                    master[key][sub] = '  |  '.join(silv_report[key][sub])
                else:
                    master[key][sub] = silv_report[key][sub]
        return master



