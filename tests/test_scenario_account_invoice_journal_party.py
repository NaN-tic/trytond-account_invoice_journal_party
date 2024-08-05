import unittest

from proteus import Model
from trytond.modules.account.tests.tools import create_chart, create_fiscalyear
from trytond.modules.account_invoice.tests.tools import \
    set_fiscalyear_invoice_sequences
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install account_invoice_journal_party
        activate_modules('account_invoice_journal_party')

        # Create company
        _ = create_company()
        company = get_company()

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)

        # Default configuration journals
        Journal = Model.get('account.journal')
        journal_revenue, = Journal.find([('type', '=', 'revenue')])
        journal_expense, = Journal.find([('type', '=', 'expense')])
        Configuration = Model.get('account.configuration')
        configuration = Configuration(1)
        configuration.default_journal_revenue = journal_revenue
        configuration.default_journal_expense = journal_expense
        configuration.save()

        # Create new journals
        Sequence = Model.get('ir.sequence')
        sequence_journal, = Sequence.find([('sequence_type.name', '=',
                                            'Account Journal')])
        journal_revenue = Journal()
        journal_revenue.name = 'Party Revenue'
        journal_revenue.type = 'revenue'
        journal_revenue.sequence = sequence_journal
        journal_revenue.save()
        journal_expense = Journal()
        journal_expense.name = 'Party Expense'
        journal_expense.type = 'expense'
        journal_expense.sequence = sequence_journal
        journal_expense.save()

        # Create parties with journal
        Party = Model.get('party.party')
        party1 = Party(name='Party')
        party1.save()
        party2 = Party(name='Party Journal')
        party2.journal_revenue = journal_revenue
        party2.journal_expense = journal_expense
        party2.save()

        # Create Out invoice
        Invoice = Model.get('account.invoice')
        invoice = Invoice()
        invoice.type = 'out'
        invoice.party = party1
        self.assertEqual(invoice.journal.rec_name, 'Revenue')
        invoice.party = party2
        self.assertEqual(invoice.journal.rec_name, 'Party Revenue')

        # Create In invoice
        invoice = Invoice()
        invoice.type = 'in'
        invoice.party = party1
        self.assertEqual(invoice.journal.rec_name, 'Expense')
        invoice.party = party2
        self.assertEqual(invoice.journal.rec_name, 'Party Expense')
