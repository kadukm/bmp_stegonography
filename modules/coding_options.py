class CodingOptions:
    def __init__(self, r_count=1, g_count=1, b_count=1):
        if r_count + g_count + b_count == 0:
            raise ValueError('Нельзя использовать 0 бит')
        if r_count > 8 or g_count > 8 or b_count > 8:
            raise ValueError('Нельзя использовать более 8-и бит в одном канале')
        self.r_count = r_count
        self.g_count = g_count
        self.b_count = b_count

    @classmethod
    def get_options_from(cls, data):
        opt_dict = {'r': 0, 'g': 0, 'b': 0}
        for i in range(0, len(data), 2):
            if data[i] not in opt_dict:
                raise KeyError('Unknown color channel')
            opt_dict[data[i]] = int(data[i + 1])
        result = CodingOptions(opt_dict['r'], opt_dict['g'], opt_dict['b'])
        return result

    @property
    def rgb_count(self):
        return self.r_count + self.g_count + self.b_count
