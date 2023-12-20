from pylab import *  # to use mean , median , max , min , range

global filename


def general_operation(op, num, general_image):
    for i in range(general_image.shape[0]):
        for j in range(general_image.shape[1]):
            pixel = general_image[i, j]
            new_pixel = op(pixel, num)
            condition(new_pixel, general_image, i, j)


def stretch_operation(stretch_image):
    for i in range(stretch_image.shape[0]):
        for j in range(stretch_image.shape[1]):
            pixel = stretch_image[i, j]
            condition_stretch(pixel, stretch_image, i, j)


def condition(new_pixel, image, i, j):
    if new_pixel >= 255:
        image[i, j] = 255
    elif new_pixel < 0:
        image[i, j] = 0
    else:
        image[i, j] = new_pixel


low_pixel = 5
high_pixel = 170


def condition_stretch(new_pixel, image, i, j):
    if new_pixel >= high_pixel:
        image[i, j] = 255
    elif new_pixel <= low_pixel:
        image[i, j] = 0
    elif low_pixel <= new_pixel <= high_pixel:
        image[i, j] = 255 * ((new_pixel - low_pixel) / (high_pixel - low_pixel))


def outlier(image3):
    D = 0.2
    # size = int(input('please enter the size of mask: '))
    # step = int((size - 1) / 2)
    step1 = int((3 - 1) / 2)
    rows, cols = image3.shape
    for i in range(0, rows):
        for j in range(0, cols):
            p = image3[i, j]
            neighbor = []
            for x in range(i - step1, i + step1 + 1):
                for y in range(j - step1, j + step1 + 1):
                    if x < 0 or y < 0 or x > rows - 1 or y > cols - 1:
                        pass
                    else:
                        neighbor.append(image3[x, y])
            m = mean(neighbor)
            if abs(p - m) > D:
                image3[i, j] = m


def general_processing(general_image, operation, value):
    general_operation(operation, value, general_image)


def general_processing_color(general_image, operation, value, out_image):
    general_operation(operation, value, general_image)
