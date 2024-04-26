import numpy
from PIL import Image
import scipy.misc

list_of_intervals = ((0, 7), (8, 15), (16, 31), (32, 63), (64, 127), (128, 255))


def to_binary(s: str):
    return ''.join(bin(ord(i))[2:].rjust(8, '0') for i in s)


def to_str(s_bin: str):
    return ''.join(chr(int(s_bin[i:i + 8], 2)) for i in range(0, len(s_bin), 8))
    # return ''.join(int)  # ord!


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
            r1, g1, b1, a1 = matrix[line][row]
            r2, g2, b2, a2 = matrix[line][row + 1]
            # 6 - max

            msg_bin_part = ''.join(msg_b[j] for j in range(i, min(i + 6, len(msg_b))))
            new_r1, new_r2, count_of_embedded_symbols = embed_to_values(r1, r2, msg_bin_part)
            matrix[line][row][0], matrix[line][row + 1][0] = new_r1, new_r2
            i += count_of_embedded_symbols
            if i == len(msg_b):
                return matrix

            msg_bin_part = ''.join(msg_b[j] for j in range(i, min(i + 6, len(msg_b))))
            new_g1, new_g2, count_of_embedded_symbols = embed_to_values(g1, g2, msg_bin_part)
            matrix[line][row][1], matrix[line][row + 1][1] = new_g1, new_g2
            i += count_of_embedded_symbols
            if i == len(msg_b):
                return matrix

            msg_bin_part = ''.join(msg_b[j] for j in range(i, min(i + 6, len(msg_b))))
            new_b1, new_b2, count_of_embedded_symbols = embed_to_values(b1, b2, msg_bin_part)
            matrix[line][row][2], matrix[line][row + 1][2] = new_b1, new_b2
            i += count_of_embedded_symbols
            if i == len(msg_b):
                return matrix


def extract_from_matrix(matrix):
    msg_b = ''
    for line in range(len(matrix)):
        for row in range(0, len(matrix[line]), 2):

            msg_b += extract_from_values(matrix[line][row][0], matrix[line][row + 1][0])
            if msg_b[-16:] == ('0' *16):
                return to_str(msg_b[:-16])

            msg_b += extract_from_values(matrix[line][row][1], matrix[line][row + 1][1])
            if msg_b[-16:] == ('0' * 16):
                return to_str(msg_b[:-16])

            msg_b += extract_from_values(matrix[line][row][2], matrix[line][row + 1][2])
            if msg_b[-16:] == ('0' * 16):
                return to_str(msg_b[:-16])


if __name__ == '__main__':
    mode = input("Embed/Extract? [Em/Ex]\n")
    if mode == "Em":
        path = input(f'Введите путь к файлу:\n')
        path = "source_copy.png" if not path else path
        im = Image.open(path)
        matrix = numpy.array(im)

        # message = ("The sun was setting behind the mountains, casting a warm glow over the meadow below. "
        #            "The sound of crickets filled the air, a peaceful symphony of nature. As the day came to an end, "
        #            "I couldn't help but feel grateful for the simple beauty of the world around me.")
        with open("the_princess_and_the_pea", "r") as f:
            message = ''.join(i for i in f.readlines())
        embed_to_matrix(message, matrix)
        out = extract_from_matrix(matrix)
        print(out)
        # matrix[0][0][0] += 255
        # print(matrix)
        # print(matrix.shape)
        # for line in range(512):
        #     for row in range(512):
        #         matrix[line][row] = matrix[line][row][:3]
        print(matrix.shape)
        # # new_img = Image.fromarray(matrix)
        # # new_img.save("output.png")
        # scipy.misc.imsave('output.png', matrix)
        Image.fromarray(matrix).save("stego-image.png")
    else:
        path = input(f'Введите путь к файлу:\n')
        path = "stego-image.png" if not path else path
        im = Image.open(path)
        matrix = numpy.array(im)
        out = extract_from_matrix(matrix)
        print(out)
