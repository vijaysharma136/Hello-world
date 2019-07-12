"""Basic unittests for rpc"""

import operator
import rpc
import unittest

import coro
from coro.test import coro_unittest

ADDR = ('127.0.0.1', 8887)


class test_root:

    def __init__ (self):
        self.calls = 0

    def add (self, *args):
        self.calls += 1
        return reduce (operator.add, args)

    def mul (self, *args):
        self.calls += 1
        return reduce (operator.mul, args)

    def __str__ (self):
        return '<test_root>'


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server = rpc.RPC_Server (test_root(), ADDR)
        coro.spawn (server.serve)
        # Give the server a chance to start.
        coro.yield_slice()

    def test_add(self):
        client = rpc.RPC_Client(ADDR)
        remote_root = client.get_proxy()
        self.assertEqual(remote_root.add (3, 4, 5, 6), 18)

    def test_mul(self):
        client = rpc.RPC_Client(ADDR)
        remote_root = client.get_proxy()
        self.assertEqual(remote_root.mul (3, 4, 5, 6), 360)

if __name__ == '__main__':
    coro_unittest.run_tests()
