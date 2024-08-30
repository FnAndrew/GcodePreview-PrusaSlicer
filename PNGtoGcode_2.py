import base64
from io import BytesIO
from PIL import Image
from array import array

def add_leading_zeros(rgb):
    str_hex = "%x" % rgb
    return str_hex.zfill(4)

def convert_to_rgb(image, height_pixel, width_pixel):
    pixel_color = image.getpixel((width_pixel, height_pixel))
    r = pixel_color[0] >> 3
    g = pixel_color[1] >> 2
    b = pixel_color[2] >> 3
    rgb = (r << 11) | (g << 5) | b
    return rgb

def default_encode(scaled_image, img_type, img_size):
    result = img_type
    datasize = 0
    for i in range(img_size[1]):
        for j in range(img_size[0]):
            rgb = convert_to_rgb(scaled_image, i, j)
            str_hex = add_leading_zeros(rgb)
            result += str_hex[2:4] + str_hex[0:2]
            datasize += 4
            if datasize >= 50:
                datasize = 0
        result += '\rM10086 ;'
        if i == img_size[1] - 1:
            result += "\r"
    return result

def decode_base64_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def add_screenshot_str(img_base64, width, height, img_type):
    img = decode_base64_image(img_base64)
    scaled_image = img.resize((width, height), Image.LANCZOS)
    img_size = scaled_image.size
    return default_encode(scaled_image, img_type, img_size)

def generate_preview(image_base64, simage_size, gimage_size):
    screenshot_string = ""
    if simage_size > 0:
        screenshot_string += add_screenshot_str(image_base64, simage_size, simage_size, ";simage:")
    if gimage_size > 0:
        screenshot_string += add_screenshot_str(image_base64, gimage_size, gimage_size, ";;gimage:")
    screenshot_string += "\r"
    return screenshot_string

#; thumbnail begin 32x32 2136
base64_image = """

;

; iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAGCUlEQVR4AdWXSWhVZxiGz6ogXWVVEL
; pRCgUXFVoQSnBtFiLNqoWAUKVdKC5UEIcYg0aNZh6aeZ7neZ4TkzQxsbemMaTUakkXFqKEIgTM4u/7
; HO4XDulNsdS2eOBwDv9//m94v/f73ns9722+oqKi3t27d2+U939cR44cOfiNrlu3bhXHxMR8vGfPnn
; e8/+Ii4ytXrnxRVFTU39zcPFxTUzOemZnZd+nSpS//dTSio6M/rKioSMzKylqsqqoKlZWVzRUXF880
; NDSMZmRkzAiQ+MOHD3/kvelr//79B0+ePPl1U1NT59DQ0PP5+Xk3NjbmFIyT45WUlJRQZ2fnQGlp6X
; R+fn7T2bNnP4Mf3pu4gFXZ/jI5OemGh4fdwsKCW15edgQhZw6nOE9OTn7Y3d3dJ1Tu5eTk3CsoKEg4
; cODA+94/uY4ePfpJa2trtiD/NS8vz/X397vV1VUXCoWckHC1tbWusLBwOTU1NdTX19cjp98SUFtb26
; DIuSTEyo4dO/bp3yYoWV+4cCFOEA9YhoL6WWVlpVtbW3Ny5rTmGhsbnbJ9wb4FIbQmcc57dnb2gmwM
; JSQkfPXaBIVoyiw5Nzd3HpbX19ePXbt2baWnp4dg1rXmQEPrrq6ujgBcUlLS44GBge6ww6mWlpZhAu
; ro6BggoPT09AdaT4Kgu6LBxokTJ2KVTaWyXaSeHIbxZEhAMhJSram7k3EniP13Zbxx/fr1FUMAPhgC
; dIiQGiEglbPh9OnTn/+JoPv27XsvLS0tkYyJFoc8dWCIPuedgORsXnV2aj2nLF17e7vPAwXp5OwnCC
; hOzBoCFpCdJwnZ7MfXoUOHPvCdx8bGRqu2lRzkY71OCdIfjNEcglQYqa6ufgERBwcHfR7oG78MWneX
; L1/exGFJScmMumPOUMMmCMjpd9hkP7xeHRcXF+NBEtvEIYdldJyPgI81ICWI8vJy3/Ho6KjfkrQmwU
; BIBbilM4sKZgLiihv3CchQMZvskySzQwh2eubQnkw2Yz5PSMUhTblF+h7ocUoQs7Oz/kACCTkBjfnw
; HLhvDnmanXAZp/HBusg85wdAhGRrm6xhiFpaQEAppCCck2E/axCYmJhwvb29PheU1XOC5TxQwynOcr
; MetIlPgqIEUxwwtvLOGh/Y4fDsn7x79+5mYmKiPwEJYHp6ersMICNReoU+kJ0lhU2QIKCdNhX0uAe5
; MG4wcYBNoidqg5HvRM4t2hANEJt955SBALq6uvwyqBuewBnOYw+7nDeb1N8SxrYX6NEhIOJDCGfsDw
; Z08eJFpwnpaEVmAI7Hx8d9QmpQ+d2gEv0OzAQRtAmncIxN9q3NPRxZj7KBQ0apdYV1gAjz45kzZ9yp
; U6c2BPWW5oNfBsjITXcwmm/evElHPDSHNhkZSkxGa22bNR6bjFpzaIMIVKgRo1gH11RDd/z4cSB+oP
; enEJEZMDIy4ncCaAhW5JnBtGp6ELRp5SZJfDK+PZNRxq9t7lQ3HSbIdXXBMpNRv4ieipBOxv3MrRXR
; B7Wrk83f7Dw2DXIcsgYZ8Xnjxo1lb7exSUAQBQSC2QCrsv0ZZUQHECemIyQEEca0fp452VzCITaBnP
; N37tz5HkJamVnzrN5Bh3wYSYxMG0S4V2RNWcga5zaW6RDJL6V4TN3NIUmazSDqXhByejWSGBlR2RfE
; S8r6JbWn5jCfluSGmIxrAjh37tzLnQ4tCZI0xfSMkTwh3V+JEWty8gT2I8fATwC0JHwgezggaaYbnu
; 0UI0vSfBKEB8lu3769FBQjej6SGBkpNXofMQ0JQA78rOEEzukOKaMTUTeCvAlqg4kRQXjU+HXECIGB
; sGGxCYmIW+IK89//VURAqrm7evUqw2pT382Y+mHHmG/28QUa22JEhiZGPE04LGsb1+xjWMPnEVoA9L
; Qk9/nz551+km8pqKVIYsSaiRGJYXNbjKi/iREBRRIjQ8gkViVaU0dsoYYoZXx8/LqYHdpNjLiDNkly
; W4xwzL2bGJmAwGDOEHD4jwjknTTu2E849iOJETbZN05EFCNTqp1ihDEjpykeDiFUEO6g2OwUI/a4WW
; P/D8syZh+MgPBeAAAAAElFTkSuQmCC
; thumbnail end
;
"""
# Odstranění whitespace a nových řádků
base64_image = base64_image.replace("\n", "")
base64_image = base64_image.replace(";", "")
base64_image = base64_image.replace(" ", "")
base64_image = base64_image.replace("thumbnail end", "")

# Příklad použití
simage_size = 32
gimage_size = 32
gcode_string = generate_preview(base64_image, simage_size, gimage_size)
print(gcode_string)
