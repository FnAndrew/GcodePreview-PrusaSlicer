import base64
from io import BytesIO
from PIL import Image
from array import array
# from UM.Application import Application
from PyQt6 import QtCore
# from UM.Logger import Logger


from . import Constants
# from .encoders import ColPicEncoder

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

def custom_encode(scaled_image, img_type, img_size):
    result = ""
    color16 = array('H')
    for i in range(img_size.height()):
        for j in range(img_size.width()):    
            rgb = convert_to_rgb(scaled_image, i, j)
            color16.append(rgb)
    max_size = img_size.height()*img_size.width()*10
    output_data = bytearray(max_size)
    resultInt = ColPicEncoder.ColPic_EncodeStr(
        color16, 
        img_size.height(), 
        img_size.width(), 
        output_data, 
        max_size, 
        1024
    )
    data_without_zeros = str(output_data).replace('\\x00', '')
    data = data_without_zeros[2:len(data_without_zeros) - 2]
    each_line_max = 1024 - 8 - 1
    max_lines = int(len(data)/each_line_max)
    length_to_append = each_line_max - 3 - int(len(data)%each_line_max)+10
    j = 0
    for i in range(len(output_data)):
        if (output_data[i] != 0):
            if j == max_lines*each_line_max:
                result += '\r;' + img_type + chr(output_data[i])
            elif j == 0:
                result += img_type + chr(output_data[i])
            elif j%each_line_max == 0:
                result += '\r' + img_type + chr(output_data[i])
            else:
                result += chr(output_data[i])
            j += 1
    result += '\r;'
    for m in range(length_to_append):
        result += '0'
    return result

def decode_base64_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def add_screenshot_str(img_base64, width, height, img_type, encoded):
    result = ""
    img = decode_base64_image(img_base64)
    scaled_image = img.scaled(width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    img_size = scaled_image.size()
    try:
        if encoded:
            result = custom_encode(scaled_image, img_type, img_size)
        else:
            result = default_encode(scaled_image, img_type, img_size)
    except Exception as e:
        print("Unable to encode screenshot: " + str(e))
    return result

# def take_screenshot():
#     return Snapshot.snapshot(width = 900, height = 900)

# def generate_preview(global_container_stack, image_base64):
#     screenshot_string = ""
#     simage = 0
#     gimage = 0
#     meta_data = global_container_stack.getMetaData()
#     print("Get current preview settings.")
#     encoded = False
#     if Constants.IS_PREVIEW_ENCODED in meta_data:
#         encoded = True
#     if Constants.SIMAGE in meta_data:
#         simage = int(global_container_stack.getMetaDataEntry(Constants.SIMAGE))
#         print("mks_simage value: " + str(simage))
#         screenshot_string += add_screenshot_str(image_base64, simage, simage, ";simage:",encoded)
#     if Constants.GIMAGE in meta_data:
#         gimage = int(global_container_stack.getMetaDataEntry(Constants.GIMAGE))
#         print("mks_gimage value: " + str(gimage))
#         screenshot_string += add_screenshot_str(image_base64, gimage, gimage, ";;gimage:",encoded)
#     screenshot_string += "\r"
#     return simage,gimage,screenshot_string

def add_preview(self, image_base64):
    # application = Application.getInstance()
    # scene = application.getController().getScene()
    # global_container_stack = application.getGlobalContainerStack()
    # if not global_container_stack:
    #     return

    gcode_dict = getattr(scene, "gcode_dict", {})
    if not gcode_dict:
        print("Scene has no gcode to process")
        return

    dict_changed = False
    processed_marker = ";MKSPREVIEWPROCESSED\n"

    screenshot_string = ""
    simage = 0
    gimage = 0

    # if image_base64:
    #     simage, gimage, screenshot_string = generate_preview(global_container_stack, image_base64)
    # else:
    #     print("Skipping adding screenshot")
    #     return
    
    for plate_id in gcode_dict:
        gcode_list = gcode_dict[plate_id]
        if len(gcode_list) < 2:
            print("Plate %s does not contain any layers", plate_id)
            continue

        if processed_marker in gcode_list[0]:
            print("Plate %s has already been processed", plate_id)
            continue

        gcode_list[0] += processed_marker
        gcode_list[0] += "; Postprocessed by [MKS WiFi plugin](https://github.com/PrintMakerLab/mks-wifi-plugin)\n"
        gcode_list[0] += "; simage=%d\n" % simage
        gcode_list[0] += "; gimage=%d\n" % gimage
        gcode_list[0] = screenshot_string + gcode_list[0]
        gcode_dict[plate_id] = gcode_list
        dict_changed = True

    if dict_changed:
        setattr(scene, "gcode_dict", gcode_dict)
