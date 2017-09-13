from nose2.tools import such
from unittest import mock

import webapp

with such.A('Web Calculator Application') as it:
    with it.having('Home Page'):
        @it.should('display the home page')
        @mock.patch('webapp.request')
        def test(request_mock):
            request_mock.method = 'GET'
            html = webapp.home()
            it.assertIn('Home Page', html)

        @it.should('display addition form')
        @mock.patch('webapp.request')
        def test(request_mock):
            request_mock.method = 'GET'
            html = webapp.home()
            it.assertIn('<form', html)
            it.assertIn('name="first"', html)
            it.assertIn('name="second"', html)

        with it.having('addition form'):
            @it.should('delegate request parameters to calc.add')
            @mock.patch('webapp.request')
            @mock.patch('webapp.calc')
            def test(calc_mock, request_mock):
                request_mock.method = 'POST'
                request_mock.form = {
                    'first': '50',
                    'second': '70',
                }

                webapp.home()

                calc_mock.add.assert_called_once_with(50, 70)

    it.createTests(globals())