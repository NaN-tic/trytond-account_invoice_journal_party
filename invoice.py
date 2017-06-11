# This file is part of account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['Invoice', 'Sale', 'Purchase']


class Invoice:
    __name__ = 'account.invoice'
    __metaclass__ = PoolMeta

    def on_change_type(self):
        Configuration = Pool().get('account.configuration')

        super(Invoice, self).on_change_type()

        configuration = Configuration(1)
        if self.type == 'out' and configuration.default_journal_revenue:
            self.journal = configuration.default_journal_revenue
        elif self.type == 'in' and configuration.default_journal_expense:
            self.journal = configuration.default_journal_expense

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


class Sale:
    __name__ = 'sale.sale'
    __metaclass__ = PoolMeta

    def _get_invoice_sale(self):
        Configuration = Pool().get('account.configuration')
        configuration = Configuration(1)

        invoice = super(Sale, self)._get_invoice_sale()
        if invoice.party.journal_revenue:
            invoice.journal = invoice.party.journal_revenue
        elif configuration.default_journal_revenue:
            invoice.journal = configuration.default_journal_revenue
        return invoice


class Purchase:
    __name__ = 'purchase.purchase'
    __metaclass__ = PoolMeta

    def _get_invoice_purchase(self):
        Configuration = Pool().get('account.configuration')
        configuration = Configuration(1)

        invoice = super(Purchase, self)._get_invoice_purchase()
        if invoice.party.journal_expense:
            invoice.journal = invoice.party.journal_expense
        elif configuration.default_journal_expense:
            invoice.journal = configuration.default_journal_expense
        return invoice
