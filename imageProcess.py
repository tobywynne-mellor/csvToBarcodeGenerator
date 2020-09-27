from pdf2image import convert_from_path, convert_from_bytes
import tempfile
from reportlab.lib.utils import ImageReader

# Generate a reportlab ready image
# meant for vector graphic files that need to be converted to bitmap at high resolution

class ImageProcessor:
    def __init__(self, width=400):
        self.width = width

    def process(self, filepath):
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(filepath, output_folder=path, size=(self.width, None))
            return ImageReader(images_from_path[0].convert())
