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


def merge_images_horizontally(images: list, width: int, height: int, output_path: str, output_format: str) -> bool:
    """
       Merges a list of images horizontally into a single image.

       Args:
           images (list): List of image file paths.
           width (int): Desired width for each image.
           height (int): Desired height for each image.
           output_path (str): Path to the output folder where the merged image will be saved.
           output_format (str): Desired output image format (e.g., "jpeg", "png", "gif").

       Raises:
           NotADirectoryError: If the output folder does not exist.
           UnsupportedImageFormatError: If the specified output format is not supported.

       Returns:
           bool: True if the merge was successful, False otherwise.
       """
    total_width = 0
    max_height = 0
    valid_images = []
    image_formats = [
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tiff",
        "webp",
        "ico"
    ]

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exists.")

    if output_format.lower() not in image_formats:
        raise UnsupportedImageFormatError(output_format)

    try:
        for img_path in images:
            if not is_file(img_path):
                print(f"Image {img_path} does not exists!")
            else:
                img = Image.open(img_path).resize(size=(width, height))
                valid_images.append(img)
                total_width += width
                max_height = max(max_height, height)

        merge_image = Image.new("RGB", (total_width, max_height), "white")
        x_offset = 0

        for img in valid_images:
            merge_image.paste(img, (x_offset, 0))
            x_offset += img.width

        merge_image.save(f"{output_path}\\merged_images_horizontally.{output_format}", format=output_format)
        return True
    except Exception as e:
        print(f"Error merging {valid_images}: {e}")
        return False


def merge_images_vertically(images: list, width: int, height: int, output_path: str, output_format: str) -> bool:
    """
    Merges a list of images vertically into a single image.

    Args:
        images (list): List of image file paths.
        width (int): Desired width for each image.
        height (int): Desired height for each image.
        output_path (str): Path to the output folder where the merged image will be saved.
        output_format (str): Desired output image format (e.g., "jpeg", "png", "gif").

    Raises:
        NotADirectoryError: If the output folder does not exist.
        UnsupportedImageFormatError: If the specified output format is not supported.

    Returns:
        None: The vertically merged image is saved to the specified output path.
    """
    total_height = 0
    max_width = 0
    valid_images = []
    image_formats = [
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tiff",
        "webp",
        "ico"
    ]

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    if output_format.lower() not in image_formats:
        raise UnsupportedImageFormatError(output_format)

    try:
        for img_path in images:
            if not is_file(img_path):
                print(f"Image {img_path} does not exist!")
            else:
                img = Image.open(img_path).resize(size=(width, height))
                valid_images.append(img)
                total_height += height
                max_width = max(max_width, width)

        merge_image = Image.new("RGB", (max_width, total_height), "white")
        y_offset = 0

        for img in valid_images:
            merge_image.paste(img, (0, y_offset))
            y_offset += img.height

        merge_image.save(f"{output_path}\\merged_images_vertically.{output_format}", format=output_format)
        return True
    except Exception as e:
        print(f"Error merging {valid_images}: {e}")
        return False
