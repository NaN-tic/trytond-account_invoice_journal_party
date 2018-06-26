# This file is part account_invoice_journal_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import invoice
from . import party


def register():
    Pool.register(
        configuration.Configuration,
        configuration.ConfigurationDefaultJournal,
        invoice.Invoice,
        party.Party,
        module='account_invoice_journal_party', type_='model')
    Pool.register(
        invoice.Sale,
        depends=['sale'],
        module='account_invoice_journal_party', type_='model'
    )
    Pool.register(
        invoice.Purchase,
        depends=['purchase'],
        module='account_invoice_journal_party', type_='model'
    )
