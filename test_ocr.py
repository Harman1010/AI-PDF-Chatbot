# test_ocr.py

import fitz
import numpy as np
import easyocr

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

pdf = fitz.open("UNIT 4 (3).pdf")

# OCR page 3 (0-based index)
page = pdf.load_page(2)

pix = page.get_pixmap(dpi=300)

image = np.frombuffer(
    pix.samples,
    dtype=np.uint8
).reshape(
    pix.height,
    pix.width,
    pix.n
)

# Convert RGBA -> RGB if needed
if pix.n == 4:
    image = image[:, :, :3]

result = reader.readtext(
    image,
    detail=0
)

print(result)