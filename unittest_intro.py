### Simple example -- testing function adding two numbers

import unittest

def factorial(num):
    if not isinstance(num, int):
        raise TypeError('Argument must be int')

    if num == 0:
        return 1
    else:
        return factorial(num-1) * num


class FactorialTests(unittest.TestCase):
    def test_factorial_of_one(self):
        got = factorial(1)
        expected = 1
        self.assertEqual(got, expected)

    def test_factorial_of_two(self):
        got = factorial(2)
        expected = 2
        self.assertEqual(got, expected)

    def test_factorial_of_three(self):
        got = factorial(3)
        expected = 6
        self.assertEqual(got, expected)

    def test_failing(self):
        raise ValueError()

    def test_raises_typeerror_for_invalid_argument(self):
        with self.assertRaises(TypeError):
            factorial(2.5)

    def test_error_message_when_passing_invalid_argument(self):
        with self.assertRaises(TypeError) as cm:
            factorial(2.5)

        self.assertEqual(cm.exception.args[0], 
                         'Argument must be int')

# if __name__ == "__main__":
#     unittest.main()


### Command line interface:
#
#     -v for higher verbosity
#     -q for quiet
#     -f for fail-fast (Python 3.2+)
#     --locals for displaying values of local variables in tracebacks (Python 3.5+)
#
# specify test to run: 
#
#     python3 unittest_intro.py FactorialTests.test_factorial_of_one
#
# Alternative way to run tests:
#
#     python3 -m unittest
#     python3 -m unittest discover -p "*.py

### setUp & teardown

class SetUpAndTearDown(unittest.TestCase):
    def setUp(self):
        print('Setup')

    def tearDown(self):
        print('TearDown')

    def test_pass(self):
        print('Passing test')

    def test_error(self):
        print('Test resulting in an error')
        raise ValueError()

    def test_fail(self):
        print('Failing test')
        self.fail()


class InvalidSetUp(unittest.TestCase):
    def setUp(self):
        self.stream = open('unittest_intro.py', 'r')
        print('SetUp')
        raise Exception()

    def tearDown(self):
        self.stream.close()
        print('TearDown')

    def test_one(self):
        print('Test')


class BetterSetUp(unittest.TestCase):
    def setUp(self):
        self.stream = open('unittest_intro.py', 'r')
        self.addCleanup(lambda: print('Stream closed'))
        self.addCleanup(self.stream.close)
        self.addCleanup(lambda: print('Closing stream'))
        print('SetUp')
        raise Exception()

    def test_one(self):
        print('Test')

# if __name__ == "__main__":
#     unittest.main()

### SetUpClass and TearDownClass

class SetUpClassAndTearDownClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stream = open('unittest_intro.py', 'r')

    @classmethod 
    def tearDownClass(cls):
        cls.stream.close()

# if __name__ == "__main__":
#     unittest.main()

### setUpModule and tearDownModule

def setUpModule():
    print('Setup module')

def tearDownModule():
    print('Tear down module')

### More assertions

class Assertions(unittest.TestCase):
    def test(self):
        self.assertTrue(['not-empty'])
        self.assertFalse([])
        self.assertNotEqual(2, 3)
        
        first_dict = {}
        second_dict = {}
        self.assertIsNot(first_dict, second_dict)
        self.assertEqual(first_dict, second_dict)

        self.assertIsNone(None)
        self.assertIsNotNone({})
        
        self.assertIn('bar', ['foo', 'bar', 'spam'])
        self.assertIsInstance([], list)
        self.assertIsInstance(2, (int, float))
        self.assertIsInstance(2.5, (int, float))

    def test_fail_immediatelly(self):
        self.fail('reason')

### Skipping tests

import sys

class Skipping(unittest.TestCase):
    @unittest.skip('demonstrating skipping')
    def test_noting(self):
        self.fail('should not be executed')

    @unittest.skipUnless(sys.platform.startswith('win'),
                         'requires Windows')
    def test_windows_support(self):
        pass

    @unittest.skipIf(sys.version.startswith('3'),
                     'requires Python 2')
    def test_python_2_support(self):
        pass

    @unittest.expectedFailure
    def test_expected_failure(self):
        self.fail('should be executed')

    @unittest.expectedFailure
    def test_unexpected_success(self):
        self.fail('should be executed')

# if __name__ == "__main__":
#     unittest.main()    

### Subtests (parametrized tests)

class SubTests(unittest.TestCase):
    def test_subtest(self):
        for a, b, expected in [
            (0, 0, 0),
            (2, 2, 4),
            (2, 5, 5),
            (2, 7, 7),
        ]:
            with self.subTest(a=a, b=b, expected=expected):
                print('Subtest')
                got = a + b
                self.assertEqual(got, expected)

    def setUp(self):
        print('SetUp')

    def tearDown(self):
        print('TearDown')


# if __name__ == "__main__":
#     unittest.main()

###

if __name__ == "__main__":
    unittest.main()
