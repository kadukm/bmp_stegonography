import sys
import unittest

sys.path.append('..')
from modules import steg_functions as steg


class TestGetEncodedThread(unittest.TestCase):
    def test_simple_cases(self):
        self._check_case(150, '0', 150)
        self._check_case(150, '1', 151)

    def test_zero_thread(self):
        for n in range(256):
            bin_n = bin(n)[2:]
            self._check_case(0, bin_n, n)

    def test_255_thread(self):
        for n in range(256):
            bin_n = bin(n)[2:]
            exp_res = int('1' * (8 - len(bin_n)) + bin_n, 2)
            self._check_case(255, bin_n, exp_res)

    def test_ValueError(self):
        with self.assertRaises(ValueError):
            steg.get_encoded_thread(255, '1' * 9)

    def test_empty_data(self):
        for n in range(256):
            self._check_case(n, '', n)

    def _check_case(self, cur_thread, data, exp_res):
        res = steg.get_encoded_thread(cur_thread, data)
        self.assertEqual(exp_res, res)


class TestGetDataFromThread(unittest.TestCase):
    def test_simple_cases(self):
        self._check_case(150, 1, '0')
        self._check_case(151, 1, '1')

    def test_zero_bits_count(self):
        for n in range(256):
            self._check_case(n, 0, '')

    def _check_case(self, cur_thread, bits_count, exp_res):
        res = steg.get_data_from_thread(cur_thread, bits_count)
        self.assertEqual(exp_res, res)


class TestGetUpddData(unittest.TestCase):
    def test_simple_case(self):
        self._check_case('1010101010000011111',
                         '00000000000000000000000001100100',
                         '0111100000000011')

    def _check_case(self, data, data_len, crc):
        normalized_polynomial = '0000000000000000000000000000000' \
                                '0000000000000000011000000000000101'
        res = steg.get_updated_data(data)
        self.assertEqual(data_len + normalized_polynomial + data + crc, res)


class TestGetAndCheckDecodedData(unittest.TestCase):
    def test_simple_case(self):
        data = '00000000000000000000000000000000000000000000000011000000' \
               '00000010110101010100000111110111100000000011'
        self._check_case(data, (True, '1010101010000011111'))

    def _check_case(self, data, exp_res):
        res = steg.get_and_check_decoded_data(data)
        self.assertEqual(exp_res, res)


if __name__ == '__main__':
    unittest.main()
