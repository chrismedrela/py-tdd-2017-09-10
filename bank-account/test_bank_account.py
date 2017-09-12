from nose2.tools import such
from bank_account import BankAccount


with such.A('BankAccount') as it:
    @it.has_test_setup
    def setup():
        it.account = BankAccount(id=1234)

    with it.having('initial state'):
        @it.should('have zero balance')
        def test():
            it.assertEqual(it.account.balance, 0)

        @it.should('be in Normal state')
        def test():
            it.assertEqual(it.account.state, 'normal')

        @it.should('have an id')
        def test():
            it.assertEqual(it.account.id, 1234)

    with it.having('normal state (balance >= 0)'):
        @it.has_test_setup
        def setup():
            it.account.deposit(1000)

        with it.having('a deposit'):
            @it.should('add amount to balance')
            def test():
                it.assertEqual(it.account.balance, 1000)

        with it.having('withdraw amount smaller than balance'):
            @it.should('subtract amount from balance')
            def test():
                it.account.withdraw(700)
                it.assertEqual(it.account.balance, 300)

        with it.having('withdraw amount greater than balance'):
            @it.should('change state to overdraft')
            def test():
                it.account.withdraw(1200)
                it.assertEqual(it.account.state, 'overdraft')

        with it.having('paying interest'):
            @it.should('add 10% interest to balance')
            def test():
                it.account.pay_interest()
                it.assertEqual(it.account.balance, 1100)


    it.createTests(globals())