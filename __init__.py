# This file is part account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .configuration import *
from .invoice import *
from .party import *

def register():
    Pool.register(
        Configuration,
        Invoice,
        Party,
        module='account_invoice_journal_party', type_='model')
