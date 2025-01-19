 Barcode Generator and PDF Formatter

This project generates scannable barcodes from a CSV file containing product names and SKUs, formats them into images, and organizes these images into a PDF for easy printing, laminating, and cutting.

HOW TO USE
- 

Features
- **Barcode Generation**: Creates scannable barcodes with consistent dimensions.
- **Custom Layout**: Formats each barcode with the product name (bold) and SKU centered below the barcode.
- **PDF Output**: Compiles all generated barcode images into a PDF in a 3-column, 4-row grid layout for easy printing.

Prerequisites
Ensure you have the following installed:
- Python 3.7 or higher
- Required Python libraries:
  - `pandas`
  - `Pillow`
  - `python-barcode`
  - `reportlab`

Install the required libraries using:
```bash
pip install pandas Pillow python-barcode reportlab
