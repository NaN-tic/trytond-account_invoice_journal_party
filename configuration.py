# This file is part of account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond import backend
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta, Pool
from trytond.tools.multivalue import migrate_property

from trytond.modules.company.model import CompanyValueMixin

__all__ = ['Configuration']


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
        domain=[('type', '=', 'revenue')])
    default_journal_expense = fields.Many2One(
        'account.journal', "Account Journal Expense",
        domain=[('type', '=', 'expense')])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(ConfigurationDefaultJournal, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.extend(
            ['default_journal_revenue', 'default_journal_expense'])
        value_names.extend(
            ['default_journal_revenue', 'default_journal_expense'])
        fields.append('company')
        migrate_property(
            'account.configuration', field_names, cls, value_names,
            fields=fields)
