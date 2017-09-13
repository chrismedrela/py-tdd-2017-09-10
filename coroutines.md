# Basics of Coroutines (Hello World)

```python
import asyncio

async def hello_world():
    print("Hello world")
```

```python
>>> print(hello_world())
<coroutine object hello_world at 0x7f9b5c70af68>
>>> loop = asyncio.get_event_loop()
>>> loop.run_until_complete(hello_world())  # blocking call
Hello world
>>> loop.close()
```

# Things a coroutine can do (from Python docs)

- `result = await future` or `result = yield from future` – suspends the coroutine until the future is done, then returns the future’s result, or raises an exception, which will be propagated. (If the future is cancelled, it will raise a CancelledError exception.) Note that tasks are futures, and everything said about futures also applies to tasks.
- `result = await coroutine` or `result = yield from coroutine` – wait for another coroutine to produce a result (or raise an exception, which will be propagated). The coroutine expression must be a call to another coroutine.
- `return expression` – produce a result to the coroutine that is waiting for this one using `await` or `yield from`.
- `raise exception` – raise an exception in the coroutine that is waiting for this one using `await` or `yield from`.

# Displaying Current Date 

## Sync version

```python
import datetime
import time

def display_date():
    end_time = time.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (time.time() + 1.0) >= end_time:
            break
        time.sleep(1)

display_date()
```

## Async version

```python
import asyncio
import datetime

async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await hello_world()
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(display_date(loop))
loop.close()
```

    2017-09-11 20:37:57.952793
    2017-09-11 20:37:58.954586
    2017-09-11 20:37:59.956252
    2017-09-11 20:38:00.958490
    2017-09-11 20:38:01.960176
    
# Two Async Functions

## Sync version

```python
import time

def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    time.sleep(1.0)
    return x + y

def print_sum(x, y):
    result = compute(x, y)
    print("%s + %s = %s" % (x, y, result))

print_sum(1, 2)
```

    Compute 1 + 2 ...
    1 + 2 = 3    
    
## Async version

```python
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```

    Compute 1 + 2 ...
    1 + 2 = 3    
    
# Factorial - parallel execution

## Sync version

```python
import time

def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        time.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))
    return f

factorial("A", 2)
factorial("B", 3)
factorial("C", 4)
```

## Async hint

```python
loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
```

## Async version

```python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))
    return f

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
loop.close()
```

    Task A: Compute factorial(2)...
    Task C: Compute factorial(2)...
    Task B: Compute factorial(2)...
    Task A: factorial(2) = 2
    Task C: Compute factorial(3)...
    Task B: Compute factorial(3)...
    Task C: Compute factorial(4)...
    Task B: factorial(3) = 6
    Task C: factorial(4) = 24

    [2, 6, 24]
    
# Testing Coroutines

```python
import unittest

class Test(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.addCleanup(self.loop.close)
        
    def test_async_hello_world(self):
        self.loop.run_until_complete(hello_world())
        
    def test_custom_async_function(self):
        async def go():
            print("Hello world")
        self.loop.run_until_complete(go())
        
    def test_factorial(self):
        got = self.loop.run_until_complete(factorial('name', 3))
        expected = 6
        self.assertEqual(got, expected)        
        
    def test_factorial_version_2(self):
        async def go():
            got = await factorial('name', 3)
            expected = 6
            self.assertEqual(got, expected)
        self.loop.run_until_complete(go())
        
unittest.main(argv=['python', 'Test'], exit=False)
```

# Testing Synchronous Server

Na podstawie [tego blogposta](https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code)

## Server

```python
def receive(packet_type, packet_data):
    if packet_type == 'PING':
        send_to_client("PONG", packet_data)
    elif packet_type == 'MESSAGE':
        response = trigger_event('message', packet_data)
        send_to_client('MESSAGE', response)
    else:
        raise ValueError('Invalid packet type')

def send_to_client(packet_type, packet_data):
    print('send_to_client', packet_type, packet_data)

def trigger_event(event_name, event_data):
    print('trigger_event', event_name, event_data)
```

## Tests

