import fitz
import os


# -----------------------------------------------------
# Convert PDF pages into images
# -----------------------------------------------------
def convert_pdf_to_images(pdf_path):

    pdf_document = fitz.open(pdf_path)

    image_paths = []


    # Process each page
    for page_number in range(len(pdf_document)):

        page = pdf_document.load_page(page_number)

        pix = page.get_pixmap()


        output_path = (
            f"processed/page_{page_number}.png"
        )

        pix.save(output_path)

        image_paths.append(output_path)


    return image_paths