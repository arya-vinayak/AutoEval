from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from google.cloud import vision
from google.cloud.vision_v1 import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ServiceAcc_Token.json"
from transformers import pipeline
import yake
from summy import summary
from keywordRec import keyWrds
from evaluator import eval


app = FastAPI()


@app.post("/detect_text/")
async def detect_text(image: UploadFile):
    # Check if an image file was provided
    if not image:
        return JSONResponse(content={"error": "No image file provided."}, status_code=400)

    with open(f"uploads/{image.filename}", "wb") as f:
        f.write(image.file.read())
    try:
    # Read the image content
        image_content = image.file.read()

        # Initialize the Google Vision client
        client = vision.ImageAnnotatorClient()

        # Create an image instance
        vision_image = types.Image(content=image_content)

        # Perform text detection on the image
        response = client.text_detection(image=vision_image)

        # Extract text annotations
        text_annotations = response.text_annotations

        # Check if there is any detected text
        if text_annotations:
            # Extract the first annotation (usually the full text)
            detected_text = text_annotations[0].description

            # Replace newlines with spaces in the detected text
            detected_text = detected_text.replace('\n', ' ')
            print(detected_text)
            #opening the ocr output file    
            with open('./temporaryFiles/ocrOutput.txt', 'w', encoding='utf-8') as output_file:
                output_file.write(detected_text)

            #summarizing the text using the summarizer
            summary()

            #opening the summarizer output file
            with open('./temporaryFiles/summarizerOutput.txt', 'r', encoding='utf-8') as input_file:
                summary_text = input_file.read()

            #extracting keywords using the keyword extractor
            keyWrds()
            #opening the keyword extractor output file
            with open('./temporaryFiles/keywordOutput.txt', 'r', encoding='utf-8') as input_file:
                extractedKeywords = input_file.read()
            #evaluating the summary
            eval()
            
            return JSONResponse(content={"summary_text:":summary_text,
                                         "keywords:":extractedKeywords
                                         } ,media_type="text/html", status_code=200)
        else:
            return JSONResponse(content={"message": "No text found in the image."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)