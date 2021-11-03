from utils.config_utils import *

FOREST_BLOCKS = ['MARCKWORTH', 'TIGER MOUNTAIN', 'RAGING RIVER', 'CCC FLATS', 'MIDDLE FORK', 'MITCHELL HILL', 'ECHO GLEN']

SALES_SEARCH_HEADER = {
    'checkbox': {
        'head': 'checkbox',
        'func': None
    },
    'sale_name': {
        'head': 'SALE NAME',
        'func': str
    },
    'fy': {
        'head': 'FISCAL YEAR',
        'func': int,
    },
    'due_date': {
        'head': 'DUE DATE',
        'func': f_date
    },
    'auction_date': {
        'head': 'AUCTION DATE',
        'func': f_date
    },
    'mbf': {
        'head': 'MBF',
        'func': f_round
    },
    'acres': {
        'head': 'ACRES',
        'func': f_round
    },
    'mbf_ac': {
        'head': 'MBF PER ACRE',
        'func': f_round
    },
    'value_mbf': {
        'head': '$ PER MBF',
        'func': f_price
    },
    'value': {
        'head': '$ SALE',
        'func': f_price
    },
    'value_ac': {
        'head': '$ PER ACRE',
        'func': f_price
    }
}

SALE_DISPLAY = {
    'due_date': f_date,
    'auction_date': f_date,
    'value': f_price,
    'value_mbf': f_price,
    'value_ac': f_price,
    'mbf': f_round,
    'acres': f_round,
    'mbf_ac': f_round,
    'lrm_spatial': f_bool,
    'cruised': f_bool,
    'pruchased': f_bool
}

SALE_DISPLAY_DATE = ['due_date', 'auction_date']
SALE_DISPLAY_PRICE = ['value', 'value_mbf', 'value_ac']
SALE_DISPLAY_ROUND = ['mbf', 'acres', 'mbf_ac']
SALE_DISPLAY_BOOL = ['lrm_spatial', 'cruised', 'purchased']

FILTERS = {
    'forest': {
        'show': 'FOREST BLOCK',
        'step': None,
        'funcs': None
    },
    'mbf': {
        'show': 'MBF',
        'step': 1000,
        'funcs': [int, int]
    },
    'mbf_ac': {
        'show': 'MBF PER ACRE',
        'step': 5,
        'funcs': [int, int]
    },
    'value_mbf': {
        'show': '$ PER MBF',
        'step': 50,
        'funcs': [f_price, f_round]
    },
    'value': {
        'show': '$ SALE',
        'step': 500_000,
        'funcs': [f_price, f_round]
    },
    'value_ac': {
        'show': '$ PER ACRE',
        'step': 5000,
        'funcs': [f_price, f_round]
    }
}

FILTER_HEADS = ['-FOREST BLOCK-', '-MBF-', '-MBF PER ACRE-', '-$ PER MBF-', '-$ SALE-', '-$ PER ACRE-']

