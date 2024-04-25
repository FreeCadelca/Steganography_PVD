import numpy
from PIL import Image

list_of_intervals = ((0, 7), (8, 15), (16, 31), (32, 63), (64, 127), (128, 255))


def to_binary(s: str):
    return ''.join(bin(ord(i))[2:].rjust(8, '0') for i in s)


def to_str(s_bin: str):
    return ''.join(chr(int(s_bin[i:i + 8], 2)) for i in range(0, len(s_bin), 8))
    # return ''.join(int)  # ord!


def get_d_l_u_n(v1: int, v2: int) -> tuple:
    d_k = abs(v1 - v2)
    l_k = None
    u_k = None
    for interval in list_of_intervals:
        if interval[0] <= d_k <= interval[1]:
            l_k = interval[0]
            u_k = interval[1]
            break
    n_k = (u_k - l_k + 1).bit_length() - 1
    return d_k, l_k, u_k, n_k


def embed_to_values(v1: int, v2: int, msg_bin: str):
    d_k, l_k, u_k, n_k = get_d_l_u_n(v1, v2)
    msg_bin_embedding = msg_bin[:n_k]
    m_k = int(msg_bin_embedding, 2)
    d_k_star = l_k + m_k if d_k >= 0 else -(l_k + m_k)
    v1_new = None
    v2_new = None
    if d_k % 2 != 0:
        v1_new = v1 + (d_k_star - d_k + 1) // 2
        v2_new = v2 - (d_k_star - d_k) // 2
    else:
        v1_new = v1 + (d_k_star - d_k) // 2
        v2_new = v2 - (d_k_star - d_k + 1) // 2
    return v1_new, v2_new, n_k


def extract_from_values(v1: int, v2: int):
    d_k, l_k, u_k, n_k = get_d_l_u_n(v1, v2)
    m_k = abs(v1 - v2) - l_k
    m = bin(m_k)[2:].rjust(n_k, '0')
    return m


path = input(f'Введите путь к файлу:\n')
path = "source_copy.png" if not path else path
im = Image.open(path)
matrix = numpy.array(im)

# for line in range(len(matrix)):
#     for row in range(0, len(matrix[line]), 2):
#         r1, g1, b1, a1 = matrix[line][row]
#         r2, g2, b2, a2 = matrix[line][row + 1]
#         print(r1, g1, b1, '\t', r2, g2, b2)
print()
