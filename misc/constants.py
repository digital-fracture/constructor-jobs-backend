from pathlib import Path
from tempfile import gettempdir


pdf_max_line_length = 52

pdf_image_size = 560


temp_dir = Path(gettempdir(), "kruase")
if not temp_dir.exists():
    temp_dir.mkdir()

resources_dir = Path("resources")

weights_path = Path(resources_dir, "catboost_weights.cbm")
template_path = Path(resources_dir, "template.png")
default_image_path = Path(resources_dir, "default_image.jpg")
font_path = Path(resources_dir, "Hangyaboly.ttf")
mask_path = Path(resources_dir, "mask.png")