```python
import unittest
from unittest import mock

class TestSynchronousServer(unittest.TestCase):
    def test_invalid_packet(self):
        with self.assertRaises(ValueError):
            receive('FOO', 'data')
            
    @mock.patch('__main__.send_to_client')
    def test_ping(self, send_to_client):
        receive('PING', 'data')
        send_to_client.assert_called_once_with('PONG', 'data')
        
    @mock.patch('__main__.trigger_event', return_value='my response')
    @mock.patch('__main__.send_to_client')
    def test_message(self, send_to_client, trigger_event):
        receive('MESSAGE', 'data')
        trigger_event.assert_called_once_with('message', 'data')
        send_to_client.assert_called_once_with('MESSAGE', 'my response')        
        
unittest.main(argv=['python', 'TestSynchronousServer'], exit=False)
```

# Testing Asynchronous Server

## Server

```python
async def receive(packet_type, packet_data):
    if packet_type == 'PING':
        await send_to_client("PONG", packet_data)
    elif packet_type == 'MESSAGE':
        response = await trigger_event('message', packet_data)
        await send_to_client('MESSAGE', response)
    else:
        raise ValueError('Invalid packet type')

async def send_to_client(packet_type, packet_data):
    raise NotImplementedError

async def trigger_event(event_name, event_data):
    raise NotImplementedError
```

## `AsyncMock` helper

For the `'PING'` case, we need to mock the `send_to_client()` call, like we did in the synchronous case, but the problem is that this is an asynchronous function and as such it is awaited by the `receive()` function. Sadly, a mock object cannot be used with the `await` keyword, only awaitable things such as coroutines can.

So how can we mock this function if we can't use a mock object? It took me a while to figure out a solution to this problem. The `send_to_client()` function returns a coroutine when it is invoked, so our mocked function needs to behave in the same way. But we don't want the coroutine that is returned during unit tests to represent the real function, since we can't allow that function to run. What we want, is for the mocked coroutine to invoke a `MagicMock` object, so that we can then ensure that the function was called as expected.


```python
import asyncio

def AsyncMock(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*coro_args, **coro_kwargs):
        return m(*coro_args, **coro_kwargs)

    mock_coro.mock = m
    return mock_coro
```

Let's look at this function one part at a time. In the middle of the function body, there is an inner asynchronous function, called `mock_coro()`, that accepts any arguments it's given. Function `AsyncMock()` returns this inner async function, you can see that in the last line. I said above that we needed a mock asynchronous function that behaves like a real one, and this `mock_coro()` function does, simply because it is a real asynchronous function.

The last thing we need, is a way for the test code to get at this `m` object. To make it accessible from the outside, I added a `mock` attribute to the `mock_coro` function. In case you find this strange, in Python, functions are objects, so you can add custom attributes to them.

Przykładowe użycie `AsyncMock`:

```python
>>> import asyncio
>>> from test_async_receive import AsyncMock
>>> f = AsyncMock(return_value='hello!')
>>> f('foo', 'bar')
<coroutine object AsyncMock.<locals>.mock_coro at 0x10ef84ca8>
>>> asyncio.get_event_loop().run_until_complete(f('foo', 'bar'))
'hello!'
>>> f.mock.assert_called_once_with('foo', 'bar')
>>> f.mock.assert_called_once_with('foo')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../unittest/mock.py", line 825, in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
  File ".../unittest/mock.py", line 814, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: Expected call: mock('foo')
Actual call: mock('foo', 'bar')
```

## Tests

```python
class TestAsynchronousServer(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)  
        self.addCleanup(self.loop.close)
    
    def test_invalid_packet(self):
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(receive('FOO', 'data'))

    @mock.patch('__main__.send_to_client', new_callable=AsyncMock)
    def test_ping(self, send_to_client):
        self.loop.run_until_complete(receive('PING', 'data'))
        send_to_client.mock.assert_called_once_with('PONG', 'data')
        
    @mock.patch('__main__.send_to_client', new_callable=AsyncMock)
    @mock.patch('__main__.trigger_event', new_callable=AsyncMock)
    def test_message(self, trigger_event, send_to_client):
        trigger_event.mock.return_value = 'my response'
        self.loop.run_until_complete(receive('MESSAGE', 'data'))
        trigger_event.mock.assert_called_once_with('message', 'data')
        send_to_client.mock.assert_called_once_with('MESSAGE', 'my response')
            
unittest.main(argv=['python', 'TestAsynchronousServer'], exit=False)  
```
