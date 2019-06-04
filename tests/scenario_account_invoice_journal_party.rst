======================================
Account Invoice Journal Party Scenario
======================================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax, set_tax_code
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences
    >>> today = datetime.date.today()

Create a database::

    >>> config = config.set_trytond()
    >>> config.pool.test = True

Install account_invoice_journal_party::

    >>> Module = Model.get('ir.module')
    >>> module, = Module.find([
    ...         ('name', '=', 'account_invoice_journal_party'),
    ...         ])
    >>> module.click('install')
    >>> Wizard('ir.module.install_upgrade').execute('upgrade')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> receivable = accounts['receivable']
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> account_tax = accounts['tax']
    >>> account_cash = accounts['cash']

Default configuration journals::

    >>> Journal = Model.get('account.journal')
    >>> journal_revenue, =  Journal.find([('type', '=', 'revenue')])
    >>> journal_expense, =  Journal.find([('type', '=', 'expense')])
    >>> Configuration = Model.get('account.configuration')
    >>> configuration = Configuration(1)
    >>> configuration.default_journal_revenue = journal_revenue
    >>> configuration.default_journal_expense = journal_expense
    >>> configuration.save()

Create new journals::

    >>> Sequence = Model.get('ir.sequence')
    >>> sequence_journal, = Sequence.find([('code', '=', 'account.journal')])
    >>> journal_revenue = Journal()
    >>> journal_revenue.name = 'Party Revenue'
    >>> journal_revenue.type = 'revenue'
    >>> journal_revenue.sequence = sequence_journal
    >>> journal_revenue.save()
    >>> journal_expense = Journal()
    >>> journal_expense.name = 'Party Expense'
    >>> journal_expense.type = 'expense'
    >>> journal_expense.sequence = sequence_journal
    >>> journal_expense.save()

Create parties with journal::

    >>> Party = Model.get('party.party')
    >>> party1 = Party(name='Party')
    >>> party1.save()
    >>> party2 = Party(name='Party Journal')
    >>> party2.journal_revenue = journal_revenue
    >>> party2.journal_expense = journal_expense
    >>> party2.save()

Create Out invoice::

    >>> Invoice = Model.get('account.invoice')
    >>> invoice = Invoice()
    >>> invoice.type = 'out_invoice'
    >>> invoice.party = party1
    >>> invoice.journal.rec_name
    u'Revenue'
    >>> invoice.party = party2
    >>> invoice.journal.rec_name
    u'Party Revenue'

Create In invoice::

    >>> invoice = Invoice()
    >>> invoice.type = 'in_invoice'
    >>> invoice.party = party1
    >>> invoice.journal.rec_name
    u'Expense'
    >>> invoice.party = party2
    >>> invoice.journal.rec_name
    u'Party Expense'
