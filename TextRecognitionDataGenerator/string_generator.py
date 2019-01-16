import random
import re
import string
import requests
import numpy as np

from bs4 import BeautifulSoup

def create_strings_from_file(filename, count):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, 'r', encoding="utf8") as f:
        lines = [l.strip()[0:200] for l in f.readlines()]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) >= count - len(strings):
                strings.extend(lines[0:count - len(strings)])
            else:
                strings.extend(lines)

    return strings


def create_strings_from_file_len(filename, count, length):
    """
        Create all strings by reading lines in specified files
    """

    strings = []

    with open(filename, 'r', encoding="utf8") as f:
        lines = [l.strip('\n')[0:200] for l in f.readlines()]
        # lines = [ch.strip('\n') for ch in lines]
        if len(lines) == 0:
            raise Exception("No lines could be read in file")
        while len(strings) < count:
            if len(lines) >= count - len(strings):
                # strings.extend(lines[0:count - len(strings)])
                tmp_str = lines[0:count - len(strings)]
                for str in tmp_str:
                    strings.append(str_process_solid_len(str, length))

            else:
                for str in lines:
                    strings.append(str_process_solid_len(str, length))

    return strings


def str_process_solid_len(str, length):
    res = ''
    if len(str) < length:
        tmp_space = ''
        for tmp_cnt in range(length - len(str)):
            tmp_space = tmp_space + " "
            res = str + tmp_space
    else:
        start = np.random.randint(0, len(str) - length)
        res = str[start: start + length]

    return res


def create_strings_from_dict(length, allow_variable, count, lang_dict):
    """
        Create all strings by picking X random word in the dictionnary
    """

    dict_len = len(lang_dict)
    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, random.randint(1, length) if allow_variable else length):
            current_string += lang_dict[random.randrange(dict_len)][:-1]
            current_string += ' '
        strings.append(current_string[:-1])
    return strings

def create_strings_from_wikipedia(minimum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    while len(sentences) < count:
        # We fetch a random page
        page = requests.get('https://{}.wikipedia.org/wiki/Special:Random'.format(lang))

        soup = BeautifulSoup(page.text, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        # Only take a certain length
        lines = list(filter(
            lambda s:
                len(s.split(' ')) > minimum_length
                and not "Wikipedia" in s
                and not "wikipedia" in s,
            [
                ' '.join(re.findall(r"[\w']+", s.strip()))[0:200] for s in soup.get_text().splitlines()
            ]
        ))

        # Remove the last lines that talks about contributing
        sentences.extend(lines[0:max([1, len(lines) - 5])])

    return sentences[0:count]

def create_strings_randomly(length, allow_variable, count, let, num, sym, lang):
    """
        Create all strings by randomly sampling from a pool of characters.
    """

    # If none specified, use all three
    if True not in (let, num, sym):
        let, num, sym = True, True, True

    pool = ''
    if let:
        if lang == 'cn':
            pool += ''.join([chr(i) for i in range(19968, 40908)]) # Unicode range of CHK characters
        else:
            pool += string.ascii_letters
    if num:
        pool += "0123456789"
    if sym:
        pool += "!\"#$%&'()*+,-./:;?@[\\]^_`{|}~"

    if lang == 'cn':
        min_seq_len = 1
        max_seq_len = 2
    else:
        min_seq_len = 2
        max_seq_len = 10

    strings = []
    for _ in range(0, count):
        current_string = ""
        for _ in range(0, random.randint(1, length) if allow_variable else length):
            seq_len = random.randint(min_seq_len, max_seq_len)
            current_string += ''.join([random.choice(pool) for _ in range(seq_len)])
            current_string += ' '
        strings.append(current_string[:-1])
    return strings

if __name__ == '__main__':
    str = '山东省临沂市莒南县十字路镇大山前社区X单元xxx室'
    str2 = '山东省'

    file_name = 'texts/test.txt'
    count = 10
    length = 5
    strings = create_strings_from_file_len(file_name, count, length)

    print(len(strings))
    for str in strings:
        print(str)

    # for i in range(10):
    #     print(str_process_solid_len(str2, 10))