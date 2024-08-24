from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import pymupdf # PyMuPDF
import io
import os


def extract_text_from_images(images):
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text


def extract_images_from_pdf(pdf_path, output_folder="extracted_images"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_file = pymupdf.open(pdf_path)
    image_list = []

    for page_index in range(len(pdf_file)):
        page = pdf_file.load_page(page_index)
        images = page.get_images(full=True)

        for image_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            try:
                image = Image.open(io.BytesIO(image_bytes))
                image_path = os.path.join(output_folder, f"image{page_index + 1}_{image_index + 1}.{image_ext}")
                image.save(image_path)
                image_list.append(image_path)
            except Image.UnidentifiedImageError:
                print(f"Skipping unsupported or corrupted image on page {page_index + 1}, image {image_index + 1}.")
            except Exception as e:
                print(f"Error processing image on page {page_index + 1}, image {image_index + 1}: {str(e)}")

    return image_list


def process_pdf(pdf_path):
    # Extract text from PDF pages
    images = convert_from_path(pdf_path)
    extracted_text = extract_text_from_images(images)

    # Extract images from the PDF
    extracted_images = extract_images_from_pdf(pdf_path)

    return extracted_text, extracted_images


if __name__ == "__main__":
    pdf_path = "/Users/airjlee/Documents/March-SAT.pdf"

    # Process the PDF to extract text and images
    text_content, image_paths = process_pdf(pdf_path)

    # Output the extracted text
    print("Extracted Text:\n", text_content)

    # Output the paths to extracted images
    print("\nExtracted Images:")
    for img_path in image_paths:
        print(img_path)
