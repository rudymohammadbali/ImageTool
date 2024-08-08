import os
from collections import Counter
from pathlib import Path
from typing import Callable

import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ExifTags, ImageDraw, ImageFont
from rembg import remove


def create_solid_color_image(output_path: str, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    image = Image.new('RGB', size, color)
    image.save(fp=output_path)


class MergeImages:
    def __init__(self, image_paths: list[str], output_folder: str, box_size: tuple[int, int], on_success: Callable,
                 on_failure: Callable):
        self.images = image_paths
        self.output_folder = output_folder
        self.box_size = box_size
        self.on_success = on_success
        self.on_failure = on_failure

    def merge_horizontally(self) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / 'images_merged_horizontally.jpg')
        try:
            images = [Image.open(path).resize(size=self.box_size, resample=Image.LANCZOS) for path in self.images]
            total_width = self.box_size[0] * len(images)

            merged_image = Image.new('RGB', (total_width, self.box_size[1]))

            x_offset = 0
            for img in images:
                merged_image.paste(img, (x_offset, 0))
                x_offset += self.box_size[0]

            merged_image.save(fp=file_path, format='JPEG')

            self.on_success(f'Images merged in horizontally, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while merging images:\n{e}')

    def merge_vertically(self) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / 'images_merged_vertically.jpg')
        try:
            images = [Image.open(path).resize(size=self.box_size, resample=Image.LANCZOS) for path in self.images]
            total_height = self.box_size[1] * len(images)

            merged_image = Image.new('RGB', (self.box_size[0], total_height))

            y_offset = 0
            for img in images:
                merged_image.paste(img, (0, y_offset))
                y_offset += self.box_size[1]

            merged_image.save(fp=file_path, format='JPEG')

            self.on_success(f'Images merged vertically, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while merging images:\n{e}')


