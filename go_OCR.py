from pdf2image import convert_from_path
import pytesseract

pdf_path = "/mnt/c/ATS/GSResume.pdf"  # full WSL path
pages = convert_from_path(pdf_path, dpi=300)

for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)
    print(f"--- Page {i+1} ---")
    print(text)
