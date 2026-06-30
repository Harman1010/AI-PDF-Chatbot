import fitz
import numpy as np
import easyocr

MIN_TEXT_LENGTH = 250

reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def apply_ocr_if_needed(pdf_path, documents):

    pdf = fitz.open(pdf_path)

    for page_number, doc in enumerate(documents):

        text = doc.page_content.strip()

        if len(text) >= MIN_TEXT_LENGTH:
            continue

        print(f"OCR on page {page_number + 1}")

        page = pdf.load_page(page_number)

        pix = page.get_pixmap(dpi=300)

        image = np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)

        if pix.n == 4:
            image = image[:, :, :3]

        results = reader.readtext(image,detail=0)

        ocr_text = "\n".join(results)

        if ocr_text.strip():

            doc.page_content = ocr_text

    pdf.close()

    return documents