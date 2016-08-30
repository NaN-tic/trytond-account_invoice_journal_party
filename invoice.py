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

        res = super(Invoice, self).on_change_party()

        journal = None
        if self.type in ('out_invoice', 'out_credit_note') \
                and configuration.default_journal_revenue:
            journal = configuration.default_journal_revenue
        if self.type in ('in_invoice', 'in_credit_note') \
                and configuration.default_journal_expense:
            journal = configuration.default_journal_expense

        if self.party:
            if self.type in ('out_invoice', 'out_credit_note') \
                    and self.party.journal_revenue:
                journal = self.party.journal_revenue
            if self.type in ('in_invoice', 'in_credit_note') \
                    and self.party.journal_expense:
                journal = self.party.journal_expense

        if journal:
            res['journal'] = journal.id
            res['journal.rec_name'] = journal.rec_name
        else:
            res.update(self.on_change_type()) # reset default journal
        return res
