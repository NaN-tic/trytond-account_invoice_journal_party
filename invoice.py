# This file is part of account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Invoice']


class Invoice:
    __name__ = 'account.invoice'
    __metaclass__ = PoolMeta

   @fields.depends('type', 'party')
    def on_change_party(self):
        Configuration = Pool().get('account.configuration')

        configuration = Configuration(1)

        super(Invoice, self).on_change_party()

        if self.type == 'out' and configuration.default_journal_revenue:
            self.journal = configuration.default_journal_revenue
        if self.type == 'in' and configuration.default_journal_expense:
            self.journal = configuration.default_journal_expense

        if self.party:
            if self.type == 'out' and self.party.journal_revenue:
                self.journal = self.party.journal_revenue
            if self.type == 'in' and self.party.journal_expense:
                self.journal = self.party.journal_expense

        if not hasattr(self, 'journal'):
            self.on_change_type() # reset default journal
