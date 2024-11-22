import fitz  # PyMuPDF
import os
from io import BytesIO

def pdf_to_images(pdf_path, output_folder='pdf_images'):
    """Converts PDF to a list of image paths using PyMuPDF."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_document = fitz.open(pdf_path)
    image_paths = []

    # Loop through each page and save it as an image
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)  # High resolution for OCR

        # Save the image as PNG
        image_path = os.path.join(output_folder, f"sample_pdf_images/page_{page_num + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    pdf_document.close()
    return image_paths

def extract_text_from_pdf(pdf_path):
    """Extracts text from all pages of a PDF using OCR."""
    image_paths = pdf_to_images(pdf_path)

pdf_path = "data/sample_soap_note.pdf"
extract_text_from_pdf(pdf_path)
