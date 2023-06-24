from pathlib import Path
from uuid import uuid4

from misc.constants import temp_dir, pdf_max_line_length


def get_temp_file_path(extension: str = None) -> Path:
    return Path(temp_dir, str(uuid4()) + (f".{extension}" if extension else ""))


def split_multiline_text(string: str) -> tuple[str, ...]:
    result = []

    while len(string) > pdf_max_line_length or "\n" in string:
        max_slice = string[:pdf_max_line_length + 1]  # +1 in case the space/newline is the next symbol
        index = max_slice.index("\n") if "\n" in max_slice else (
            max_slice.rindex(" ") if " " in max_slice else len(max_slice) - 1
        )
        result.append(string[:index])
        string = string[index + 1:]

    result.append(string)

    return tuple(result)
