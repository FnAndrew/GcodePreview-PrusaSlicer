from PIL import Image

# Funkce pro převod obrázku na ASCII art
def image_to_ascii(image_path, output_width=200):
    image = Image.open(image_path)
    image = image.convert('L')  # Převod na odstíny šedi
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(output_width * aspect_ratio)
    image = image.resize((output_width, new_height))
    
    pixels = image.getdata()
    ascii_chars = '@%#*+=-:. '  # Můžete upravit znaky podle požadované úrovně detailu
    ascii_image = ''.join([ascii_chars[pixel // 32] for pixel in pixels])
    
    return '\n'.join([ascii_image[i:i + output_width] for i in range(0, len(ascii_image), output_width)])

def image_to_ascii2(image_, output_width=200):
    image = image_.convert('L')  # Převod na odstíny šedi
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(output_width * aspect_ratio)
    image = image.resize((output_width, new_height))
    
    pixels = image.getdata()
    ascii_chars = '@%#*+=-:. '  # Můžete upravit znaky podle požadované úrovně detailu
    ascii_image = ''.join([ascii_chars[pixel // 32] for pixel in pixels])
    
    return '\n'.join([ascii_image[i:i + output_width] for i in range(0, len(ascii_image), output_width)])


# Uložení ASCII art do souboru
def save_ascii_image(ascii_art, file_path):
    with open(file_path, 'w') as f:
        f.write(ascii_art)


# Načtení obrázku
import base64
from io import BytesIO

base64_image = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACcklEQVR4Ae2VSUtycRTG/7sGGqQoaH
cboIIogxa1KaGBqI2LVkEk0SKIwqJxUVYqojjjhFPOE4qICweEXLhwpR/Bj+BHeN57LrzQB1DhffEH
F+79b84953me82esT58+ffr8D8zPz4v39/dlb29v2YmJCY71ktnZWXGtVkMul4PVasXc3JyU9Yrl5W
VJKpVCPp+HVquFQqHAwcGBnPUCGns4HG6FQiFoNBqhe51Oh8PDw2/WK3i9xXq9Hk6nEy6XC5+fn8L7
0NCQiPWC6+trUyaTQTKZRCKRgMPhgNfrxfj4OMe6xe7uruzi4kIRCASapVIJsVgMHo8HSqUSX19fsF
gsWFhY6I4RV1ZWJGS4YrEI6rxcLiMSicDn88FsNsNms+H19RU7Ozsm1mn4eImpOMWNOifz0djpsdvt
MBgMwvhfXl5weXnZGhgY6KwP+BFn0+k0qtUqCoUC3G630DUVpUelUuHh4QF3d3e4ublps07Dx0seDA
aF4jR6ih1pbjKZhO7JgLQHnp6eOi/B8PCwiMZfr9cRj8cF/Y1GI97f34UFRBGk98fHR1xdXWF0dJRj
nWRxcVEwX6PRQKVSQTQaFTomvW9vb8GnAufn5zg7O8Pm5mbnF5FIJOL4hdOmwiSBWq3G/f29UJh+QC
aT4fj4+Of5+RljY2Mc6wbr6+ty3lwt3uHY2toyTU5OSuj86OjoRyqVttbW1qQfHx/tkZGR7m3Bk5MT
OS9F+3fE+Mvne29vLzs4OCjy+/1N/n5osm6xuroqIR9sbGxI/p5tb2/L+Ui2ZmZmOOp+enqaY91kaW
lJ/Pt7amqKo7V8enqqYH3+Rf4AHyxYfh4D6GwAAAAASUVORK5CYII=
"""

image_data = base64.b64decode(base64_image)
image = Image.open(BytesIO(image_data))


# Použití funkcí
ascii_art = image_to_ascii('wolf_big.png')
#ascii_art = image_to_ascii2(image)
save_ascii_image(ascii_art, 'ascii_art.txt')