SALE_INFO_LABELS = {
    'sale_name': {
        'head': 'SALE NAME',
        'editable': True,
        'func': str,
        'val': None,
        'type': 'text',
        'err': False
    },
    'forest': {
        'head': 'FOREST BLOCK',
        'editable': True,
        'func': str,
        'val': None,
        'type': 'select',
        'err': False
    },
    'due_date': {
        'head': 'DUE DATE',
        'editable': True,
        'func': h_date,
        'val': None,
        'type': 'date',
        'err': False
    },
    'value_mbf': {
        'head': '$ PER MBF',
        'editable': True,
        'func': f_round,
        'val': None,
        'type': 'text',
        'err': False
    },
    'lrm_spatial': {
        'head': 'LRM SPATIAL UPDATE',
        'editable': True,
        'func': f_bool,
        'val': None,
        'type': 'text',
        'err': False
    },
    'cruised': {
        'head': 'CRUISED',
        'editable': True,
        'func': f_bool,
        'val': None,
        'type': 'text',
        'err': False
    },
    'purchased': {
        'head': 'PURCHASED',
        'editable': True,
        'func': f_bool,
        'val': None,
        'type': 'text',
        'err': False
    },
    'fy': {
        'head': 'FISCAL YEAR',
        'editable': False,
        'func': str,
        'val': None
    },
    'auction_date': {
        'head': 'AUCTION DATE',
        'editable': False,
        'func': f_date,
        'val': None
    },
    'mbf': {
        'head': 'MBF',
        'editable': False,
        'func': f_round,
        'val': None
    },
    'acres': {
        'head': 'ACRES',
        'editable': False,
        'func': f_round,
        'val': None
    },
    'mbf_ac': {
        'head': 'MBF PER ACRE',
        'editable': False,
        'func': f_round,
        'val': None
    },
    'value': {
        'head': '$ SALE',
        'editable': False,
        'func': f_price,
        'val': None
    },
    'value_ac': {
        'head': '$ PER ACRE',
        'editable': False,
        'func': f_price,
        'val': None
    }
}

UNIT_HEADER = {'': {'head': None,
                    'subs': None},

               'unit_name': {'head': 'UNIT',
                             'subs': None},

               'harvest': {'head': 'HARVEST',
                           'subs': None},

               1: {'head': 'TRUST 01',
                   'subs': ['ACRES', 'MBF']},

               3: {'head': 'TRUST 03',
                   'subs': ['ACRES', 'MBF']},

               6: {'head': 'TRUST 06',
                   'subs': ['ACRES', 'MBF']},

               7: {'head': 'TRUST 07',
                   'subs': ['ACRES', 'MBF']},

               8: {'head': 'TRUST 08',
                   'subs': ['ACRES', 'MBF']},

               9: {'head': 'TRUST 09',
                   'subs': ['ACRES', 'MBF']},

               10: {'head': 'TRUST 10',
                    'subs': ['ACRES', 'MBF']},

               11: {'head': 'TRUST 11',
                    'subs': ['ACRES', 'MBF']},

               12: {'head': 'TRUST 12',
                    'subs': ['ACRES', 'MBF']},

               77: {'head': 'TRUST 77',
                    'subs': ['ACRES', 'MBF']},
               }


TRUSTS_DICT = {
    1: {
        'acres': 0, 'mbf': 0},
    3:
        {'acres': 0, 'mbf': 0},
    6:
        {'acres': 0, 'mbf': 0},
    7:
        {'acres': 0, 'mbf': 0},
    8:
        {'acres': 0, 'mbf': 0},
    9:
        {'acres': 0, 'mbf': 0},
    10:
        {'acres': 0, 'mbf': 0},
    11:
        {'acres': 0, 'mbf': 0},
    12:
        {'acres': 0, 'mbf': 0},
    77:
        {'acres': 0, 'mbf': 0}
}

TRUSTS_REV_SPLIT = {
    1: 0.28,
    3: 0.31,
    6: 0.31,
    7: 0.31,
    8: 0.31,
    9: 0.31,
    10: 0.31,
    11: 0.31,
    12: 0.31,
    77: 0.28
}


PURCHASER_SALES_BID_DICT = {'acres': None,
                            'mbf': None,
                            'mbf_ac': None,
                            'min_bid': None,
                            'real_bid': None,
                            'winner': None}

AUCTION_DICT = {'min_bid': None,
                'win_bid': None,
                'purchaser_bids': {}}


UNITS_TABLE_BODY = {
    'checkbox': {
        'name': 'cbx_{}'
    },
    'unit_name': {
        'name': 'U_attr_{}_unit_name',
        'val': None,
        'err': False
    },
    'harvest': {
        'name': 'U_attr_{}_harvest',
        'val': None,
        'err': False
    },
    'trusts': []
}

