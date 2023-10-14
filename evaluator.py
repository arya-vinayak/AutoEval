def eval():
    input_file = "./temporaryFiles/keywordOutput.txt"
    answer_key = "./temporaryFiles/answerKey.txt"

    # Define the answer key as a list of keywords
    with open(answer_key, "r", encoding="utf-8") as file:
        answer_key = file.read().split()


    # Read the content of the text file
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Split the text into words
    words = text.split()

    # Initialize a counter for matching words
    matching_count = 0

    # Iterate through the words and count matching keywords
    for word in words:
        if word in answer_key:
            matching_count += 1

    # Calculate the matching percentage
    matching_percentage = (matching_count / len(answer_key)) * 100

    # Print the result
    print(f"Matching Percentage: {matching_percentage:.2f}%")

    marks = 10 #
    marks = float(marks)
    print(f"Your marks are {marks*matching_percentage/100}")