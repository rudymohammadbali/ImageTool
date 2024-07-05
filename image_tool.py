from pathlib import Path

from PIL import Image, ImageFilter, ImageEnhance

from common_functions import UnsupportedFormatError, InvalidPercentageError, path_exists, is_file, \
    get_filename_extension


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
        raise UnsupportedFormatError(f"Unsupported image format: {target_format}")

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
        raise UnsupportedFormatError(f"Unsupported image format: {output_format}")

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
        raise UnsupportedFormatError(f"Unsupported image format: {output_format}")

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


def resize_image(input_path: str, output_path: str, width: int, height: int) -> bool:
    """
        Resizes an image to the specified dimensions.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to save the resized image.
            width (int): Target width in pixels.
            height (int): Target height in pixels.

        Returns:
            bool: True if the image was successfully resized and saved, False otherwise.
        Raises:
            FileExistsError: If the input file does not exist.
            NotADirectoryError: If the output folder does not exist.
        """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"resized_{filename}.{extension}"

    try:
        img = Image.open(input_path)

        resized_img = img.resize((width, height))
        resized_img.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error resize: {input_path}: {e}")
        return False


def crop_image(input_path: str, output_path: str, left: int, upper: int, right: int, lower: int):
    """
        Crops an image based on the specified coordinates.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to save the cropped image.
            left (int): X-coordinate of the left edge of the cropping rectangle.
            upper (int): Y-coordinate of the upper edge of the cropping rectangle.
            right (int): X-coordinate of the right edge of the cropping rectangle.
            lower (int): Y-coordinate of the lower edge of the cropping rectangle.

        Returns:
            bool: True if the image was successfully cropped and saved, False otherwise.
        Raises:
            FileExistsError: If the input file does not exist.
            NotADirectoryError: If the output folder does not exist.
        """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"cropped_{filename}.{extension}"

    try:
        img = Image.open(input_path)

        cropped_img = img.crop((left, upper, right, lower))

        cropped_img.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error cropping: {input_path}: {e}")
        return False


def flip_image(input_path: str, output_path: str, flip_horizontal: bool = False, flip_vertical: bool = False) -> bool:
    """
    Flips an image based on the specified options.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the modified image.
        flip_horizontal (bool, optional): Whether to flip horizontally (left to right). Default is False.
        flip_vertical (bool, optional): Whether to flip vertically (top to bottom). Default is False.

    Returns:
        bool: True if the image was successfully modified and saved, False otherwise.
    Raises:
        FileExistsError: If the input file does not exist.
        NotADirectoryError: If the output folder does not exist.
    """

    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"rotated_{filename}.{extension}"

    try:
        img = Image.open(input_path)

        if flip_horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

        img.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error flip: {input_path}: {e}")
        return False


def rotate_image(input_path: str, output_path: str, rotate_angle: int = 0, expand: bool = True) -> bool:
    """
        Rotates an image by the specified angle and saves the result.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to save the rotated image.
            rotate_angle (int, optional): Angle in degrees for rotation (default is 0).
            expand (bool, optional): Whether to expand the output image to fit rotated content (default is True).

        Returns:
            bool: True if the image was successfully rotated and saved, False otherwise.
        Raises:
            FileExistsError: If the input file does not exist.
            NotADirectoryError: If the output folder does not exist.
        """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"rotated_{filename}.{extension}"

    try:
        img = Image.open(input_path)
        if rotate_angle:
            img = img.rotate(rotate_angle, expand=expand)
            img.save(fp=output_name, format=extension)

        return True
    except Exception as e:
        print(f"Error rotate: {input_path}: {e}")
        return False


def add_border(input_path: str, output_path: str, border_size: int, border_color: str) -> bool:
    """
    Adds a border to an image.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the image with the added border.
        border_size (int): Width of the border in pixels.
        border_color (str): Border color (e.g., 'red', '#FF0000', etc.).

    Returns:
        bool: True if the image was successfully processed and saved, False otherwise.
    Raises:
        FileExistsError: If the input file does not exist.
        NotADirectoryError: If the output folder does not exist.
    """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"added_border_{filename}.{extension}"

    try:
        img = Image.open(input_path)

        background = Image.new("RGBA", (img.width + 2 * border_size, img.height + 2 * border_size), border_color)
        background.paste(img, (border_size, border_size))

        background.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error adding border {input_path}: {e}")
        return False


def blur_image(input_path: str, output_path: str, blur_radius: int) -> bool:
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"blured_{filename}.{extension}"

    try:
        img = Image.open(input_path)

        blurred_img = img.filter(ImageFilter.BoxBlur(blur_radius))

        blurred_img.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error add blur to {input_path}: {e}")
        return False


def remove_transparency_by_color(input_path: str, output_path: str, target_color: tuple = (0, 0, 0)) -> bool:
    """
    Removes transparency from an image by replacing a specific color with transparency.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the modified image.
        target_color (tuple): RGB value of the color to make transparent (default is black).

    Returns:
        bool: True if successful, False otherwise.
    """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"removed_transparency_{filename}.{extension}"

    try:
        img = Image.open(input_path)
        rgba_image = img.convert("RGBA")

        new_data = []
        for item in rgba_image.getdata():
            if item[0] == target_color[0] and item[1] == target_color[1] and item[2] == target_color[2]:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        rgba_image.putdata(new_data)
        rgba_image.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error to remove transparency from {input_path}: {e}")
        return False


def add_contrast(input_path: str, output_path: str, contrast: float = 1.2) -> bool:
    """
        Enhances the contrast of an image and saves the result.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to the output folder where the enhanced image will be saved.
            contrast (float, optional): Contrast factor (default is 1.2).

        Returns:
            bool: True if successful, False otherwise.
        """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"added_contrast_{filename}.{extension}"

    try:
        img = Image.open(input_path)
        contrast_enhancer = ImageEnhance.Contrast(img)

        contrast_factor = contrast
        output_image = contrast_enhancer.enhance(contrast_factor)

        output_image.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error add contrast {input_path}: {e}")
        return False


def grayscale_image(input_path: str, output_path: str) -> bool:
    """
        Converts a color image to grayscale and saves the result.

        Args:
            input_path (str): Path to the input image file.
            output_path (str): Path to the output folder where the grayscale image will be saved.

        Returns:
            bool: True if successful, False otherwise.
        """
    if not is_file(input_path):
        raise FileExistsError(f"File {input_path} does not exists.")

    if not path_exists(output_path):
        raise NotADirectoryError(f"Output folder {output_path} does not exist.")

    filename, extension = get_filename_extension(input_path)
    if extension[1:] == "jpg":
        extension = "jpeg"
    else:
        extension = extension[1:]
    output_name = Path(output_path) / f"grayscale_{filename}.{extension}"

    try:
        img = Image.open(input_path)
        image = img.convert("L")

        image.save(fp=output_name, format=extension)
        return True
    except Exception as e:
        print(f"Error grayscale {input_path}: {e}")
        return False
