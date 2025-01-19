import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

# Set up paths
output_folder = 'barcodes'
pdf_output_path = 'barcodes_output.pdf'

# Configure page settings
page_width, page_height = letter
margin = 36  # 0.5-inch margin on all sides
num_columns = 3  # Number of barcodes per row
spacing_x = 20  # Horizontal spacing between barcodes
spacing_y = 40  # Vertical spacing between barcodes
barcode_width = 200  # Adjust to fit within the layout grid
barcode_height = 150  # Adjust to fit within the layout grid

# Initialize PDF canvas
pdf_canvas = canvas.Canvas(pdf_output_path, pagesize=letter)

# Define starting position for barcodes
x_position = margin
y_position = page_height - margin - barcode_height

# Get list of barcode image files
barcode_files = [f for f in os.listdir(output_folder) if f.endswith('.png')]

for i, barcode_file in enumerate(barcode_files):
    barcode_path = os.path.join(output_folder, barcode_file)

    # Open the barcode image with PIL and resize to fit within the grid cell
    barcode_img = Image.open(barcode_path)
    barcode_img = barcode_img.resize((barcode_width, barcode_height), Image.LANCZOS)

    # Save resized barcode temporarily to insert into PDF
    temp_img_path = f"{output_folder}/temp_{i}.png"
    barcode_img.save(temp_img_path)

    # Draw barcode image on PDF
    pdf_canvas.drawImage(temp_img_path, x_position, y_position, width=barcode_width, height=barcode_height)

    # Update position for the next barcode
    x_position += barcode_width + spacing_x
    if x_position + barcode_width + margin > page_width:  # Move to next row if end of column is reached
        x_position = margin
        y_position -= barcode_height + spacing_y

    # Start a new page if we've reached the bottom of the page
    if y_position < margin:
        pdf_canvas.showPage()
        x_position = margin
        y_position = page_height - margin - barcode_height

# Save and finalize the PDF
pdf_canvas.save()

# Clean up temporary images
for i in range(len(barcode_files)):
    os.remove(f"{output_folder}/temp_{i}.png")

print(f"PDF generated successfully at {pdf_output_path}")
