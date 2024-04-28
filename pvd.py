import numpy
from PIL import Image
import sys
from pvd_analysis import *

list_of_intervals = ((0, 7), (8, 15), (16, 31), (32, 63), (64, 127), (128, 255))


def calibration_of_matrix(matrix: numpy.array):
    for line in range(len(matrix)):
        for row in range(len(matrix[line])):
            for channel in range(3):
                matrix[line][row][channel] = max(8, min(255 - 8, matrix[line][row][channel]))


def to_binary(s: str):
    return ''.join(bin(ord(i))[2:].rjust(8, '0') for i in s)


def to_str(s_bin: str):
    return ''.join(chr(int(s_bin[i:i + 8], 2)) for i in range(0, len(s_bin), 8))


def get_d_l_u_n(v1: int, v2: int) -> tuple:
    d_k = numpy.int16(v1) - numpy.int16(v2)
    l_k = None
    u_k = None
    for interval in list_of_intervals:
        if interval[0] <= abs(d_k) <= interval[1]:
            l_k = interval[0]
            u_k = interval[1]
            break
    n_k = (u_k - l_k + 1).bit_length() - 1
    return d_k, l_k, u_k, n_k


def embed_to_values(v1: int, v2: int, msg_bin: str):
    d_k, l_k, u_k, n_k = get_d_l_u_n(v1, v2)
    msg_bin_embedding = None
    if n_k <= len(msg_bin):
        msg_bin_embedding = msg_bin[:n_k]
    else:
        msg_bin_embedding = msg_bin
        n_k = len(msg_bin)
    m_k = int(msg_bin_embedding, 2)
    d_k_star = l_k + m_k if d_k >= 0 else -(l_k + m_k)
    v1_new = None
    v2_new = None
    if abs(d_k) % 2 != 0:
        v1_new = v1 + (d_k_star - d_k + 1) // 2
        v2_new = v2 - (d_k_star - d_k) // 2
    else:
        v1_new = v1 + (d_k_star - d_k) // 2
        v2_new = v2 - (d_k_star - d_k + 1) // 2
    return v1_new, v2_new, n_k


def extract_from_values(v1: int, v2: int):
    d_k, l_k, u_k, n_k = get_d_l_u_n(v1, v2)
    m_k = abs(numpy.int16(v1) - numpy.int16(v2)) - l_k
    m = bin(m_k)[2:].rjust(n_k, '0')
    return m


# def embed_to_channel(message):
#     pass


def embed_to_matrix(message, matrix):
    msg_b = to_binary(message)
    msg_b += '0' * 16
    i = 0
    for line in range(len(matrix)):
        for row in range(0, len(matrix[line]), 2):
            r1, g1, b1, _ = matrix[line][row]
            r2, g2, b2, _ = matrix[line][row + 1]
            # 6 - max

            msg_bin_part = ''.join(msg_b[j] for j in range(i, min(i + 6, len(msg_b))))
            new_r1, new_r2, count_of_embedded_symbols = embed_to_values(r1, r2, msg_bin_part)
            matrix[line][row][0], matrix[line][row + 1][0] = new_r1, new_r2
            i += count_of_embedded_symbols
            if i >= len(msg_b):
                return len(msg_b)

            msg_bin_part = ''.join(msg_b[j] for j in range(i, min(i + 6, len(msg_b))))
            new_g1, new_g2, count_of_embedded_symbols = embed_to_values(g1, g2, msg_bin_part)
            matrix[line][row][1], matrix[line][row + 1][1] = new_g1, new_g2
            i += count_of_embedded_symbols
            if i >= len(msg_b):
                return len(msg_b)

            msg_bin_part = ''.join(msg_b[j] for j in range(i, min(i + 6, len(msg_b))))
            new_b1, new_b2, count_of_embedded_symbols = embed_to_values(b1, b2, msg_bin_part)
            matrix[line][row][2], matrix[line][row + 1][2] = new_b1, new_b2
            i += count_of_embedded_symbols
            if i >= len(msg_b):
                return len(msg_b)
    return i


def extract_from_matrix(matrix):
    msg_b = ''
    for line in range(len(matrix)):
        for row in range(0, len(matrix[line]), 2):

            msg_b += extract_from_values(matrix[line][row][0], matrix[line][row + 1][0])
            if msg_b[-16:] == ('0' * 16):
                return to_str(msg_b[:-16])

            msg_b += extract_from_values(matrix[line][row][1], matrix[line][row + 1][1])
            if msg_b[-16:] == ('0' * 16):
                return to_str(msg_b[:-16])

            msg_b += extract_from_values(matrix[line][row][2], matrix[line][row + 1][2])
            if msg_b[-16:] == ('0' * 16):
                return to_str(msg_b[:-16])
    return to_str(msg_b)


def get_all_possible_bytes(matrix):
    count = 0
    i = 0
    for line in range(len(matrix)):
        for row in range(0, len(matrix[line]), 2):
            r1, g1, b1, _ = matrix[line][row]
            r2, g2, b2, _ = matrix[line][row + 1]

            _, _, _, n_k1 = get_d_l_u_n(r1, r2)
            _, _, _, n_k2 = get_d_l_u_n(g1, g2)
            _, _, _, n_k3 = get_d_l_u_n(b1, b2)
            count += n_k1 + n_k2 + n_k3
    return count


if __name__ == '__main__':
    mode = input("Embed/Extract/getMaxBits? [Em/Ex/Max]\n")
    path = input(f'Введите путь к файлу:\n')
    if mode == "Em":
        path = "Images\\source.png" if not path else path
        im = Image.open(path)
        matrix = numpy.array(im)
        old_matrix = matrix.copy()
        calibration_of_matrix(matrix)
        print('Введите сообщение (должны использоваться только символы из ASCII):')
        message = ''
        new_line = input()
        while len(new_line):
            message += new_line + '\n'
            new_line = input()
        # with open("Texts/the_princess_and_the_pea_long", "r") as f:
        #     message = ''.join(i for i in f.readlines())
        embedded_bits = embed_to_matrix(message, matrix)
        Image.fromarray(matrix).save("Images\\stego-image.png")
        print("Информация встроена")

        mse = MSE(old_matrix, matrix)
        specifications = {
            "MSE": sum(mse) / 3,
            "PSNR": sum(PSNR(mse)) / 3,
            "RMSE": sum(RMSE(mse)) / 3,
            "SSIM": sum(SSIM(old_matrix, matrix)) / 3,
            "EC": [embedded_bits / (matrix.shape[0] * matrix.shape[1]), embedded_bits / 8],
        }
        print("Характеристики незаметности встраивания:")
        for s in specifications.keys():
            print(f'{s}: {specifications[s]}')

    elif mode == "Ex":
        path = "Images\\stego-image.png" if not path else path
        im = Image.open(path)
        matrix = numpy.array(im)
        out = extract_from_matrix(matrix)
        print(out)
    else:
        path = "Images\\source.png" if not path else path
        im = Image.open(path)
        matrix = numpy.array(im)
        count = get_all_possible_bytes(matrix)
        print(count, count // 8)
