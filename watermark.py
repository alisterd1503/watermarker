from PIL import Image, ExifTags
import os

def get_image_orientation(image_path):
    with Image.open(image_path) as img:
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(img._getexif().items())

            if orientation in exif:
                if exif[orientation] == 3:
                    return 180
                elif exif[orientation] == 6:
                    return 270
                elif exif[orientation] == 8:
                    return 90
        except (AttributeError, KeyError, IndexError):
            pass
        
    return 0

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size

def watermark(input_image_path, output_image_path, watermark_image_path, position):

    orientation = get_image_orientation(input_image_path)

    with Image.open(input_image_path) as base_image:
        base_image = base_image.rotate(orientation, expand=True)

        with Image.open(watermark_image_path) as watermark:
            watermark = watermark.convert("RGBA")
            width, height = base_image.size

            # Check if watermark dimensions match input image dimensions
            watermark_width, watermark_height = watermark.size
            input_dimensions = (width, height)
            watermark_dimensions = (watermark_width, watermark_height)
            if input_dimensions != watermark_dimensions:
                print("Warning: Watermark image dimensions do not match input image dimensions. Watermark may not appear correctly.")

            output = Image.new('RGBA', (width, height), (0,0,0,0))
            output.paste(base_image, (0,0))
            output.paste(watermark, position, mask=watermark)
            out = output.convert('RGB')
            out.save(output_image_path)

if __name__ == '__main__':
    input_directory = "input"
    output_directory = "output"
    watermark_image_directory = "logos"

    watermark_image_files = [f for f in os.listdir(watermark_image_directory) if f.endswith(('.png', '.PNG', '.jpg', '.jpeg', '.JPG', '.JPEG'))]
    if len(watermark_image_files) != 1:
        raise ValueError("There should be exactly one image file in the logos folder.")
    watermark_image_path = os.path.join(watermark_image_directory, watermark_image_files[0])

    count = 1
    for filename in os.listdir(input_directory):
        if filename.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
            input_image_path = os.path.join(input_directory, filename)
            output_image_path = os.path.join(output_directory, filename)
            watermark(input_image_path, output_image_path, watermark_image_path, (0,0))
            print(f"{count}: {filename} watermarked!")
            count += 1
            
# Usage: python3 watermark.py
