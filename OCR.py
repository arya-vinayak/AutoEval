from google.cloud import vision
from google.cloud.vision_v1 import types

# Initialize the client
client = vision.ImageAnnotatorClient()

# Path to the image file containing the handwritten text
image_path = '/Users/aryavinayak/Desktop/PES/Hallothon/OCR_TEST/hi.jpeg'

# Read the image
with open(image_path, 'rb') as image_file:
    content = image_file.read()

# Create an image instance
image = types.Image(content=content)

# Perform text detection on the image
response = client.text_detection(image=image)

# Extract text annotations
text_annotations = response.text_annotations

# Check if there is any detected text
if text_annotations:
    # Extract the first annotation (usually the full text)
    full_text = text_annotations[0].description

    # Replace newlines with spaces in the detected text
    full_text = full_text.replace('\n', ' ')

    # Print the detected text
    print("Detected Text:")
    print(full_text)
else:
    print("No text found in the image.")
