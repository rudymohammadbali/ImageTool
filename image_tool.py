import os

from PIL import Image


class UnsupportedImageFormatError(Exception):
    def __init__(self, format_name: str):
        super().__init__(f"Unsupported image format: {format_name}")


class InvalidPercentageError(Exception):
    def __init__(self, percentage: int):
        super().__init__(f"Invalid compression percentage: {percentage}. Please enter a value between 0 and 100.")


def path_exists(path: str) -> bool:
    return os.path.exists(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def is_valid_compression_percentage(compression_percentage: int) -> bool:
    return 0 <= compression_percentage <= 100


def convert_image(input_path: str, output_path: str, target_format: str) -> bool:
    """
    Converts an image from the input path to the specified target format.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the converted image will be saved.
        target_format (str): The desired output image format (e.g., 'JPEG', 'PNG', 'GIF', etc.).
    returns:
        (bool), True if conversion successful, else false
    """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exists.")

    image_formats = [
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tiff",
        "tif",
        "webp",
        "svg",
        "ico"
    ]

    if target_format.lower() not in image_formats:
        raise UnsupportedImageFormatError(target_format)

    try:
        output_path = f"{output_path}\\converted_image.{target_format}"
        image = Image.open(input_path)
        image.convert('RGB').save(output_path, format=target_format)
        print(f"Converted {input_path} to {target_format} format.")
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False


def compress_image(input_path: str, output_path: str, quality: int) -> bool:
    """
    Compresses an image by a specified percentage.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the compressed image will be saved.
        quality (int): Compression percentage (0 to 100).
    returns:
        (bool), True if conversion successful, else false
    """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not is_valid_compression_percentage(quality):
        raise InvalidPercentageError(quality)

    try:
        image = Image.open(input_path)
        image.save(output_path, optimize=True, quality=quality)
        print(f"Compressed {input_path} to {quality}% quality.")
        return True
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return False
