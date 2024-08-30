# Copyright (c) 2021
# MKS Plugin is released under the terms of the AGPLv3 or higher.
from array import array
from PyQt6 import QtCore
from PyQt5.QtGui import QImage

def add_leading_zeros(rgb):
    str_hex = "%x" % rgb
    str_hex_len = len(str_hex)
    if str_hex_len == 3:
        str_hex = '0' + str_hex[0:3]
    elif str_hex_len == 2:
        str_hex = '00' + str_hex[0:2]
    elif str_hex_len == 1:
        str_hex = '000' + str_hex[0:1]
    return str_hex

def convert_to_rgb(image, height_pixel, width_pixel):
    pixel_color = image.pixelColor(width_pixel, height_pixel)
    r = pixel_color.red() >> 3
    g = pixel_color.green() >> 2
    b = pixel_color.blue() >> 3
    rgb = (r << 11) | (g << 5) | b
    return rgb


def default_encode(scaled_image, img_type, img_size):
    result = img_type
    datasize = 0
    for i in range(img_size.height()):
        for j in range(img_size.width()):
            rgb = convert_to_rgb(scaled_image, i, j)
            str_hex = add_leading_zeros(rgb)
            if str_hex[2:4] != '':
                result += str_hex[2:4]
                datasize += 2
            if str_hex[0:2] != '':
                result += str_hex[0:2]
                datasize += 2
            if datasize >= 50:
                datasize = 0
        result += '\rM10086 ;'
        if i == img_size.height() - 1:
            result += "\r"
    return result


def add_screenshot_str(img, width, height, img_type, encoded):
    result = ""
    scaled_image = img.scaled(width, height)
    img_size = scaled_image.size()
    try:
        result = default_encode(scaled_image, img_type, img_size)
    except Exception as e:
        print("Unable to encode screenshot: " + str(e))
    return result

def generate_preview(image):
    screenshot_string = ""
    simage = 100
    gimage = 200
    print("Get current preview settings.")
    encoded = False

    screenshot_string += add_screenshot_str(image, simage, simage, ";simage:",encoded)
    #screenshot_string += add_screenshot_str(image, gimage, gimage, ";;gimage:",encoded)
    screenshot_string += "\r"
    return simage,gimage,screenshot_string

def add_preview():
    # TODO import Gcode
    processed_marker = ";MKSPREVIEWPROCESSED\n"

    image = QImage("wolf_big.png")
    screenshot_string = ""
    simage = 0
    gimage = 0

    if image:
        simage, gimage, screenshot_string = generate_preview(image)
    else:
        print("Skipping adding screenshot")
        return
    
    #print(screenshot_string)
    print("upečeno")
    
    with open("plugin-output.txt", 'w') as f:
        f.write(screenshot_string)
    
    # for plate_id in gcode_dict:
    #     gcode_list = gcode_dict[plate_id]
    #     if len(gcode_list) < 2:
    #         print("Plate %s does not contain any layers", plate_id)
    #         continue

    #     if processed_marker in gcode_list[0]:
    #         print("Plate %s has already been processed", plate_id)
    #         continue

    #     # adding to header
    #     gcode_list[0] += processed_marker
    #     gcode_list[0] += "; Postprocessed by [MKS WiFi plugin](https://github.com/PrintMakerLab/mks-wifi-plugin)\n"
    #     gcode_list[0] += "; simage=%d\n" % simage
    #     gcode_list[0] += "; gimage=%d\n" % gimage
    #     gcode_list[0] = screenshot_string + gcode_list[0]
    #     gcode_dict[plate_id] = gcode_list
    #     dict_changed = True

add_preview()