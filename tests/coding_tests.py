import sys
import unittest
import math
from PIL import Image

sys.path.append('..')
from modules import steg_functions as steg
from modules.coding_options import CodingOptions


class TestGetDataFromFile(unittest.TestCase):
    def test_simple_cases(self):
        self._check_case('resources/test_data_10101010', '10101010')
        self._check_case('resources/test_data_00000001', '00000001')
        self._check_case('resources/test_data_10000000', '10000000')

    def test_only_ones(self):
        self._check_case('resources/test_data_only1', '1'*80)

    def test_only_zeros(self):
        self._check_case('resources/test_data_only0', '0'*80)

    def _check_case(self, filename, exp_res):
        res = steg.get_data_from_file(filename)
        self.assertEqual(exp_res, res)


class TestEncoding(unittest.TestCase):
    def test_the_same_sizes(self):
        options = CodingOptions()
        source_way = 'resources/source.bmp'
        res_way = 'resources/res.bmp'
        steg.encode('10101010'*10, source_way, options, res_way)
        with open(source_way, 'rb') as fs, open(res_way, 'rb') as fr:
            with Image.open(fs) as s, Image.open(fr) as r:
                size_s = s.size
                size_r = r.size
                self.assertEqual(size_s, size_r)

    def test_only_little_changes(self):
        options = CodingOptions()
        source_way = 'resources/source.bmp'
        res_way = 'resources/res.bmp'
        steg.encode('10101010'*10, source_way, options, res_way)
        with open(source_way, 'rb') as fs, open(res_way, 'rb') as fr:
            with Image.open(fs) as s, Image.open(fr) as r:
                width, height = s.size
                for i in range(width):
                    for j in range(height):
                        s_pixel = s.getpixel((i, j))
                        r_pixel = r.getpixel((i, j))
                        for t in range(3):
                            self.assertTrue(
                                math.fabs(s_pixel[t] - r_pixel[t]) <= 1)

    def test_too_big_data(self):
        with self.assertRaises(ValueError):
            options = CodingOptions()
            source_way = 'resources/source.bmp'
            res_way = 'resources/res.bmp'
            steg.encode('10101010' * 100000000, source_way, options, res_way)


class TestGetDecodedDataWithPolynomial(unittest.TestCase):
    def test_simple_case(self):
        options = CodingOptions()
        data = '10000000'
        exp_res = steg.get_updated_data(data)[32:]
        self._check_case(options,
                         'resources/test_encoded_111_10101010.bmp',
                         exp_res)

    def _check_case(self, options, image, exp_res):
        res = steg.get_decoded_data_with_polynomial(image, options)
        self.assertEqual(exp_res, res)


class TestDecoding(unittest.TestCase):
    def test_simple_cases(self):
        self._check_case('1010101010101010',
                         'resources/decoded_1010101010101010')
        self._check_case('1111111111111111',
                         'resources/decoded_1111111111111111')

    def _check_case(self, data, filename):
        steg.decode(data, filename)
        with open(filename, 'rb') as f:
            res = f.read(len(data) + 1)
        self.assertEqual(int(data, 2).to_bytes(len(data) // 8, byteorder='big'),
                         res)


if __name__ == '__main__':
    unittest.main()
