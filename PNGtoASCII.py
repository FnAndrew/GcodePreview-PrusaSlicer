import base64
from PIL import Image
from io import BytesIO
import base64
from PIL import Image
from io import BytesIO

# Base64 string (výňatek)
base64_string = """
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
P/D8syZh+MgPBeAAAAAElFTkSuQmCC
"""

# Dekódování Base64 stringu do obrázku
image_data = base64.b64decode(base64_string)
image = Image.open(BytesIO(image_data))

# Alternativa - Načtení uloženého obrázku
# with open("image.png", "rb") as f:
#     image = Image.open(f)

# Převod na stupně šedi
gray_image = image.convert("L")

# Zmenšení obrázku pro ASCII Art
width, height = gray_image.size
aspect_ratio = height/float(width)
new_width = 100
new_height = int(aspect_ratio * new_width * 0.55)  # Vzhledem k rozměrům znaků
resized_gray_image = gray_image.resize((new_width, new_height))

# ASCII znaky podle jasu
ASCII_CHARS = "@%#*+=-:. "
# ASCII_CHARS = "bcd02456"

# Převod pixelů na ASCII znaky
def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join([ASCII_CHARS[pixel//32] for pixel in pixels])
    return ascii_str

ascii_str = pixel_to_ascii(resized_gray_image)

# Rozdělení ASCII stringu na více řádků podle šířky
ascii_str_len = len(ascii_str)
ascii_img = "\n".join([ascii_str[index:index + new_width] for index in range(0, ascii_str_len, new_width)])

# Zobrazení výsledného ASCII Artu
print(ascii_img)
