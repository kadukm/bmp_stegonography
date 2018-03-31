import argparse
import sys
import gui as gui
from os.path import isfile
from modules import steg_functions as steg
from modules.coding_options import CodingOptions

__version__ = '1.1'
__author__ = 'Kaduk Mikhal'
__email__ = 'mk.shark25@gmail.com'


def main():
    parser = argparse.ArgumentParser()
    set_parser(parser)

    if len(sys.argv) == 1:
        gui.run()
    else:
        args = parser.parse_args()
        parse_args(args)


def set_parser(parser):
    coding_group = parser.add_mutually_exclusive_group()
    coding_group.add_argument('-e', '--encode', dest='file_to_encode', type=str)
    coding_group.add_argument('-d', '--decode', dest='file_to_decode', type=str)
    parser.add_argument('-i', '--in', dest='source_file', type=str)
    parser.add_argument('-a', '--as', dest='save_as', type=str)
    parser.add_argument('-w', '--with', dest='coding_options', type=str,
                        default='r1g1b1')
    parser.add_argument('-s', '--safe', dest='safe_mode', action='store_true')


def parse_args(args):
    if args.file_to_encode is not None:
        try_encode(args)
    elif args.file_to_decode is not None:
        try_decode(args)
    else:
        print('ERROR: please choose some action [ENCODE or DECODE]\n'
              'Use "steg.py -h" for more information')


def try_encode(args):
    error_found = False
    if not isfile(args.file_to_encode):
        error_found = True
        print('ERROR: FILE_TO_ENCODE doesn\'t exist')

    if args.source_file is None:
        error_found = True
        print('ERROR: can\'t encode without SOURCE_FILE')
    elif not isfile(args.source_file):
        error_found = True
        print('ERROR: SOURCE_FILE doesn\'t exist')

    if args.save_as is None:
        error_found = True
        print('ERROR: it is not known how to save the result')

    options = None
    try:
        options = CodingOptions.get_options_from(args.coding_options)
    except Exception:
        error_found = True
        print('ERROR: incorrect coding options')

    if error_found:
        print('\nUse "steg.py -h" for more information')
        return

    data_to_encode = steg.get_data_to_encode_from_file(args.file_to_encode)
    steg.encode(data_to_encode, args.source_file, options, args.save_as)


def try_decode(args):
    error_found = False
    if not isfile(args.file_to_decode):
        error_found = True
        print('ERROR: FILE_TO_ENCODE doesn\'t exist')
    if args.save_as is None:
        error_found = True
        print('ERROR: it is not known how to save the result')
    options = None
    try:
        options = CodingOptions.get_options_from(args.coding_options)
    except Exception:
        error_found = True
        print('ERROR: incorrect coding options')
    if error_found:
        print('\nUse "steg.py -h" for more information')
        return

    decoded_data = steg.get_decoded_data_with_polynomial(args.file_to_decode,
                                                         options)
    normalized_polynomial = decoded_data[:65]
    origin_polynomial = steg.denormalize_polynomial(normalized_polynomial)
    crc = steg.get_crc_from_clear_data(decoded_data, origin_polynomial)
    if '1' in crc:
        if args.safe_mode:
            print('ERROR: decoded data is broken')
            return
    decoded_data = decoded_data[65:-len(origin_polynomial) + 1]
    steg.decode(decoded_data, args.save_as)


if __name__ == '__main__':
    main()
