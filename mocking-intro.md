# Mocking

## Importowanie

```python
>>> from unittest import mock
>>> try:
...     from unittest import mock
... except ImportError:
...     import mock
...     
```

## Mock imitujący funkcje

```python
>>> m = mock.Mock()
>>> m()
<Mock name='mock()' id='140567917706992'>
>>> m.assert_called_once_with()
>>> m.assert_called_once_with(23)
Traceback (most recent call last):
  File "<ipython-input-10-6807c2c0052f>", line 1, in <module>
    m.assert_called_once_with(23)
  File "/usr/lib/python3.5/unittest/mock.py", line 805, in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
  File "/usr/lib/python3.5/unittest/mock.py", line 794, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: mock(23)
Actual call: mock()

>>> m(42, foo=3)
<Mock name='mock()' id='140567917706992'>
>>> m.assert_called_with(42, foo=3)
>>> m.assert_called_once_with(42, foo=3)
Traceback (most recent call last):
  File "<ipython-input-13-1a74e3446ad6>", line 1, in <module>
    m.assert_called_once_with(42, foo=3)
  File "/usr/lib/python3.5/unittest/mock.py", line 804, in assert_called_once_with
    raise AssertionError(msg)
AssertionError: Expected 'mock' to be called once. Called 2 times.

>>> m.call_args
call(42, foo=3)
>>> m.call_args == mock.call(42, foo=3)
True
```

## `return_value`

```python
>>> m.return_value = 'asdf'
>>> m()
'asdf'
>>> m.return_value.foo = 42
Traceback (most recent call last):
  File "<ipython-input-18-647f53884ca0>", line 1, in <module>
    m.return_value.foo = 42
AttributeError: 'str' object has no attribute 'foo'

>>> m.return_value = mock.Mock()
>>> m.return_value.foo = 42
>>> inside_m = m()
>>> inside_m.foo
42
>>> m.return_value.bar.return_value = 84
>>> inside_m = m()
>>> inside_m.foo
42
>>> inside_m.bar()
84
>>> inside_m.bar('asdf', 'qwer')
84
>>> m.return_value.bar.assert_called_with('asdf', 'qwer')
>>> m.return_value.bar2 = mock.Mock(return_value=84)
>>> inside_m = m()
>>> inside_m.bar2()
84
>>> m().bar2()
84
```

## `side_effect`

```python
>>> m.side_effect = KeyError
>>> m()
Traceback (most recent call last):
  File "<ipython-input-34-7e5925b669a0>", line 1, in <module>
    m()
  File "/usr/lib/python3.5/unittest/mock.py", line 919, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.5/unittest/mock.py", line 975, in _mock_call
    raise effect
KeyError

>>> m.side_effect = [1, 2, 3]
>>> m()
1
>>> m()
2
>>> m()
3
>>> m()
Traceback (most recent call last):
  File "<ipython-input-39-7e5925b669a0>", line 1, in <module>
    m()
  File "/usr/lib/python3.5/unittest/mock.py", line 919, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.5/unittest/mock.py", line 978, in _mock_call
    result = next(effect)
StopIteration

>>> m.side_effect = lambda x: x+1
>>> m(5)
6
>>> m(1)
2
>>> m.return_value = lambda x: x+1
>>> m()
Traceback (most recent call last):
  File "<ipython-input-44-7e5925b669a0>", line 1, in <module>
    m()
  File "/usr/lib/python3.5/unittest/mock.py", line 919, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.5/unittest/mock.py", line 985, in _mock_call
    ret_val = effect(*args, **kwargs)
TypeError: <lambda>() missing 1 required positional argument: 'x'

>>> m(5)
6
```

## Assercje

```python
>>> m = mock.Mock()
>>> m(10)
<Mock name='mock()' id='140567916229912'>
>>> m.assert_called_with(10)
>>> m.assert_called_once_with(10)
>>> m.assert_any_call(10)
>>> m(20)
<Mock name='mock()' id='140567916229912'>
>>> m.assert_any_call(10)
>>> m.assert_called_with(10)
Traceback (most recent call last):
  File "<ipython-input-54-192ac0b9363e>", line 1, in <module>
    m.assert_called_with(10)
  File "/usr/lib/python3.5/unittest/mock.py", line 794, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: mock(10)
Actual call: mock(20)

>>> m.assert_not_called()
Traceback (most recent call last):
  File "<ipython-input-55-a0ad89fca13e>", line 1, in <module>
    m.assert_not_called()
  File "/usr/lib/python3.5/unittest/mock.py", line 775, in assert_not_called
    raise AssertionError(msg)
AssertionError: Expected 'mock' to not have been called. Called 2 times.

>>> m.called
True
>>> m.call_count
2
>>> m.call_args
call(20)
>>> m.call_args_list
[call(10), call(20)]
```

## Zagnieżdżenia

