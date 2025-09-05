import unittest
from lib.pyscm.pyscm_api import PyscmApi

class TestPyscmApi(unittest.TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)

    def test_init(self):
        self.assertTrue(PyscmApi.init("test_repo"))
