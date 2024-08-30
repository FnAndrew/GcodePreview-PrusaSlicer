# Copyright (c) 2021
# MKS Plugin is released under the terms of the AGPLv3 or higher.
from PyQt5.QtGui import QImage
import sys, base64
from io import BytesIO
from PIL import Image

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

def get_preview_from_png(img_Base64):
    
    print("Converting image to QImage")
    
    # image_data = base64.b64decode(img_Base64)
    # image_png = Image.open(BytesIO(image_data))
    
    # with open("./tmp.png", "wb") as f:
    #     f.write()
    # f.close()
    
    # Image.open(BytesIO(base64.b64decode(img_Base64))).save("./tmp.png")
    
    # image = QImage("./tmp.png")
    # image = QImage()
    # image.loadFromData(img_Base64, "PNG")
    
    import base64 
    image_bytes = base64.b64decode(img_Base64)
    image_stream = BytesIO(image_bytes)
    # Open the image using Pillow (PIL)
    image = Image.open(image_stream)
    image.save("./temp.png")
    
    # f = open("./temp.png", "w")
    # f.write(png_recovered)
    # f.close()
    
    image = QImage("temp.png")
    
    print(image.colorCount())
    
    screenshot_string = ""

    if image:
        simage, gimage, screenshot_string = generate_preview(image)
    else:
        print("Skipping adding screenshot")
        return
    
    print(screenshot_string)
    #print("done")
    
    return screenshot_string

# -- My code --
def getGcodePrusaPreview(gcodePath, resolution="400x300"):
    img_string = ""
    inside_thumbnail = False

    # Načtení souboru a zpracování řádků s thumbnail částí
    with open(gcodePath, "r") as f:
        for line in f:
            # Odstranění bílých znaků na začátku a konci řádku
            line = line.strip()

            # Kontrola, zda začíná thumbnail část
            if line.startswith(f"; thumbnail begin"): # 32x32
                inside_thumbnail = True
                continue

            # Kontrola, zda končí thumbnail část
            if line.startswith("; thumbnail end"):
                inside_thumbnail = False
                break

            # Pokud jsme uvnitř thumbnail části, přidáme řádek do výsledného stringu
            if inside_thumbnail:
                img_string += line + '\n'

    # Odstranění posledního nového řádku na konci stringu (volitelné)
    img_string = img_string.rstrip()

    img_Base64 = img_string.replace("; ", "")
    return img_Base64

def formatePreviewToGcode(preview):
    formated_preview = ""
    
    for i, line in enumerate(preview):
        if i == 0:
            formated_preview += f";simage:{line}"
            
        formated_preview += f"M10086 ;{line}"
        
    return formated_preview

def savePreviewToGcode(preview, outputFilePath):
    with open(outputFilePath, 'r') as f:
        lines = f.readlines()
        
        lines.insert(0, preview)

# Actual usage
#sourceFile=sys.argv[1]
sourceFile = "E:/Ostatni - Soubory/3DModels/Gcodes/Testy/trash/Wolf.gcode"

# přečtení souboru a získání Base64 stringu
img_Base64 = getGcodePrusaPreview(sourceFile)

# získání preview pro tiskárnu z Base64 stringu
img_preview = get_preview_from_png(img_Base64)

# zformátování preview pro Gcode
img_preview_formated = formatePreviewToGcode(img_preview)

# uložení preview do Gcode souboru
savePreviewToGcode(img_preview_formated, sourceFile)

print("done")