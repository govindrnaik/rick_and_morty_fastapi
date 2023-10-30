import unittest
import ifaddr

class TestIfaddr(unittest.TestCase):
    def test_get_adapters_contains_localhost(self):
        adapters = ifaddr.get_adapters()
        found = False
        for adapter in adapters:
            for ip in adapter.ips:
                if ip.ip == "127.0.0.1":
                    found = True
        self.assertTrue(found, "No adapter has IP 127.0.0.1: %s" % str(adapters))