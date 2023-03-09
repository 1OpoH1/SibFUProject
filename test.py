def make_regex_string(array: list):
        try:
            array = '|'.join(array)
        except TypeError:
            for i in range(len(array)):
                array[i] = make_string(array[i])
        if type(array) == list:
            return '|'.join(array)
        else:
            return array