UNITS_TABLE_BODY_TRUST = {
    'name': 'U_trust_{}_{}_{}',
    'val': None,
    'err': False
}

RFRS_SHEET_HEADER = ['STAND', 'PLOT', 'TREE', 'SPECIES', 'DBH', 'TOTAL HEIGHT']

RFRS_STAND_METRIC_HEADER = [['tpa', 'TPA'], ['ba_ac', 'BASAL AREA'], ['rd_ac', 'RD'], ['qmd', 'QMD'], ['vbar', 'VBAR'],
                            ['avg_hgt', 'AVG HEIGHT'], ['hdr', 'HDR'], ['bf_ac', 'BOARD FEET'], ['cf_ac', 'CUBIC FEET']]

RFRS_LOG_LENGTHS = {
    '<= 10 feet': (1, 10),
    '11 - 20 feet': (11, 20),
    '21 - 30 feet': (21, 30),
    '31 - 40 feet': (31, 40),
    '> 40 feet': (41, 999)
}

RFRS_ALL_SPECIES_NAMES = {
    'DF': 'DOUGLAS-FIR',
    'WH': 'WESTERN HEMLOCK',
    'RC': 'WESTERN REDCEDAR',
    'SS': 'SITKA SPRUCE',
    'ES': 'ENGLEMANN SPRUCE',
    'SF': 'SILVER FIR',
    'GF': 'GRAND FIR',
    'NF': 'NOBLE FIR',
    'WL': 'WESTERN LARCH',
    'WP': 'WHITE PINE',
    'PP': 'PONDEROSA PINE',
    'LP': 'LODGEPOLE PINE',
    'JP': 'JEFFERY PINE',
    'SP': 'SUGAR PINE',
    'WF': 'WHITE FIR',
    'RF': 'RED FIR',
    'RW': 'COASTAL REDWOOD',
    'IC': 'INSENCE CEDAR',
    'RA': 'RED ALDER',
    'BM': 'BIGLEAF MAPLE',
    'CW': 'BLACK COTTONWOOD',
    'AS': 'QUAKING ASPEN'
}

RFRS_GRADE_SORT = {
    'P3': 0,
    'SM': 1,
    'S1': 2,
    'S2': 3,
    'S3': 4,
    'S4': 5,
    'S5': 6,
    'S6': 7,
    'UT': 8,
    'CR': 9,
    'TOTALS': 10
}

RFRS_STATS_CONVERSIONS = {
    'mean': f_round_or_blank,
    'variance': f_round_or_blank,
    'stdev': f_round_or_blank,
    'stderr': f_round_or_blank,
    'stderr_pct': f_pct,
}

RFRS_ERROR_HOLDER = {
    'name_id': None,
    'val': None,
    'err': False
}

RFRS_ERR_CHECK = {
    'STAND': is_err_check_stand_for_special_char_or_space,
    'PLOT': is_err_check_int_required,
    'TREE': is_err_check_int_required,
    'SPECIES': lambda val, col_name, row, x: [False, val.upper(), None] if val.upper() in RFRS_ALL_SPECIES_NAMES else [True, val.upper(), f'{col_name} row {row} incorrect code ({val})'],
    'DBH': is_err_check_float_required,
    'TOTAL HEIGHT': is_err_check_float_notrequired
}

RFRS_DNR_HEADS = ['PUNIT_NAME', 'PLOT', 'TREE_N', 'SPECIES', 'DBH', 'HT']
RFRS_FVS_HEADS = ['Variant', 'Forest Code', 'Region Code', 'Stand Age', 'Site Species', 'Site Index']

