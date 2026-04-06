from PIL import Image
import sys
import os

def process_for_ig(input_path, output_path, target_width=1080, target_height=1350):
    """Resizes and crops an image to fit IG 4:5 ratio exactly."""
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    img_width, img_height = img.size
    target_ratio = target_width / target_height
    img_ratio = img_width / img_height
    
    if img_ratio > target_ratio:
        new_width = int(img_height * target_ratio)
        left = (img_width - new_width) / 2
        img = img.crop((left, 0, left + new_width, img_height))
    else:
        new_height = int(img_width / target_ratio)
        top = (img_height - new_height) / 2
        img = img.crop((0, top, img_width, top + new_height))
        
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    img.save(output_path, "JPEG", quality=95)
    print(f"Processed: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process_image.py <input> <output>")
    else:
        process_for_ig(sys.argv[1], sys.argv[2])
