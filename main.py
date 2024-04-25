import numpy
from PIL import Image


def to_binary(s: str):
    return ''.join(bin(ord(i))[2:].rjust(8, '0') for i in s)


def to_str(s_bin: str):
    return ''.join(chr(int(s_bin[i:i + 8], 2)) for i in range(0, len(s_bin), 8))
    # return ''.join(int)  # ord!


def embed(p1: list, p2: list, message: bin, ):
    return p1, p2


# path = input(f'Введите путь к файлу:\n')
# if not path:
#     path = "source_copy.png"
# im = Image.open(path)
# matrix = numpy.array(im)
#
# for line in range(len(matrix)):
#     for row in range(0, len(matrix[line]), 2):
#         r1, g1, b1, a1 = matrix[line][row]
#