class ImageTool:
    def __init__(self, image_path: str, output_folder: str, on_success: Callable, on_failure: Callable):
        self.image = image_path
        self.output_folder = output_folder
        self.on_success = on_success
        self.on_failure = on_failure

        self.filename, self.extension = self.get_filename_extension(image_path)

    def convert_image(self, output_format: str, save_method: str = 'default', **kwargs) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_converted.{output_format}')
        try:
            image = Image.open(self.image)

            if image.mode != 'RGB':
                image = image.convert('RGB')

            if output_format.upper() == 'ICO':
                image.save(fp=file_path, format=output_format.upper(), sizes=[(32, 32), (64, 64), (128, 128)], **kwargs)
            else:
                if save_method == 'default':
                    image.save(fp=file_path, format=output_format.upper(), **kwargs)
                elif save_method == 'optimize':
                    image.save(fp=file_path, format=output_format.upper(), optimize=True, **kwargs)
                elif save_method == 'progressive':
                    image.save(fp=file_path, format=output_format.upper(), progressive=True, **kwargs)
                else:
                    self.on_failure(
                        f"Invalid save method ({save_method}). Choose 'default', 'optimize', or 'progressive'.")
                    return

            self.on_success(f'Converted from {self.extension} to {output_format}, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while converting image: {self.image}:\n{e}')

    def compress_image(self, quality: int = 85, optimize: bool = True) -> None:
        file_path = os.path.abspath(
            Path() / self.output_folder / f'{self.filename}_compressed.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            image.save(fp=file_path, quality=quality, optimize=optimize)

            before = round(os.path.getsize(self.image) / 1_000_000, 1)
            after = round(os.path.getsize(file_path) / 1_000_000, 1)

            self.on_success(f'Image size reduced from {before}MB to {after}MB, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while compressing image: {self.image}:\n{e}')

    def resize_image(self, width: int = None, height: int = None, keep_aspect_ratio: bool = True) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_resized.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            original_width, original_height = image.size

            if keep_aspect_ratio:
                if width and height:
                    aspect_ratio = min(width / original_width, height / original_height)
                    new_width = int(original_width * aspect_ratio)
                    new_height = int(original_height * aspect_ratio)
                elif width:
                    aspect_ratio = width / original_width
                    new_width = width
                    new_height = int(original_height * aspect_ratio)
                elif height:
                    aspect_ratio = height / original_height
                    new_width = int(original_width * aspect_ratio)
                    new_height = height
                else:
                    new_width, new_height = original_width, original_height
            else:
                new_width = width if width else original_width
                new_height = height if height else original_height

            resized_img = image.resize((new_width, new_height))
            resized_img.save(fp=file_path)

            self.on_success(f'Image resized to {new_width}, {new_height}, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while resizing image: {self.image}:\n{e}')

    def crop_image(self, crop_box: tuple[float, float, float, float]) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_cropped.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            cropped_image = image.crop(crop_box)
            cropped_image.save(fp=file_path)

            self.on_success(f'Image cropped to {crop_box}, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while cropping image: {self.image}:\n{e}')

    def flip_image(self, flip_direction: str = 'both') -> None:
        file_path = os.path.abspath(
            Path() / self.output_folder / f'{self.filename}_flipped_{flip_direction}.{self.extension.lower()}')
        try:
            image = Image.open(self.image)

            if flip_direction == 'horizontal':
                flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif flip_direction == 'vertical':
                flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            elif flip_direction == 'both':
                flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
            else:
                self.on_failure("Invalid flip direction. Choose 'horizontal', 'vertical', or 'both'.")
                return

            flipped_image.save(fp=file_path)

            self.on_success(f'Image flipped to {flip_direction}, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while flipping image: {self.image}:\n{e}')

    def rotate_image(self, angle: int, expand: bool = True) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_rotated.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            rotated_image = image.rotate(angle=angle, expand=expand)
            rotated_image.save(fp=file_path)

            self.on_success(f'Image rotated by {angle}, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while rotating image: {self.image}:\n{e}')

    def add_border_image(self, border_width: int, border_color: tuple[int, int, int]) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_border.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            image_with_border = ImageOps.expand(image, border=border_width, fill=border_color)
            image_with_border.save(fp=file_path)

            self.on_success(f'Added border to image, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while adding border to image: {self.image}:\n{e}')

    def blur_image(self, blur_type: str = 'gaussian', radius: int = 5) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_blured.{self.extension.lower()}')
        try:
            image = Image.open(self.image)

            if blur_type == 'gaussian':
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
            elif blur_type == 'box':
                blurred_image = image.filter(ImageFilter.BoxBlur(radius))
            elif blur_type == 'simple':
                blurred_image = image.filter(ImageFilter.BLUR)
            else:
                self.on_failure("Invalid blur type. Choose 'gaussian', 'box', or 'simple'.")
                return

            blurred_image.save(fp=file_path)

            self.on_success(f'Blur type {blur_type} added to image, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while adding blur to image: {self.image}:\n{e}')

    def remove_bg(self, alpha_matting: bool = False,
                  alpha_matting_foreground_threshold: int = 240,
                  alpha_matting_background_threshold: int = 10, alpha_matting_erode_size: int = 10,
                  only_mask: bool = False,
                  post_process_mask: bool = False, bg_color: tuple[int, int, int, int] = None) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_transparent.png')
        try:
            image = Image.open(self.image)
            new_image = remove(
                data=image,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
                alpha_matting_erode_size=alpha_matting_erode_size,
                only_mask=only_mask,
                post_process_mask=post_process_mask,
                bgcolor=bg_color
            )
            new_image.save(fp=file_path, format='PNG')

            self.on_success(f'Background removed from image, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while removing image background: {self.image}:\n{e}')

    def add_contrast_image(self, contrast_factor: float = 1.0) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_contrast.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            enhancer = ImageEnhance.Contrast(image)
            image_enhanced = enhancer.enhance(contrast_factor)
            image_enhanced.save(fp=file_path)

            self.on_success(f'Contrast added to image by {contrast_factor} factor, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while adding contrast to the image: {self.image}:\n{e}')

    def adjust_brightness(self, brightness_factor: float = 1.0) -> None:
        file_path = os.path.abspath(
            Path() / self.output_folder / f'{self.filename}_brightness.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            enhancer = ImageEnhance.Brightness(image)
            enhanced_image = enhancer.enhance(brightness_factor)

            enhanced_image.save(fp=file_path)

            self.on_success(f"Brightness adjusted by a factor of {brightness_factor}, saved as:\n{file_path}.")
        except Exception as e:
            self.on_failure(f"Error wile adjusting image brightness:\n{e}")

    def grayscale_image(self) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_grayscale.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            new_image = image.convert('L')
            new_image.save(fp=file_path)

            self.on_success(f'Image converted to grayscale, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while converting image to grayscale: {self.image}:\n{e}')

    def add_text_to_image(self, text: str, position: tuple[int, int], **kwargs) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_text.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            draw = ImageDraw.Draw(image)

            font_family = kwargs.get('font_family', None)
            font_size = kwargs.get('font_size', 36)
            color = kwargs.get('color', (255, 255, 255))
            bg_color = kwargs.get('bg_color', None)
            shadow_color = kwargs.get('shadow_color', None)
            line_height = kwargs.get('line_height', 1.2)
            bold = kwargs.get('bold', False)
            box_width = kwargs.get('box_width', None)
            box_height = kwargs.get('box_height', None)
            align = kwargs.get('align', 'left')
            radius = kwargs.get('radius', 0)

            try:
                font = ImageFont.truetype(font_family, font_size) if font_family else ImageFont.load_default(font_size)
            except IOError:
                font = ImageFont.load_default(font_size)

            stroke_width = 6 if bold else 0

            lines = text.split('\n')
            max_line_width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
            total_height = int(len(lines) * font_size * line_height)

            if box_width:
                max_line_width = box_width
            if box_height:
                total_height = box_height

            if bg_color:
                x0, y0 = position
                x1, y1 = x0 + max_line_width, y0 + total_height
                draw.rounded_rectangle([x0, y0, x1, y1], radius, fill=bg_color)

            y = position[1]
            for line in lines:
                if align == 'center':
                    x = position[0] + (max_line_width - draw.textbbox((0, 0), line, font=font)[2]) // 2
                elif align == 'right':
                    x = position[0] + max_line_width - draw.textbbox((0, 0), line, font=font)[2]
                else:
                    x = position[0]

                if shadow_color:
                    draw.text((x + 2, y + 2), line, font=font, fill=shadow_color, stroke_width=stroke_width)

                draw.text((x, y), line, font=font, fill=color, stroke_width=stroke_width)

                y += int(font_size * line_height)

            image.save(file_path)
            self.on_success(f'Text added to image, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while adding text to image: {self.image}:\n{e}')

    def blur_area(self, position: tuple[int, int, int, int], blur: float = 50) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_blur_area.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            cropped_image = image.crop(position)
            blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(blur))
            image.paste(blurred_image, position)
            image.save(file_path)
            self.on_success(f'Blur added to selected area, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while adding blur to selected area: {self.image}:\n{e}')

    def pixelate_area(self, position: tuple[int, int, int, int], pixel_size: int = 50) -> None:
        file_path = os.path.abspath(
            Path() / self.output_folder / f'{self.filename}_pixelate_area.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            cropped_image = image.crop(position)
            small = cropped_image.resize(
                (cropped_image.size[0] // pixel_size, cropped_image.size[1] // pixel_size),
                resample=Image.NEAREST
            )
            result = small.resize(cropped_image.size, Image.NEAREST)
            image.paste(result, position)
            image.save(file_path)
            self.on_success(f'Selected area pixelated, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while pixelating selected area: {self.image}:\n{e}')

    def add_gaussian_noise(self, mean: int = 0, std: int = 50) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_noisy.{self.extension.lower()}')
        try:
            image = Image.open(self.image)
            image_array = np.array(image)

            noise = np.random.normal(mean, std, image_array.shape)
            noisy_image = image_array + noise

            noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
            noisy_image_pil = Image.fromarray(noisy_image)
            noisy_image_pil.save(file_path)
            self.on_success(f'Noise added to image, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while adding noise to image: {self.image}:\n{e}')

    def replace_color(self, target_color: tuple[int, int, int], replacement_color: tuple[int, int, int]) -> None:
        file_path = os.path.abspath(Path() / self.output_folder / f'{self.filename}_color_replacement.png')
        try:
            img = Image.open(self.image)
            img = img.convert("RGBA")
            data = img.getdata()

            new_data = []
            for item in data:
                if item[:3] == target_color:
                    new_data.append((*replacement_color, item[3]))
                else:
                    new_data.append(item)

            img.putdata(new_data)
            img.save(fp=file_path, format='PNG')
            self.on_success(f'Color replaced with new color, saved as:\n{file_path}')
        except Exception as e:
            self.on_failure(f'Error while replacing color with new color: {self.image}:\n{e}')

    def get_color_palette(self, palette_size: int = 15) -> list:
        try:
            image = Image.open(self.image)
            # image = image.resize((image.width // 2, image.height // 2))
            image = image.convert('RGB')

            pixels = list(image.getdata())
            total_pixels = len(pixels)

            color_counts = Counter(pixels)
            most_common_colors = color_counts.most_common(palette_size)

            color_palette = [(f"rgb{color}", round(count / total_pixels * 100, 2)) for color, count in
                             most_common_colors]

            return color_palette
        except Exception as e:
            self.on_failure(f'Error while getting color palette: {self.image}:\n{e}')

    def get_image_info(self) -> dict:
        image = Image.open(self.image)
        return {'format': image.format, 'size': image.size, 'mode': image.mode}

    def get_exif_data(self) -> dict:
        image = Image.open(self.image)
        exif_data = image._getexif()

        if exif_data:
            exif = {}
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                exif[tag_name] = value

            return exif

    @staticmethod
    def get_filename_extension(file_path: str) -> tuple[str, str]:
        filename, extension = os.path.splitext(os.path.basename(file_path))
        return filename, extension[1:].upper()
