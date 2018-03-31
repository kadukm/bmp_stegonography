import sys
import unittest

sys.path.append('..')
from modules.coding_options import CodingOptions


class TestCodingOptions(unittest.TestCase):
    def test_without_args(self):
        opt = CodingOptions()
        self.assertEqual(opt.r_count, 1)
        self.assertEqual(opt.g_count, 1)
        self.assertEqual(opt.b_count, 1)

    def test_with_args123(self):
        opt = CodingOptions(1, 2, 3)
        self.assertEqual(opt.r_count, 1)
        self.assertEqual(opt.g_count, 2)
        self.assertEqual(opt.b_count, 3)

    def test_with_0(self):
        opt = CodingOptions(0)
        self.assertEqual(opt.r_count, 0)
        self.assertEqual(opt.g_count, 1)
        self.assertEqual(opt.b_count, 1)

    def test_with_000(self):
        with self.assertRaises(ValueError):
            CodingOptions(0, 0, 0)

    def test_with_9(self):
        with self.assertRaises(ValueError):
            CodingOptions(9)

    def test_get_from_str(self):
        opt = CodingOptions.get_options_from('r1g2b4')
        self.assertEqual(opt.r_count, 1)
        self.assertEqual(opt.g_count, 2)
        self.assertEqual(opt.b_count, 4)

    def test_get_from_str_with_error(self):
        with self.assertRaises(KeyError):
            CodingOptions.get_options_from('r1g2h4')


if __name__ == '__main__':
    unittest.main()
