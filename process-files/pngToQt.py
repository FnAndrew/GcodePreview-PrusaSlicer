from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt

def load_png_as_qimage(png_file_path):
    # Load PNG file into QImage
    image = QImage(png_file_path)
    
    if image.isNull():
        raise ValueError("Failed to load image.")
    
    return image

# Example usage
qimage = load_png_as_qimage('wolf_big.png')
print(qimage.size())
