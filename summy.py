import os
from transformers import pipeline

def summary():
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'
    model = pipeline('summarization', model='facebook/bart-large-cnn')

    #setting up the input and output file paths
    input_file_path = './temporaryFiles/ocrOutput.txt'
    output_file_path = './temporaryFiles/summarizerOutput.txt'

    #getting the input text from the input file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    #using deterministic method in order to keep the meaning of what the user wrote each time and not to add in extra creative content 
    summary = model(text, max_length=50, min_length=20, do_sample=False)
    print(summary[0]['summary_text'])

    #writing the summary to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(summary[0]['summary_text'])