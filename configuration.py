# This file is part of account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval

from trytond.modules.company.model import CompanyValueMixin


class Configuration(metaclass=PoolMeta):
    __name__ = 'account.configuration'
    default_journal_revenue = fields.MultiValue(fields.Many2One(
            'account.journal', "Account Journal Revenue",
            domain=[('type', '=', 'revenue')]))
    default_journal_expense = fields.MultiValue(fields.Many2One(
            'account.journal', "Account Journal Expense",
            domain=[('type', '=', 'expense')]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'default_journal_revenue', 'default_journal_expense'}:
            return pool.get('account.configuration.default_journal')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationDefaultJournal(ModelSQL, CompanyValueMixin):
    "Account Configuration Default Journal"
    __name__ = 'account.configuration.default_journal'
    default_journal_revenue = fields.Many2One(
        'account.journal', "Account Journal Revenue",
        domain=[('type', '=', 'revenue')],  context={
            'company': Eval('company', -1),
            }, depends=['company'])
    default_journal_expense = fields.Many2One(
        'account.journal', "Account Journal Expense",
        domain=[('type', '=', 'expense')], context={
            'company': Eval('company', -1),
            }, depends=['company'])
