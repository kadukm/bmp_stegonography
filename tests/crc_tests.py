import sys
import unittest

sys.path.append('..')
from modules import steg_functions as steg


class TestGetCRC(unittest.TestCase):
    def test_simple_examples(self):
        self._check_case('1010011', '10101', '1110')
        self._check_case('1010101', '1100', '000')
        self._check_case('10100110', '1111', '110')

    def test_double_end_cases(self):
        self._check_case('11110', '1111', '000')
        self._check_case('100000', '10000', '0000')

    def test_double_beginning_cases(self):
        self._check_case('011001', '101', '10')
        self._check_case('0010010101', '11011', '0011')
        self._check_case('00000', '111111', '00000')

    def test_big_cases(self):
        self._check_case('10100101001010001010010010101010010'
                         '10010010010001000101101011010101010100100',
                         '111010101',
                         '10011011')
        self._check_case(data='0000000100100011010001010110011110'
                              '0010011010101111001101111011110'
                              '0000001001000110100010101100111100'
                              '0100110101011110011011110111100'
                              '0000010010001101000101011001111000'
                              '1001101010111100110111101111000'
                              '0000100100011010001010110011110001'
                              '001101010111100110111101111',
                         polynomial='101000010111100001110000111101011'
                                    '10101001111010100011011010010011',
                         expected_res='11001011110001111011001110000010'
                                      '00110101101101101000011010110101')

    def test_ValueError(self):
        with self.assertRaises(ValueError):
            steg.get_crc_from_clear_data('101', '1' * 66)

    def _check_case(self, data, polynomial, expected_res):
        res = steg.get_crc_from_clear_data(data, polynomial)
        self.assertEqual(expected_res, res)


class TestCRCIsRight(unittest.TestCase):
    def test_simple_examples(self):
        self._check_case('1010011', '10101', '1110')
        self._check_case('1010101', '1100', '000')
        self._check_case('10100110', '1111', '110')

    def test_double_end_cases(self):
        self._check_case('11110', '1111', '000')
        self._check_case('100000', '10000', '0000')

    def test_double_beginning_cases(self):
        self._check_case('011001', '101', '10')
        self._check_case('0010010101', '11011', '0011')
        self._check_case('00000', '111111', '00000')

    def test_big_cases(self):
        self._check_case('101001010010100010100100101010100101'
                         '0010010010001000101101011010101010100100',
                         '111010101',
                         '10011011')
        self._check_case(data='00000001001000110100010101100111'
                              '100010011010101111001101111011110'
                              '00000010010001101000101011001111'
                              '000100110101011110011011110111100'
                              '00000100100011010001010110011110'
                              '001001101010111100110111101111000'
                              '00001001000110100010101100111100'
                              '01001101010111100110111101111',
                         polynomial='1010000101111000011100001111010111'
                                    '0101001111010100011011010010011',
                         crc='1100101111000111101100111000001000110'
                             '101101101101000011010110101')

    def _check_case(self, data, polynomial, crc):
        upd_data = data + crc
        self.assertTrue(steg.crc_is_right(upd_data, polynomial))


class TestNormalizePolynomial(unittest.TestCase):
    def test_standard_polynomials(self):
        self.assertEqual('0000000000000000000000000000000'
                         '0000000000000000011000000000000101',
                         steg.normalize_polynomial('11000000000000101'))
        self.assertEqual('0000000000000000000000000001111111'
                         '1111111111111111111111111111111',
                         steg.normalize_polynomial('11111111111111111111'
                                                   '111111111111111111'))
        self.assertEqual('00000000000000000000000000011000'
                         '000000000000000000000000000000000',
                         steg.normalize_polynomial('1100000000000000000'
                                                   '0000000000000000000'))

    def test_0x0_polynomial(self):
        self.assertEqual('000000000000000000000000000000'
                         '00000000000000000000000000000000010',
                         steg.normalize_polynomial('10'))

    def test_0xFFFFFFFF_polynomial(self):
        expected_res = '1' * 65
        res = steg.normalize_polynomial('1' * 65)
        self.assertEqual(expected_res, res)


class TestDenormalizePolynomial(unittest.TestCase):
    def test_standard_polynomials(self):
        self._check_case('11000000000000101',
                         '0000000000000000000000000000000'
                         '0000000000000000011000000000000101')
        self._check_case('11111111111111111111111111111111111111',
                         '0000000000000000000000000001111'
                         '1111111111111111111111111111111111')
        self._check_case('11000000000000000000000000000000000000',
                         '00000000000000000000000000011000'
                         '000000000000000000000000000000000')

    def test_0x0_polynomial(self):
        self._check_case('10', '0000000000000000000000000000000'
                               '0000000000000000000000000000000010')

    def test_0xFFFFFFFF_polynomial(self):
        self._check_case('1' * 65, '1' * 65)

    def _check_case(self, expected_res, norm_polynomial):
        res = steg.denormalize_polynomial(norm_polynomial)
        self.assertEqual(expected_res, res)


if __name__ == '__main__':
    unittest.main()
