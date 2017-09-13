import unittest
from unittest import mock

import coro

class TestSynchronousServer(unittest.TestCase):
    @mock.patch('coro.next_packet')
    @mock.patch('coro.send_to_client')
    def test_ping(self, 
                  send_to_client_mock,
                  next_packet_mock):
        next_packet_mock.side_effect = [
            ('PING', 'data'),
            StopIteration,
        ]
        with self.assertRaises(StopIteration):
            coro.receive()

        send_to_client_mock.assert_called_once_with('PONG', 'data')
          

if __name__ == '__main__':
    unittest.main()