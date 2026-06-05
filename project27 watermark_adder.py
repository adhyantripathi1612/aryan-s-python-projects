from PIL import Image, ImageDraw, ImageFont

# 1. Get User Input
image_name = input('Enter image name (without extension): ').strip()
extension = input('Enter extension (e.g., .jpg, .png): ').strip()

# Ensure extension starts with a dot
if not extension.startswith('.'):
    extension = '.' + extension

watermark_text = input('Enter watermark text: ')

try:
    # 2. Process Image
    full_path = image_name + extension
    print(f"Opening {full_path}...")
    
    with Image.open(full_path).convert('RGBA') as original:
        # Load font
        font_size = 80
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except IOError:
            font = ImageFont.load_default()
            print("Note: 'arial.ttf' not found. Using default font.")

        # 3. Create Watermark Canvas
        # We need a dummy draw object to calculate the text size
        dummy_img = Image.new("RGBA", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        bbox = dummy_draw.textbbox((0, 0), watermark_text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Transparent canvas for watermark text
        watermark_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        # Translucent white (alpha=100)
        draw.text((0, 0), watermark_text, font=font, fill=(255, 255, 255, 100))

        # 4. Rotate Watermark (45 degrees)
        angle = 45
        # expand=True ensures the rotated text isn't clipped
        rotated_watermark = watermark_layer.rotate(angle, expand=True)

        # 5. Position and Paste (Centered)
        pos = (
            (original.width - rotated_watermark.width) // 2, 
            (original.height - rotated_watermark.height) // 2
        )
        
        # Paste the layer onto the original
        original.paste(rotated_watermark, pos, rotated_watermark)
        
        # 6. Save Output
        output_name = f"{image_name}_slanted_watermarked{extension}"
        # Convert back to RGB for JPEG compatibility (RGBA for PNG is also fine)
        if extension.lower() in ['.jpg', '.jpeg']:
            original.convert('RGB').save(output_name)
        else:
            original.save(output_name)
            
        print(f"Success! Slanted watermark added. Saved as: {output_name}")

except FileNotFoundError:
    print(f"Error: The file '{full_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
