# This file is part of account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Party']


class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta
    journal_revenue = fields.Many2One(
        'account.journal', 'Account Journal Revenue',
        domain=[('type', '=', 'revenue')])
    journal_expense = fields.Many2One(
        'account.journal', 'Account Journal Expense',
        domain=[('type', '=', 'expense')])
