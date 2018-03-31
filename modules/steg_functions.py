from PIL import Image


def get_data_to_encode_from_file(filename):
    data = get_data_from_file(filename)
    upd_data = get_updated_data(data)
    return upd_data


def get_data_from_file(filename):
    result = []
    step = 1024
    with open(filename, 'rb') as f:
        while True:
            data = f.read(step)
            if len(data) == 0:
                break
            for byte in data:
                bin_str = bin(byte)[2:]
                res_bin_str = '0' * (8 - len(bin_str)) + bin_str
                result.append(res_bin_str)
    data = ''.join(result)
    return data


def get_updated_data(data):
    POLYNOMIAL = '11000000000000101'  # CRC-16-IBM
    # Длина данных + CRC-полинома + CRC-code
    data_len = len(data) + 65 + (len(POLYNOMIAL) - 1)
    bin_data_len = bin(data_len)[2:]
    bin_data_len = '0' * (32 - len(bin_data_len)) + bin_data_len
    normalized_polynomial = normalize_polynomial(POLYNOMIAL)
    return (bin_data_len + normalized_polynomial
            + data + get_crc_from_clear_data(data, POLYNOMIAL))


def get_crc_from_updated_data(data, polynomial):
    next_idx = len(polynomial)
    cur_data = data[:len(polynomial)]
    while len(cur_data) == len(polynomial):
        prev_idx = next_idx
        is_beginning = True
        new_data = ''
        for i in range(len(polynomial)):
            if cur_data[i] == polynomial[i]:
                if is_beginning:
                    next_idx += 1
                else:
                    new_data += '0'
            else:
                new_data += '1'
                is_beginning = False
        cur_data = new_data + data[prev_idx: next_idx]
    return '0' * (len(polynomial) - len(cur_data) - 1) + cur_data


def get_crc_from_clear_data(data, polynomial):
    if len(polynomial) > 65:
        raise ValueError('Слишком большой CRC-полином')
    data += '0' * (len(polynomial) - 1)
    return get_crc_from_updated_data(data, polynomial)


def denormalize_polynomial(polynomial):
    idx = 0
    while polynomial[idx] == '0':
        idx += 1
    return polynomial[idx:]


def normalize_polynomial(polynomial):
    return '0' * (65 - len(polynomial)) + polynomial


def crc_is_right(data, polynomial):
    cur_crc = get_crc_from_updated_data(data, polynomial)
    return cur_crc == '0' * (len(polynomial) - 1)


def encode(data, image, options, save_to):
    file = open(image, 'rb')
    original_image = Image.open(file)
    width, height = original_image.size
    steg_image = Image.new('RGB', (width, height))
    data_index = 0
    data_len = len(data)
    data += '0000000'
    # Нули в конце нужны для того, чтобы не обрабатывать случай, когда,
    # к примеру, r_count больше, чем кол-во оставшихся для кодирования бит
    if data_len > options.rgb_count * width * height:
        file.close()
        steg_image.close()
        original_image.close()
        raise ValueError('Не хватает места для шифрования. '
                         'Попробуйте использовать больше бит')
    for i in range(width):
        for j in range(height):
            pixel = original_image.getpixel((i, j))
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]

            if data_index >= data_len:
                steg_image.putpixel((i, j), (r, g, b))
                continue
            data_to_encode = data[data_index: data_index + options.r_count]
            data_index += options.r_count
            r = get_encoded_thread(r, data_to_encode)

            if data_index >= data_len:
                steg_image.putpixel((i, j), (r, g, b))
                continue
            data_to_encode = data[data_index: data_index + options.g_count]
            data_index += options.g_count
            g = get_encoded_thread(g, data_to_encode)

            if data_index >= data_len:
                steg_image.putpixel((i, j), (r, g, b))
                continue
            data_to_encode = data[data_index: data_index + options.b_count]
            data_index += options.b_count
            b = get_encoded_thread(b, data_to_encode)

            steg_image.putpixel((i, j), (r, g, b))
    steg_image.save(save_to)
    file.close()
    steg_image.close()
    original_image.close()


def get_decoded_data_with_polynomial(image, options):
    image_file = open(image, 'rb')
    encoded_image = Image.open(image_file)
    width, height = encoded_image.size
    result = []
    bin_len = ''
    expected_data_len = None
    cur_res_len = 0
    data_decoded = False
    for i in range(width):
        if data_decoded:
            break
        for j in range(height):
            r, g, b = encoded_image.getpixel((i, j))
            if len(bin_len) < 32:
                bin_len += (get_data_from_thread(r, options.r_count) +
                            get_data_from_thread(g, options.g_count) +
                            get_data_from_thread(b, options.b_count))
                continue
            if expected_data_len is None:
                expected_data_len = int(bin_len[:32], 2)
                result.append(bin_len[32:])
                cur_res_len += len(bin_len) - 32
            result.append(get_data_from_thread(r, options.r_count))
            result.append(get_data_from_thread(g, options.g_count))
            result.append(get_data_from_thread(b, options.b_count))
            cur_res_len += options.rgb_count
            if cur_res_len >= expected_data_len:
                data_decoded = True
                break
    encoded_image.close()
    image_file.close()
    return ''.join(result)[:expected_data_len]


def get_and_check_decoded_data(data_with_polynomial):
    normalized_polynomial = data_with_polynomial[:65]
    origin_polynomial = denormalize_polynomial(normalized_polynomial)
    data_with_crc = data_with_polynomial[65:]
    crc_check_res = crc_is_right(data_with_crc, origin_polynomial)
    data = data_with_crc[:-len(origin_polynomial) + 1]
    return crc_check_res, data


def decode(decoded_data, decodefile):
    with open(decodefile, 'wb') as f:
        idx = 0
        max_len = len(decoded_data)
        while idx < max_len:
            str_byte = decoded_data[idx: idx + 8]
            idx += 8
            int_byte = int(str_byte, 2)
            f.write(int_byte.to_bytes(1, byteorder='big'))


def get_encoded_thread(cur_thread, data):
    if data == '':
        return cur_thread
    if len(data) > 8:
        raise ValueError('В один канал можно зашифровать не более восьми бит')
    value_to_or = int(data, 2)
    binary_value_to_and = '1' * (8 - len(data)) + data
    value_to_and = int(binary_value_to_and, 2)
    return (cur_thread | value_to_or) & value_to_and


def get_data_from_thread(thread, bits_count):
    bin_value = bin(thread)[2:]
    bin_value = '0' * (8 - len(bin_value)) + bin_value
    return bin_value[8 - bits_count:]
