from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image

from misc.util import get_temp_file_path, split_multiline_text
from misc.constants import pdf_image_size, template_path, default_image_path, font_path, mask_path


registerFont(TTFont("Zelek Bold", font_path))

mask_image = Image.open(mask_path)


def process_image(path: Path) -> Path:
    image = Image.open(path)
    width, height = image.size

    scale = pdf_image_size / min(width, height)
    resized_image = image.resize((round(width * scale), round(height * scale)))
    width, height = resized_image.size

    cropped_image = resized_image.crop(
        (
            width // 2 - pdf_image_size // 2, height // 2 - pdf_image_size // 2,
            width // 2 + pdf_image_size // 2, height // 2 + pdf_image_size // 2
        )
    )

    output_image = Image.new("RGBA", (pdf_image_size, pdf_image_size), (0, 0, 0, 0))
    output_image.paste(cropped_image, mask=mask_image.getchannel("A"))

    output_image.save(output_path := get_temp_file_path("png"))

    return output_path


def generate_pdf(
        position: str,
        speciality: str,
        requirements: str,
        conditions: str,
        notes: str,
        phone: str,
        email: str,
        image_path: Path = default_image_path
) -> Path:
    c = canvas.Canvas(str(output_path := get_temp_file_path("pdf")), pagesize=(1500, 2100))

    c.drawImage(template_path, 0, 0)

    c.setFillColor((255, 255, 255))

    c.setFont("Zelek Bold", 60)
    c.drawCentredString(750, 1870, position)

    c.setFont("Zelek Bold", 80)
    c.drawCentredString(750, 1700, speciality)

    c.setFont("Zelek Bold", 24)

    text_object = c.beginText(171, 1140)
    text_object.textLines("\n".join(split_multiline_text(requirements)))
    c.drawText(text_object)

    text_object = c.beginText(820, 1140)
    text_object.textLines("\n".join(split_multiline_text(conditions)))
    c.drawText(text_object)

    text_object = c.beginText(171, 710)
    text_object.textLines("\n".join(split_multiline_text(notes)))
    c.drawText(text_object)

    text_object = c.beginText(171, 250)
    text_object.textLines("\n".join(filter(lambda field: field, (phone, email))))
    c.drawText(text_object)

    processed_image_path = process_image(image_path)
    c.drawImage(processed_image_path, 850, 150)

    c.showPage()
    c.save()

    return output_path
