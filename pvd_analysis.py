import math
import numpy
from PIL import Image


def Covariance(matrix_src: numpy.array, matrix_stg: numpy.array):
    width, height, _ = matrix_src.shape

    src_avg = average(matrix_src)
    stg_avg = average(matrix_stg)

    covariance = [0, 0, 0]
    for line in range(len(matrix_src)):
        for row in range(len(matrix_src[line])):
            for channel in range(len(matrix_src[line][row]) - 1):
                covariance[channel] += ((matrix_src[line][row][channel] - src_avg[channel]) *
                                        (matrix_stg[line][row][channel] - stg_avg[channel]))
    for channel in range(len(covariance)):
        covariance[channel] /= (matrix_src.shape[0] * matrix_src.shape[1])
    return covariance


def MSE(matrix_src: numpy.array, matrix_stg: numpy.array):
    width, height, _ = matrix_src.shape

    total_sum = [0, 0, 0]
    for line in range(len(matrix_src)):
        for row in range(len(matrix_src[line])):
            for channel in range(len(matrix_src[line][row]) - 1):
                total_sum[channel] += (numpy.int16(matrix_src[line][row][channel]) -
                                       numpy.int16(matrix_stg[line][row][channel])) ** 2
    for channel in range(len(total_sum)):
        total_sum[channel] /= (matrix_src.shape[0] * matrix_src.shape[1])
    return total_sum


def PSNR(matrix_src: numpy.array, matrix_stg: numpy.array):
    mse = MSE(matrix_src, matrix_stg)
    return [10 * math.log10((255 ** 2) / mse[channel]) for channel in range(len(mse))]


def PSNR(mse: list):
    return [10 * math.log10((255 ** 2) / mse[channel]) for channel in range(len(mse))]


def RMSE(matrix_src: numpy.array, matrix_stg: numpy.array):
    mse = MSE(matrix_src, matrix_stg)
    return [math.sqrt(mse[channel]) for channel in range(len(mse))]


def RMSE(mse: list):
    return [math.sqrt(mse[channel]) for channel in range(len(mse))]


def dispersion(matrix: numpy.array):
    width, height, _ = matrix.shape
    total_sum = [0, 0, 0]
    for line in range(len(matrix)):
        for row in range(len(matrix[line])):
            for channel in range(len(matrix[line][row]) - 1):
                total_sum[channel] += numpy.int32(matrix[line][row][channel]) ** 2
    for channel in range(len(total_sum)):
        total_sum[channel] /= (width * height)
    avg = average(matrix)
    for channel in range(len(total_sum)):
        total_sum[channel] -= avg[channel] ** 2
    return total_sum


def average(matrix: numpy.array):
    width, height, _ = matrix.shape
    total_sum = [0, 0, 0]
    for line in range(len(matrix)):
        for row in range(len(matrix[line])):
            for channel in range(len(matrix[line][row]) - 1):
                total_sum[channel] += matrix[line][row][channel]
    for channel in range(len(total_sum)):
        total_sum[channel] /= (width * height)
    return total_sum


def SSIM(matrix_src: numpy.array, matrix_stg: numpy.array):
    result = [0, 0, 0]
    k1 = (0.01 * 255) ** 2
    k2 = (0.03 * 255) ** 2
    mu_p = average(matrix_src)
    mu_s = average(matrix_stg)
    cov = Covariance(matrix_src, matrix_stg)
    sigma_p = dispersion(matrix_src)
    sigma_s = dispersion(matrix_src)

    for channel in range(len(result)):
        numerator = (2 * mu_p[channel] * mu_s[channel] + k1) * (2 * cov[channel] + k2)
        denominator = ((mu_p[channel] ** 2 + mu_s[channel] ** 2 + k1) *
                       (sigma_p[channel] ** 2 + sigma_s[channel] ** 2 + k2))
        result[channel] = numerator / denominator
    return result