```python
>>> m.foo
<Mock name='mock.foo' id='140567916294776'>
>>> m
<Mock id='140567916229800'>
>>> m.foo.bar.egg.spam
<Mock name='mock.foo.bar.egg.spam' id='140567916294216'>
>>> os = mock.Mock()
>>> os.remove
<Mock name='mock.remove' id='140567916295112'>
>>> m.foo.bar.egg.spam()
<Mock name='mock.foo.bar.egg.spam()' id='140567916273280'>
>>> m.mock_calls
[call(10), call(20), call.foo.bar.egg.spam()]
```

## MagicMock

```python
>>> m = mock.Mock()
>>> mm = mock.MagicMock()
>>> len(m)
Traceback (most recent call last):
  File "<ipython-input-71-31c0f2e6f20c>", line 1, in <module>
    len(m)
TypeError: object of type 'Mock' has no len()

>>> len(mm)
0
>>> 42 in m
Traceback (most recent call last):
  File "<ipython-input-73-3edee1faa062>", line 1, in <module>
    42 in m
TypeError: argument of type 'Mock' is not iterable

>>> 42 in mm
False
>>> mm.__len__.return_value = 84
>>> len(mm)
84
>>> mm = MagicMock(__len__=lambda: 84)
Traceback (most recent call last):
  File "<ipython-input-77-53f85f6dc837>", line 1, in <module>
    mm = MagicMock(__len__=lambda: 84)
NameError: name 'MagicMock' is not defined

>>> mm = mock.MagicMock(__len__=lambda: 84)
>>> len(mm)
Traceback (most recent call last):
  File "<ipython-input-79-2cb7f0cb9a1d>", line 1, in <module>
    len(mm)
  File "/usr/lib/python3.5/unittest/mock.py", line 1706, in method
    return func(self, *args, **kw)
TypeError: <lambda>() takes 0 positional arguments but 1 was given

>>> mm = mock.MagicMock(__len__=lambda self: 84)
>>> len(mm)
84
```

## Auto-spec

```python
>>> dumb_os_mock = mock.Mock()
>>> dumb_os_mock.remove('file')
<Mock name='mock.remove()' id='140567917868872'>
>>> dumb_os_mock.remoev('file')
<Mock name='mock.remoev()' id='140567916343760'>
>>> dumb_os_mock.remove.asser_called_with('another file')
<Mock name='mock.remove.asser_called_with()' id='140567916317608'>
>>> dumb_os_mock.remove.assetr_called_with('another file')
<Mock name='mock.remove.assetr_called_with()' id='140567915832544'>
>>> 
>>> import os
>>> os_mock = mock.Mock(spec=os)
>>> os.mock.remove('file')
Traceback (most recent call last):
  File "<ipython-input-90-a60bce089747>", line 1, in <module>
    os.mock.remove('file')
AttributeError: module 'os' has no attribute 'mock'

>>> os_mock.remove('file')
<Mock name='mock.remove()' id='140567915871704'>
>>> os_mock.remoev('file')
Traceback (most recent call last):
  File "<ipython-input-92-c6136eff5b98>", line 1, in <module>
    os_mock.remoev('file')
  File "/usr/lib/python3.5/unittest/mock.py", line 580, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'remoev'

>>> os_mock.remove
<Mock name='mock.remove' id='140567915868904'>
>>> os_mock.remove.asser_called_with('another file')
<Mock name='mock.remove.asser_called_with()' id='140567915871032'>
>>> class Something:
...     def __init__(self):
...         self.foo = 42
...         
>>> something_mock = mock.Mock(spec=Something)
>>> something_mock.foo
Traceback (most recent call last):
  File "<ipython-input-97-9b7307fdf935>", line 1, in <module>
    something_mock.foo
  File "/usr/lib/python3.5/unittest/mock.py", line 580, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'foo'
```

## Mocking context managers

```python
>>> # @patch as context manager
>>> with mock.patch('__main__.open') as open_mock:
...     with open('foo', 'r') as s:
...         s.read()
...         
>>> open_mock
<MagicMock name='open' id='140567915949584'>
>>> open_mock.call_args_list
[call('foo', 'r')]
>>> open_mock.mock_calls
[call('foo', 'r'),
 call().__enter__(),
 call().__enter__().read(),
 call().__exit__(None, None, None)]
```

## `mock.ANY` utility

```python
>>> # mock.ANY utility
>>> open_mock.assert_called_once_with(mock.ANY, 'r')
>>> mock.ANY == 2
True
>>> mock.ANY == 'asdf'
True
>>> mock.ANY == []
True
>>> mock.ANY == False
True
>>> mock.ANY == mock.ANY
True
>>> open_mock()
<MagicMock name='open()' id='140567915982520'>
>>> open_mock.assert_called_with(mock.ANY)
Traceback (most recent call last):
  File "<ipython-input-112-d9e1f41cd8a2>", line 1, in <module>
    open_mock.assert_called_with(mock.ANY)
  File "/usr/lib/python3.5/unittest/mock.py", line 794, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: open(<ANY>)
Actual call: open()
```