# This file is part of account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Configuration']


class Configuration:
    __name__ = 'account.configuration'
    __metaclass__ = PoolMeta
    default_journal_revenue = fields.Property(fields.Many2One('account.journal',
        'Account Journal Revenue', domain=[('type', '=', 'revenue')]))
    default_journal_expense = fields.Property(fields.Many2One('account.journal', 
        'Account Journal Expense', domain=[('type', '=', 'expense')]))
