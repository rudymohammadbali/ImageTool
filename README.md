# Image-Tool
Compress and convert images to various other image formats using Pillow library.


## Example
```python
from image_tool import convert_image, compress_image, merge_images_horizontally, merge_images_vertically, resize_image, \
    crop_image, flip_image, rotate_image, add_border, blur_image, remove_transparency_by_color, add_contrast, grayscale_image

# Convert image
# ["jpg","jpeg","png","gif","bmp","tiff","tif","webp","svg","ico"]
convert_image(input_path="path/to/input", output_path="path/to/output/dir", target_format="png")

# Compress image
# quality: 0-100
compress_image(input_path="path/to/input", output_path="path/to/output/dir", quality=50)

# Merge images
image_list = ["image1.png", "image2.png", "image3.png"]
merge_images_horizontally(image_list, width=250, height=500, output_path="path/to/output/dir", output_format="jpeg")
merge_images_vertically(image_list, width=500, height=250, output_path="path/to/output/dir", output_format="jpeg")

# Resize image
resize_image(input_path="path/to/input", output_path="path/to/output/dir", width=200, height=200)

# Crop image
crop_image(input_path="path/to/input", output_path="path/to/output/dir", left=0, upper=0, right=500, lower=500)

# Flip image
flip_image(input_path="path/to/input", output_path="path/to/output/dir", flip_horizontal=True, flip_vertical=False)

# Rotate image
rotate_image(input_path="path/to/input", output_path="path/to/output/dir", rotate_angle=90, expand=True)

# Add border
add_border(input_path="path/to/input", output_path="path/to/output/dir", border_size=10, border_color="white")

# Blur image
blur_image(input_path="path/to/input", output_path="path/to/output/dir", blur_radius=10)

# Remove a color from image
remove_transparency_by_color(input_path="path/to/input", output_path="path/to/output/dir", target_color=(0, 0, 0))

# Add contrast to image
add_contrast(input_path="path/to/input", output_path="path/to/output/dir", contrast=5.5)

# Add grayscale effect to image
grayscale_image(input_path="path/to/input", output_path="path/to/output/dir")

# All function will return True if task successfully otherwise False.
```

Make sure to install pillow version: 10.3.0
```
pip install pillow==10.3.0
```

###

<h2 align="left">Support</h2>

###

<p align="left">If you'd like to support my ongoing efforts in sharing fantastic open-source projects, you can contribute by making a donation via PayPal.</p>

###

<div align="center">
  <a href="https://www.paypal.com/paypalme/iamironman0" target="_blank">
    <img src="https://img.shields.io/static/v1?message=PayPal&logo=paypal&label=&color=00457C&logoColor=white&labelColor=&style=flat" height="40" alt="paypal logo"  />
  </a>
</div>

###
