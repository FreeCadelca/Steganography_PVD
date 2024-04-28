import numpy
from PIL import Image
import sys
from pvd import *


path = input(f'Введите путь к изначальному стегоизображению:\n')
path = "Images\\stego-image.png" if not path else path
im = Image.open(path)
matrix_og = numpy.array(im)
message_og = extract_from_matrix(matrix_og)
message_og_bin = to_binary(message_og)

path = input(f'Введите путь к изменённому стегоизображению:\n')
path = "Images\\stego-image.png" if not path else path
im = Image.open(path)
matrix_mod = numpy.array(im)
message_mod = extract_from_matrix(matrix_mod)
message_mod_bin = to_binary(message_mod)

count = 0
for i in range(min(len(message_og_bin), len(message_mod_bin))):
    count += 1 if message_og_bin[i] == message_mod_bin[i] else 0
if len(message_og_bin) > len(message_mod_bin):
    count += len(message_og_bin) - len(message_mod_bin)
print(f'BER: {count / len(message_og_bin)}')