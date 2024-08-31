# Copyright (c) 2021
# MKS Plugin is released under the terms of the AGPLv3 or higher.
# Edited by its.Andrew & cltWilly

from PyQt5.QtGui import QImage
import sys, base64

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
    screenshot_string += "\r"
    return simage,gimage,screenshot_string

def get_preview_from_png(image):  
    screenshot_string = ""

    if image:
        simage, gimage, screenshot_string = generate_preview(image)
    else:
        print("Skipping adding screenshot")
        return
    
    #print("preview done")
    
    return screenshot_string

# -- My code --
def getGcodePrusaPreview(gcodePath): # resolution="400x300"
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

def convertBase64ToQImage(base64String):
    image_data = base64.b64decode(base64String)
    image = QImage()
    image.loadFromData(image_data)
    
    return image

def formatePreviewToGcode(preview):
    print(preview)
    formated_preview = ""
    
    for i, line in enumerate(preview):
        if i == 0:
            formated_preview += f";simage:{line}"
            
        formated_preview += f"M10086 ;{line}"
        
    return formated_preview

def savePreviewToGcode(preview, outputFilePath):    
    # Read the file and insert the preview at the beginning
    with open(outputFilePath, 'r') as f:
        lines = f.readlines()
        
        lines.insert(0, f"; generated preview\n{preview}\n\n")
        
    # Write new content to the file
    with open(outputFilePath, 'w') as fo:
        fo.writelines(lines)

# Actual usage
sourceFile=sys.argv[1]

# přečtení souboru a získání Base64 stringu
img_Base64 = getGcodePrusaPreview(sourceFile)

# konverze Base64 na QImage
qimage = convertBase64ToQImage(img_Base64)

# získání preview pro tiskárnu z QImage
img_preview = get_preview_from_png(qimage)

# uložení preview do Gcode souboru
savePreviewToGcode(img_preview, sourceFile)

print("done")