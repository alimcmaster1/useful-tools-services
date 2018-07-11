import unittest


class ciTest(unittest.TestCase):
    """
    For the sake of getting tests
    to run on CI server
    """

    def test_basic(self):
        self.assertEquals(True, True)
