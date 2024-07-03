# Image-Tool
Compress and convert images to various other image formats using Pillow library.


## Example
```python
from image_tool import convert_image, compress_image, merge_images_horizontally, merge_images_vertically

# Convert image
convert_image(input_path="image.jpg", output_path="D:\\Dev\\Python\\ConverterToolkit\\", target_format="png") # Convert image to other image formats: ["jpg","jpeg","png","gif","bmp","tiff","tif","webp","svg","ico"]

# Compress image
compress_image(input_path="image.jpg", output_path="D:\\Dev\\Python\\ConverterToolkit\\image_compressed.jpg", quality=50) # Compress images by quality: 0-100

# Merge images
image_list = ["image1.png", "image2.png", "image3.png"]
merge_images_horizontally(image_list, width=250, height=500, output_path="path/to/output/dir", output_format="jpeg")
merge_images_vertically(image_list, width=500, height=250, output_path="path/to/output/dir", output_format="jpeg")

# All function will return True if convert/compress/merge successfull otherwise False.
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
