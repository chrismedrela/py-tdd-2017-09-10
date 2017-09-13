import asyncio
import unittest
from unittest import mock

import coro

def AsyncMock(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*coro_args, **coro_kwargs):
        return m(*coro_args, **coro_kwargs)

    mock_coro.mock = m
    return mock_coro

class TestAsynchronousServer(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)  
        self.addCleanup(self.loop.close)
    
    def test_invalid_packet(self):
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(coro.receive('FOO', 'data'))

    def test_ping_manual(self):
        try:
            send_to_client_mock = mock.Mock()
            async def send_to_client_coroutine(packet_type, packet_data):
                return send_to_client_mock(packet_type, packet_data)

            real_send_to_client = coro.send_to_client
            coro.send_to_client = send_to_client_coroutine
            self.loop.run_until_complete(coro.receive('PING', 'data'))
            send_to_client_mock.assert_called_once_with('PONG', 'data')
        finally:
            coro.send_to_client = real_send_to_client

    @mock.patch('coro.send_to_client', new_callable=AsyncMock)
    def test_ping(self, send_to_client):
        self.loop.run_until_complete(coro.receive('PING', 'data'))
        send_to_client.mock.assert_called_once_with('PONG', 'data')
        
    @mock.patch('coro.send_to_client', new_callable=AsyncMock)
    @mock.patch('coro.trigger_event', new_callable=AsyncMock)
    def test_message(self, trigger_event, send_to_client):
        trigger_event.mock.return_value = 'my response'
        self.loop.run_until_complete(coro.receive('MESSAGE', 'data'))
        trigger_event.mock.assert_called_once_with('message', 'data')
        send_to_client.mock.assert_called_once_with('MESSAGE', 'my response')
            
unittest.main(argv=['python', 'TestAsynchronousServer'], exit=False)  