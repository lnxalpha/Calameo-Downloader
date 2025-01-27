import requests
import os
from PIL import Image
import cairosvg

# divide the image url based off of the base and token
# Base URL parts
base_url = "https://"
token = "?_token_="

# Output directory
output_dir = "downloaded_images"
os.makedirs(output_dir, exist_ok=True)

# File extensions to try (e.g., .svgz, .jpeg, .svg)
file_extensions = ["svgz", "jpeg", "svg"]

# Iterating through pages
for i in range(1, _):
    success = False
    for ext in file_extensions:
        url = f"{base_url}p{i}.{ext}{token}"
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(output_dir, f"p{i}.{ext}")
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {file_path}")
                success = True
                break  # Exit the loop once the file is downloaded successfully
            else:
                print(f"Attempt {url} failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    if not success:
        print(f"Failed to download page {i} with any extension.")

print("Download process completed.")


# Directory containing .svgz files
svgz_dir = "downloaded_images"
output_image_dir = "converted_images"
os.makedirs(output_image_dir, exist_ok=True)

# Convert .svgz files to image files
def convert_svgz_to_images(svgz_dir, output_image_dir):
    for filename in sorted(os.listdir(svgz_dir)):
        if filename.endswith('.svgz'):
            svgz_path = os.path.join(svgz_dir, filename)
            output_path = os.path.join(output_image_dir, f"{os.path.splitext(filename)[0]}.png")
            try:
                with open(svgz_path, 'rb') as svgz_file:
                    svg_data = svgz_file.read()
                    cairosvg.svg2png(bytestring=svg_data, write_to=output_path)
                print(f"Converted: {svgz_path} -> {output_path}")
            except Exception as e:
                print(f"Error converting {svgz_path}: {e}")


# Compile images into a PDF
def compile_images_to_pdf(image_dir, output_pdf):
    images = []
    for i in range(1, _):  # Ensure sequential order
        filename = f"p{i}.png"  # Assuming files are named p1.png, p2.png, etc.
        img_path = os.path.join(image_dir, filename)
        if os.path.exists(img_path):
            img = Image.open(img_path).convert("RGB")
            images.append(img)
        else:
            print(f"Missing file: {filename}")

    if images:
        pdf_path = os.path.join(image_dir, output_pdf)
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF created: {pdf_path}")
    else:
        print("No images found to compile into a PDF.")

# Execute the conversion and compilation
convert_svgz_to_images(svgz_dir, output_image_dir)
compile_images_to_pdf(output_image_dir, "compiled_output.pdf")
