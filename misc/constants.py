from pathlib import Path
from tempfile import gettempdir


pdf_max_line_length = 36

pdf_image_size = 560


temp_dir = Path(gettempdir(), "kruase")
if not temp_dir.exists():
    temp_dir.mkdir()

template_path = Path("resources", "template.png")
default_image_path = Path("resources", "default_image.jpg")
font_path = Path("resources", "Hangyaboly.ttf")
mask_path = Path("resources", "mask.png")
