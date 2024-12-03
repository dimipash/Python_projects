from PIL import Image, ImageDraw, ImageFont
import os


def add_text_watermark_to_folder(input, output, watermark_text, position, font_size=30):
    if not os.path.exists(output):
        os.makedirs(output)

    for filename in os.listdir(input):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            image_path = os.path.join(input, filename)
            original = Image.open(image_path)
            width, height = original.size
            print(f"Image width: {width}")
            print(f"Image height: {height}")

            draw = ImageDraw.Draw(original)
            font = ImageFont.truetype("super_nought.ttf", size=font_size)

            text_width = font.getmask(watermark_text).getbbox()[2]
            text_height = font.getmask(watermark_text).getbbox()[3]
            print(f"text width: {text_width}")
            print(f"text height: {text_height}")

            margin = 100
            a = width - text_width - margin
            b = height - text_height - margin

            draw.text((a, b), text=watermark_text, fill="white", font=font)

            output_path = os.path.join(output, f"Watermarked {filename}")

            original.save(output_path)

            print(f"Watermarked image saved to {output_path}")


input_directory = "./input"
output_directory = "./output"
watermark = "Karandila"

add_text_watermark_to_folder(
    input=input_directory,
    output=output_directory,
    watermark_text=watermark,
    font_size=200,
    position=(50, 50),
)
