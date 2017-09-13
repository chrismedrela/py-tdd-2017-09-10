from nose2.tools import such
from calc import add

with such.A('calculator module') as it:
    with it.having('addition feature'):
        @it.should('return sum of two numbers')
        def test():
            a = 50
            b = 70
            expected = 120
            got = add(a, b)
            it.assertEqual(got, expected)
    
    it.createTests(globals())