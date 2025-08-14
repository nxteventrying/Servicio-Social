import os
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
import re

# Helper function to extract the alphabetical prefix before the first number
def get_prefix(filename):
    match = re.match(r'^([a-zA-Z]+)', filename)  # Match alphabetical characters at the beginning
    return match.group(1) if match else ''  # Return the prefix or empty string if no match

# Function to group images by their alphabetical prefix before the first number
def group_images_by_prefix(image_files):
    # Sort the images by their prefix and filename
    image_files.sort(key=lambda x: (get_prefix(os.path.basename(x)), os.path.basename(x)))
    return image_files

# Function to convert images to a PDF, ordered by prefix group
def convert_images_to_pdf(image_folder, output_pdf_filename):
    # Gather all image file paths
    image_files = glob.glob(os.path.join(image_folder, "*.png"))  # Adjust extension if needed
    
    # Group and sort images by common prefix
    sorted_image_files = group_images_by_prefix(image_files)
    
    # Create a PDF file to save the images
    with PdfPages(output_pdf_filename) as pdf:
        images_per_page = 4  # Number of images per page
        a4_width, a4_height = 15, 11.69  # A4 dimensions in inches

        num_images = len(sorted_image_files)
        # Loop through images and create pages
        for i in range(0, num_images, images_per_page):
            fig, axs = plt.subplots(images_per_page, 1, figsize=(a4_width, a4_height))  # 4 rows, 1 column, A4 size
            
            for j in range(images_per_page):
                if i + j < num_images:  # Check if image exists
                    img = Image.open(sorted_image_files[i + j])
                    axs[j].imshow(img)
                    axs[j].axis('off')  # Hide axes
                else:
                    axs[j].axis('off')  # Hide unused axes

            # Save the current page with the A4 size
            pdf.savefig(fig,dpi=300, bbox_inches='tight')
            plt.close(fig)

if __name__ == "__main__":
    # Specify the folder containing images and the output PDF filename
    image_folder = "Plots_Lazy"  # Assuming 'plots' is the folder name in the same directory
    output_pdf_filename = "Lazy.pdf"  # Desired output PDF file name

    convert_images_to_pdf(image_folder, output_pdf_filename)

