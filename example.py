from image_tool import ImageTool, MergeImages, create_solid_color_image


def success_callback(msg: str) -> None:
    print(msg)


def failure_callback(msg: str) -> None:
    print(msg)


image_tool = ImageTool('assets/original.jpg', './assets', success_callback, failure_callback)

image_tool.convert_image('png', 'default')
image_tool.compress_image(70, True)
image_tool.resize_image(1920, 1080, True)
image_tool.crop_image((0, 0, 3840, 2160))
image_tool.flip_image('both')
image_tool.rotate_image(180, True)
image_tool.add_border_image(50, (255, 0, 0))
image_tool.blur_image("gaussian", 5)
image_tool.remove_bg()
image_tool.add_contrast_image(2.0)
image_tool.adjust_brightness(2.0)
image_tool.grayscale_image()
options = {
    'font_family': "assets/Poppins-Regular.ttf",
    'font_size': 380,
    'color': (0, 0, 0),
    'bg_color': (255, 165, 0),
    'shadow_color': None,
    'line_height': 1.2,
    'bold': False,
    'box_width': 3400,
    'box_height': 1000,
    'align': 'center',
    'radius': 50
}
image_tool.add_text_to_image('Dodge Challenger\nSRT Demon 170', (50, 50), **options)
image_tool.blur_area((0, 0, 3000, 3000), 50)
image_tool.pixelate_area((0, 0, 3000, 3000), 50)
image_tool.add_gaussian_noise(0, 50)
image_tool.replace_color((255, 255, 255), (255, 0, 0))

palette = image_tool.get_color_palette(15)
for color, percentage in palette:
    print(f"{color}, {percentage}%")
print(image_tool.get_image_info())
print(image_tool.get_exif_data())

cat_images = ["assets/cat1.jpg", "assets/cat2.jpg", "assets/cat3.jpg", "assets/cat4.jpg"]
merge_images = MergeImages(cat_images, './assets', (400, 400), success_callback, failure_callback)
merge_images.merge_horizontally()
merge_images.merge_vertically()

create_solid_color_image("assets/output.jpg", (400, 200), (255, 0, 0))
