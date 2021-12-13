from imports._imports_ import (
    deepcopy,
    loads,
    relativedelta,
    TU
)
from config import (
    AUCTION_DICT,
    SALE_INFO_LABELS,
    TRUSTS_DICT,
    TRUSTS_REV_SPLIT,
    SILV_MONTH_YEAR
)
from utils.config_utils import (
    f_pct,
    f_round,
    f_price
)
from models.orm import ORM
from models.unit import Unit
from models.silviculture import Silviculture
from models.presale import Presale


class Sale(ORM):
    args = {
        'ref': 'INTEGER',
        'sale_name': 'TEXT',
        'fy': 'INTEGER',
        'forest': 'TEXT',
        'due_date': 'BLOB',
        'auction_date': 'BLOB',
        'value_mbf': 'REAL',
        'cruised': 'INTEGER',
        'purchased': 'INTEGER',
        'auction': 'BLOB',
        'lrm_spatial': 'INTEGER'
    }

    exclude = (
        'ref',
        'db',
        'conn',
        'cur',
        'units',
        'units_table',
        'trusts',
        'purchasers',
        'acres',
        'mbf',
        'mbf_ac',
        'value',
        'value_ac',
        'trust_summary',
        'info',
        'silv_report',
        'presales'
    )

    primary_key = 'ref'

    foreign_key = None

    def __init__(self, db=None, ref=None, sale_name=None, fy=None, forest=None, due_date=None, auction_date=None, value_mbf=0,
                 cruised=0, purchased=0, auction=deepcopy(AUCTION_DICT), lrm_spatial=None):
        super().__init__(db, ref)
        self.sale_name = sale_name
        self.fy = fy
        self.forest = forest
        self.due_date = due_date
        self.auction_date = auction_date
        self.value_mbf = value_mbf
        self.cruised = cruised
        self.purchased = purchased
        self.auction = auction
        self.lrm_spatial = lrm_spatial

        self.units = None
        self.units_table = None
        self.trusts = None

        self.acres = None
        self.mbf = None
        self.mbf_ac = None

        self.value = None
        self.value_ac = None

        self.trust_summary = None
        self.info = None
        self.silv_report = None

        self.presales = None

    def set_other_attrs(self):
        self.set_silviculture()
        self.set_units_and_trusts()

    def set_silviculture(self):
        sql = f"""SELECT * FROM silvicultures WHERE sale_ref = ?"""
        self.cur.execute(sql, [self.ref])
        silv_args = self.cur.fetchone()
        if silv_args:
            args = [self.db]
            for i in silv_args:
                if isinstance(i, bytes):
                    args.append(loads(i))
                else:
                    args.append(i)
            self.silv_report = Silviculture(*args)

    def set_units_and_trusts(self):
        sql = f"""SELECT * FROM units WHERE sale_ref = ?"""
        self.cur.execute(sql, [self.ref])
        unit_data = self.cur.fetchall()

        temp_units = {}
        self.trusts = deepcopy(TRUSTS_DICT)
        acres, mbf = 0, 0
        for u in unit_data:
            args = [self.db]
            for i in u:
                if isinstance(i, bytes):
                    args.append(loads(i))
                else:
                    args.append(i)
            unit = Unit(*args)
            temp_units[int(unit.unit_name[1:])] = unit
            for trust in unit.trusts:
                self.trusts[trust]['acres'] += unit.trusts[trust]['acres']
                self.trusts[trust]['mbf'] += unit.trusts[trust]['mbf']
                acres += unit.trusts[trust]['acres']
                mbf += unit.trusts[trust]['mbf']
        self.acres = acres
        self.mbf = mbf
        self.value = self.value_mbf * self.mbf
        if self.acres != 0:
            self.mbf_ac = self.mbf / self.acres
            self.value_ac = self.value / self.acres
        else:
            self.mbf_ac = 0
            self.value_ac = 0
        sort = sorted(temp_units)
        self.units = {key: temp_units[key] for key in sort}
        self.trust_summary = self._get_trust_summary()

    def set_presales(self):
        sql = f"""SELECT * FROM presales WHERE sale_ref = ?"""
        self.cur.execute(sql, [self.ref])
        args = [self.db] + [i for i in self.cur.fetchone()]
        self.presales = Presale(*args)

    def _get_trust_summary(self):
        master = {}
        totals = [0, 0, 0, 0]
        for trust in self.trusts:
            show = f"TRUST {'0' * (2 - len(str(trust)))}{trust}"
            if self.trusts[trust]['acres'] > 0 and self.trusts[trust]['mbf'] > 0:
                value = self.trusts[trust]['mbf'] * self.value_mbf

                acres = self.trusts[trust]['acres']
                mbf = self.trusts[trust]['mbf']
                trustee_val = value * (1 - TRUSTS_REV_SPLIT[trust])
                dnr_val = value * TRUSTS_REV_SPLIT[trust]

                master[show] = [
                    [f_round(acres), f_pct(acres / self.acres)],
                    [f_round(mbf), f_pct(mbf / self.mbf)],
                    [f_price(trustee_val), f_pct(trustee_val / self.value)],
                    [f_price(dnr_val), f_pct(dnr_val / self.value)]
                ]
                x = [acres, mbf, trustee_val, dnr_val]
                for i, val in enumerate(x):
                    totals[i] += val
        master['TOTALS'] = []
        for i, val in enumerate(totals):
            if i > 1:
                master['TOTALS'].append(f_price(val))
            else:
                master['TOTALS'].append(f_round(val))
        return master

    def set_sale_info(self):
        master = {}
        for key in SALE_INFO_LABELS:
            master[key] = deepcopy(SALE_INFO_LABELS[key])
            master[key]['val'] = master[key]['func'](self[key])
        self.info = master

    def rerun_silv_fys(self):
        master = self.silv_report.silv_report
        for key in master:
            month = SILV_MONTH_YEAR[key]['month']
            day = SILV_MONTH_YEAR[key]['day']
            year = self.fy + self.silv_report.contract_years + SILV_MONTH_YEAR[key]['year_adj']
            master[key]['lab|target_date'] = f'{month}/{day}/{year}'
            master[key]['lab|fiscal_year'] = self.get_fy(month, year)
        self.silv_report.silv_report_formatted = self.silv_report.format_silv_report()
        self.silv_report.update_self()

    def get_auction_date(self):
        auction = self.due_date + relativedelta(months=+6)
        auction_month = auction.month

        for i in range(1, 6):
            last_tuesday = auction + relativedelta(weekday=TU(i))
            if last_tuesday.month != auction_month:
                last_tuesday += relativedelta(weekday=TU(-2))
        return last_tuesday

    def get_fy(self, month, year):
        keep_year = [1, 2, 3, 4, 5, 6]
        if month in keep_year:
            return year
        else:
            return year + 1

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
        self.value = self.value_mbf * self.mbf
        if self.acres != 0:
            self.mbf_ac = self.mbf / self.acres
            self.value_ac = self.value / self.acres
        else:
            self.mbf_ac = 0
            self.value_ac = 0

    def update_after_edit(self):
        self.set_other_attrs()
        self.auction_date = self.get_auction_date()
        self.fy = self.get_fy(self.auction_date.month, self.auction_date.year)
        if self.silv_report is not None:
            self.rerun_silv_fys()
        self.set_sale_info()
        self.update_self()





