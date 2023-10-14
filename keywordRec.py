import yake

def keyWrds():
    kw_extractor = yake.KeywordExtractor()

    #Input and output file paths
    input_file_path = "./temporaryFiles/summarizerOutput.txt"
    output_file_path = "./temporaryFiles/keywordOutput.txt"

    #reading from the input file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    #parameters to tune
    language = "en"
    max_ngram_size = 3  #maximum ngram size - used to determine how many words maximum to consider a keyword
    deduplication_threshold = 0.3  #used for deduplication of keywords
    numOfKeywords = 40    #number of keywords to extract

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
    
    keywords = custom_kw_extractor.extract_keywords(text)
    # for kw in keywords:
    #     print(kw[0])
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for kw in keywords:
            output_file.write(kw[0] + "\n")