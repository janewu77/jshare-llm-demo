from pdf2image import convert_from_path
import pytesseract


def ocr_pdf_to_text(file_path):
    # Convert the PDF to images
    images = convert_from_path(file_path)
    text = ""
    # Perform OCR on each image
    for i, image in enumerate(images, start=1):
        text += pytesseract.image_to_string(image, lang='chi_sim')  # Using Simplified Chinese for OCR
    return text


# Replace 'path_to_your_file.pdf' with the actual path to your PDF file
file_path = 'a.pdf'
ocr_text = ocr_pdf_to_text(file_path)
print(ocr_text)