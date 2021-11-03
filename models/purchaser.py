from models.orm import ORM


class Purchaser(ORM):
    args = {'ref': 'INTEGER',
            'purchaser_name': 'TEXT',
            'sales_bid': 'BLOB'}

    exclude = (
        'ref',
        'db'
        'conn',
        'cur',
    )

    primary_key = 'ref'

    foreign_key = None

    def __init__(self, db=None, ref=None, purchaser_name=None, sales_bid=None):
        super().__init__(db, ref)
        self.purchaser_name = purchaser_name
        self.sales_bid = sales_bid