FOREST_LOCS = {
    'AK': ['1002', '1003', '1004', '1005'],
    'BM': ['604', '607', '614', '616', '619'],
    'CA': ['505', '506', '508', '511', '514', '518', '610', '611'],
    'CI': ['117', '402', '406', '412', '413', '414'],
    'CR': ['202', '203', '204', '206', '207', '209', '210', '212', '213', '214', '215',
           '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '312'],
    'CS': ['905', '908', '912'],
    'EC': ['603', '606', '608', '613', '617', '699'],
    'EM': ['102', '108', '109', '111', '112', '115'],
    'IE': ['103', '104', '105', '106', '110', '113', '114', '116', '117', '118', '621'],
    'LS': ['902', '903', '904', '906', '907', '909', '910', '913', '924'],
    'NC': ['505', '510', '514', '611'],
    'NE': ['914', '919', '920', '921'],
    'PN': ['609', '612'],
    'SN': ['80101', '80103', '80104', '80105', '80106', '80107', '80211', '80212', '80213', '80214', '80215', '80216', '80217',
           '80301', '80302', '80304', '80305', '80306', '80307', '80308', '80401', '80402', '80403', '80404', '80405', '80506',
           '80501', '80502', '80504', '80505', '80506', '80601', '80602', '80603', '80604', '80605',
           '80701', '80702', '80704', '80705', '80706', '80717', '80801', '80802', '80803', '80804', '80805', '80806',
           '80811', '80812', '80813', '80814', '80815', '80816', '80901', '80902', '80903', '80904', '80905', '80906',
           '80907', '80908', '80909', '80910', '80911', '80912', '81001', '81002', '81003', '81004', '81005', '81006', '81007',
           '81102', '81103', '81105', '81106', '81107', '81108', '81109', '81110', '81111', '81201', '81202', '81203', '81205',
           '81301', '81303', '81304', '81307', '81308','905', '908'],
    'SO': ['505', '506', '509', '511', '601', '602', '620'],
    'TT': ['403', '405', '415', '416'],
    'UT': ['401', '407', '408', '410', '418', '419'],
    'WC': ['603', '605', '606', '610', '615', '618'],
    'WS': ['503', '511', '513', '515', '516', '517']
}

REGION_LOCS = {
    'AK': ['10'],
    'BM': ['6'],
    'CA': ['5', '6'],
    'CI': ['1', '4'],
    'CR': ['2', '3'],
    'CS': ['9'],
    'EC': ['6'],
    'EM': ['1'],
    'IE': ['1', '6'],
    'LS': ['9'],
    'NC': ['5', '6'],
    'NE': ['9'],
    'PN': ['6'],
    'SN': ['8', '9'],
    'SO': ['5', '6'],
    'TT': ['4'],
    'UT': ['4'],
    'WC': ['6'],
    'WS': ['5']
}


def is_err_fvs_forest_region(val, key, stand, variant):
    if variant not in FOREST_LOCS:
        return True, val, None
    else:
        if key == 'Forest Code':
            check_in = FOREST_LOCS
        else:
            check_in = REGION_LOCS

        if val not in check_in[variant]:
            return True, val, f'{stand} {key} not valid code for given Variant ({variant})'
        else:
            return False, val, None


FVS_ERR_CHECK = {
    'Variant': lambda val, key, stand, x: [False, val.upper(), None] if val.upper() in FOREST_LOCS else [True, val.upper(), f'{stand} {key} not valid Variant ({val.upper()})'],
    'Forest Code': is_err_fvs_forest_region,
    'Region Code': is_err_fvs_forest_region,
    'Stand Age': is_err_fvs_int_required,
    'Site Species': lambda val, key, stand, x: [False, val.upper(), None] if val.upper() in RFRS_ALL_SPECIES_NAMES else [True, val.upper(), f'{stand} {key} not valid code ({val.upper()})'],
    'Site Index': is_err_fvs_int_required
}

FVS_SHEETS = ['FVS_Cases', 'FVS_TreeList', 'FVS_Summary', 'FVS_CutList', 'FVS_ATRTList']
FVS_SHEET_PARAMS = ['Species', 'TPA', 'DBH', 'Ht', 'BdFt']


SILVICULTURE_SUBS = {
    'target_date': None,
    'fiscal_year': None,
    'activity_type': None,
    'technique': None,
    'crew': None
}

REGEN_SUBS = {
    'species_1': 'DF',
    'stock_type_1': '1+1',
    'target_tpa_1': 330,
    'species_2': None,
    'stock_type_2': None,
    'target_tpa_2': None,
}

SLASHING_SUBS = {
    'target_species_1': 'BM',
    'target_species_2': 'CW',
    'target_species_3': 'RA',
}

PCT_SUBS = {
    'retain_species_1': 'RC',
    'retain_species_2': 'DF',
    'retain_species_3': 'WH',
    'reatin_species_4': 'RA',
    'target_tpa': 302
}
SILV_MONTH_YEAR = {
    'contract_expires': {
        'month': '10',
        'day': '31',
        'year_adj': -1
    },
    'site_prep': {
        'month': '07',
        'day': '01',
        'year_adj': 0
    },
    'regen': {
        'month': '01',
        'day': '01',
        'year_adj': 1
    },
    'surv_assess': {
        'month': '09',
        'day': '01',
        'year_adj': 1
    },
    'stocking': {
        'month': '11',
        'day': '01',
        'year_adj': 3
    },
    'veg_comp': {
        'month': '07',
        'day': '01',
        'year_adj': 4
    },
    'veg_mgmt': {
        'month': '07',
        'day': '01',
        'year_adj': 5
    },
    'vrfy_target': {
        'month': '05',
        'day': '01',
        'year_adj': 8
    },
    'pct': {
        'month': '09',
        'day': '01',
        'year_adj': 8
    },
    'low_site_vrfy_target': {
        'month': '05',
        'day': '01',
        'year_adj': 13
    },
    'low_site_pct': {
        'month': '09',
        'day': '01',
        'year_adj': 13
    },
}

KEEP_SPP_ORDER = ['W_REDCEDAR', 'DOUGLAS_FIR', 'NOBLE_FIR', 'W_HEMLOCK', 'RED_ALDER', 'PAC_SILV_FIR', 'GRAND_FIR', 'SITKA_SPRUCE',
                  'BIGLEAF_MAPL', 'B_COTTONWOOD', 'SUBALP_FIR', 'MTN_HEMLOCK', 'LODGEPOLE', 'W_WHITE_PINE', 'WHTBARK_PINE', 'PAC_MADRONE']

REMO_SPP_ORDER = ['BIGLEAF_MAPL', 'B_COTTONWOOD', 'RED_ALDER', 'BLACKBERRY', 'V_MAPLE', 'CEANTHOS', 'CHERRY', 'ELDERBERRY', 'SALMONBERRY']

VEG_MGMT_WHO = ['CONTACTOR', 'CEDAR_CRK_CC', 'LARCH_CC', 'NASELLE_CC', 'WCC', 'PRIOR_OWNER', 'DNR']

PLANT_SPP = ['DOUGLAS_FIR', 'W_REDCEDAR', 'NOBLE_FIR', 'W_HEMLOCK', 'RED_ALDER',
             'PAC_SILV_FIR', 'GRAND_FIR', 'SITKA_SPRUCE', 'W_WHITE_PINE', 'WHTBARK_PINE']

STOCK_TYPE = ['1+1', 'P+1', 'P+0', 'P+P1', '2+0', 'P+1/2', 'P2+0', 'NATURAL']

REGEN_OBJ = ['MERCH_STAND', 'RESTORATION']

#lab, sel, mul, add_sel, inpt

SILVICULTURE = {
    'contract_expires': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|crew': 'PURCHASER'
    },
    'site_prep': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'SITE PREP',
        'sel|technique': ['HAND CUT', 'FOLIAR_BROAD', 'AERIAL_HERB', 'FOLIAR_DIRECT', 'FOLIAR_SPOT', 'GROUND_MECH', 'HACK_SQRT',
                          'THINLINE', 'LO_VOL_BASAL', 'BROAD_BURN', 'PILE_BURN', 'MASTICATION', 'HAND_PULL', 'UBURN', 'SEED_GRASS'],
        'sel|crew': VEG_MGMT_WHO,
        'mul|objective': ['REDUCE_COMP', 'REDUCE_INVASIVE', 'SLASH_DISPOSAL', 'FUELS_MGMT'],
        'mul|target_species_': REMO_SPP_ORDER
    },
    'regen': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'REGEN',
        'sel|technique': ['HAND PLANT', 'NATURAL'],
        'sel|crew': VEG_MGMT_WHO,
        'mul|objective': REGEN_OBJ,
        'mul|units_1': None,
        'addsel|species_1': PLANT_SPP,
        'addsel|stock_type_1': STOCK_TYPE,
        'inpt|target_tpa_1': 330,
    },
    'surv_assess': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'FOREST_SURV',
        'lab|crew': 'DNR',
        'lab|objective': 'MONITORING'
    },
    'stocking': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'FOREST_SURV',
        'lab|crew': 'DNR',
        'lab|objective': 'MONITORING'
    },
    'veg_comp': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'FOREST_SURV',
        'lab|crew': 'DNR',
        'lab|objective': 'MONITORING'
    },
    'veg_mgmt': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'VEG MGMT',
        'sel|technique': ['HAND CUT', 'THINLINE', 'LO_VOL_BASAL', 'HACK_SQRT', 'FOLIAR_BROAD', 'FOLIAR_DIRECT', 'AERIAL_HERB',
                      'MASTICATION', 'HAND_PULL', 'UBURN', 'FUELS_MGMT', 'SEED_GRASS'],
        'sel|crew': VEG_MGMT_WHO,
        'mul|objective': ['REDUCE_COMP', 'FOREST_HEALTH', 'FUELS_MGMT'],
        'mul|target_species': REMO_SPP_ORDER
    },
    'vrfy_target': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'FOREST_SURV',
        'lab|crew': 'DNR',
        'lab|objective': 'MONITORING',
        'mul|units': None
    },
    'pct': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'PCT',
        'sel|technique': ['HAND CUT', 'MASTICATION'],
        'sel|crew': VEG_MGMT_WHO,
        'mul|objective': ['IMPROVE_GROWTH', 'FOREST_HEALTH', 'FUELS_MGMT', 'HABITAT'],
        'mul|units': None,
        'mul|retain_species': KEEP_SPP_ORDER,
        'inpt|target_tpa': 302,
    },
    'low_site_vrfy_target': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'FOREST_SURV',
        'lab|crew': 'DNR',
        'lab|objective': 'MONITORING',
        'mul|units': None
    },
    'low_site_pct': {
        'lab|target_date': None,
        'lab|fiscal_year': None,
        'lab|activity_type': 'PCT',
        'sel|technique': ['HAND CUT', 'MASTICATION'],
        'sel|crew': VEG_MGMT_WHO,
        'mul|objective': ['IMPROVE_GROWTH', 'FOREST_HEALTH', 'FUELS_MGMT', 'HABITAT'],
        'mul|units': None,
        'mul|retain_species': KEEP_SPP_ORDER,
        'inpt|target_tpa': 400,
    },
}

GET_SILV_LIST_KEYS = ['site_prep=mul|objective', 'site_prep=mul|target_species_',
                      'regen=mul|objective', 'regen=mul|units_1',
                      'veg_mgmt=mul|objective', 'veg_mgmt=mul|target_species',
                      'vrfy_target=mul|units',
                      'pct=mul|objective', 'pct=mul|units', 'pct=mul|retain_species',
                      'low_site_vrfy_target=mul|units',
                      'low_site_pct=mul|objective', 'low_site_pct=mul|units', 'low_site_pct=mul|retain_species']