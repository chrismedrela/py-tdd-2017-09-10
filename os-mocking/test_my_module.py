import os.path
import unittest

from unittest import mock
# import mock  # pip install mock

from my_module import my_remove


class NoMockingTestCase(unittest.TestCase):
    def test_provided_extension_should_be_used(self):
        filename = 'file.md'
        open(filename, 'w').close()
        self.assertTrue(os.path.isfile(filename))
        my_remove(filename)
        self.assertFalse(os.path.isfile(filename))

    def test_when_extension_is_missing_then_use_default_one(self):
        filename = 'file.txt'
        open(filename, 'w').close()
        self.assertTrue(os.path.isfile(filename))
        my_remove('file')
        self.assertFalse(os.path.isfile(filename))


class PatchingTestCase(unittest.TestCase):
    @mock.patch('my_module.os')
    def test_provided_extension_should_be_used(self, os_mock):
        my_remove('file.md')
        os_mock.remove.assert_called_once_with('file.md')

    @mock.patch('my_module.os')
    def test_when_extension_is_missing_then_use_default_one(self, os_mock):
        my_remove('file')
        os_mock.remove.assert_called_once_with('file.txt')


@mock.patch('my_module.os')
class ClassPatchingTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_provided_extension_should_be_used(self, os_mock):
        my_remove('file.md')
        os_mock.remove.assert_called_once_with('file.md')

    def test_when_extension_is_missing_then_use_default_one(self, os_mock):
        my_remove('file')
        os_mock.remove.assert_called_once_with('file.txt')


class PatchingTestCase(unittest.TestCase):
    @mock.patch('my_module.os')
    @mock.patch('my_module.sys')
    def test_provided_extension_should_be_used(self, sys_mock, os_mock):
        my_remove('file.md')
        os_mock.remove.assert_called_once_with('file.md')



class PatchingInSetupTestCase(unittest.TestCase):
    def setUp(self):
        os_patcher = mock.patch('my_module.os')
        self.os_mock = os_patcher.start()
        self.addCleanup(os_patcher.stop)

    def test_provided_extension_should_be_used(self):
        my_remove('file.md')
        self.os_mock.remove.assert_called_once_with('file.md')

    def test_when_extension_is_missing_then_use_default_one(self):
        my_remove('file')
        self.os_mock.remove.assert_called_once_with('file.txt')


class PatchAsContextManager(unittest.TestCase):
    def test_provided_extension_should_be_used(self):
        with mock.patch('my_module.os') as os_mock:
            my_remove('file.md')
            os_mock.remove.assert_called_once_with('file.md')


import my_module
class ManualPatching(unittest.TestCase):
    def setUp(self):
        self.os_mock = mock.Mock()
        self.real_os = my_module.os
        my_module.os = self.os_mock

    def tearDown(self):
        my_module.os = self.real_os

    def test_provided_extension_should_be_used(self):
        my_remove('file.md')
        self.os_mock.remove.assert_called_once_with('file.md')

# class PatchingTestCase(unittest.TestCase):
#     @mock.patch('my_module.remove')
#     def test_provided_extension_should_be_used(self, remove_mock):
#         my_remove('file.md')
#         remove_mock.assert_called_once_with('file.md')

#     @mock.patch('my_module.remove')
#     def test_when_extension_is_missing_then_use_default_one(self, remove_mock):
#         my_remove('file')
#         remove_mock.assert_called_once_with('file.txt')

if __name__ == '__main__':
    unittest.main()