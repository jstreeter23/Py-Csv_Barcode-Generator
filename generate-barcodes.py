import os
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import re
import textwrap

# Create the folder if it doesn't exist
output_folder = 'barcodes'
os.makedirs(output_folder, exist_ok=True)

# Load CSV
try:
    df = pd.read_csv('ProductNames_SKUS.csv')  # Use the exact file name
    print("CSV loaded successfully!")
except FileNotFoundError:
    print("CSV file not found. Check the file path.")
    exit()

# Load fonts (Adjust the path if necessary)
try:
    bold_font_path = "arialbd.ttf"  # Bold font
    regular_font_path = "arial.ttf"  # Regular font
    title_font = ImageFont.truetype(bold_font_path, 24)  # Product Name in bold and larger size
    sku_font = ImageFont.truetype(regular_font_path, 18)  # SKU in regular font and slightly smaller size
except IOError:
    print("Font file not found. Make sure valid font file paths are specified.")
    exit()

# Set a fixed size for barcode images
barcode_width = 400  # Set a fixed width
barcode_height = 150  # Set a fixed height
max_text_width = 380  # Maximum width for wrapping text (slightly smaller than barcode width for padding)

for _, row in df.iterrows():
    # Retrieve product name and SKU, and sanitize product name for file name
    product_name = str(row['Product Name']).strip()  # Adjust to your exact column name
    sku = row['SKU']

    # Use product name as SKU if SKU is missing
    if pd.isna(sku) or sku == '':
        print(f"SKU missing for {product_name}. Using product name as SKU.")
        sku = product_name
    sku = str(sku)  # Ensure SKU is a string

    # Sanitize product name for the file name
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', product_name)  # Replace invalid filename characters with underscores

    # Generate Barcode
    barcode = Code128(sku, writer=ImageWriter())
    barcode_img = barcode.render()

    # Resize barcode to fixed dimensions
    resized_barcode_img = barcode_img.resize((barcode_width, barcode_height))

    # Wrap product name text to fit within the max_text_width
    wrapped_product_name = textwrap.fill(product_name, width=30)  # Adjust width to fit your desired max line length

    # Create a new image canvas with extra space for text
    width, height = resized_barcode_img.size
    total_height = height + 120  # Extra space for multi-line Product Name and SKU
    combined_image = Image.new('RGB', (width, total_height), 'white')
    combined_image.paste(resized_barcode_img, (0, 20))  # Add padding at the top

    # Draw wrapped Product Name and SKU centered below the barcode
    draw = ImageDraw.Draw(combined_image)
    current_y = height + 30  # Start drawing text below the barcode

    # Draw each line of the wrapped product name
    for line in wrapped_product_name.splitlines():
        draw.text((width // 2, current_y), line, font=title_font, fill='black', anchor="mm")
        current_y += 30  # Adjust spacing between lines

    # Draw SKU below the product name
    draw.text((width // 2, current_y + 10), f"SKU: {sku}", font=sku_font, fill='black', anchor="mm")

    # Save Image in the specified folder
    file_path = os.path.join(output_folder, f"{sanitized_name}_{sku}.png")
    combined_image.save(file_path)
    print(f"Saved barcode image for {product_name} with SKU {sku} in folder '{output_folder}'")

print("All barcodes generated successfully with text wrapping for long product names.")
