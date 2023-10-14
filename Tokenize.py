import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.util import ngrams
from nltk.corpus import wordnet
import language_tool_python  

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Sample answer key and student's answer
answer_key = """The part of our brain that leaps to conclusions like this is called
the adaptive unconscious, and the study of this kind of decision
making is one of the most important new fields in psychology.
The adaptive unconscious is not to be confused with the
unconscious described by Sigmund Freud, which was a dark and
murky place filled with desires and memories and fantasies that
were too disturbing for us to think about consciously. This new
notion of the adaptive unconscious is thought of, instead, as a
kind of giant computer that quickly and quietly processes a lot
of the data we need in order to keep functioning as human
beings. When you walk out into the street and suddenly realize
that a truck is bearing down on you, do you have time to think
through all your options? Of course not. The only way that
human beings could ever have survived as a species for as long
as we have is that we’ve developed another kind of decision making apparatus that’s capable of making very quick
judgments based on very little information. As the psychologist
Timothy D. Wilson writes in his book Strangers to Ourselves:
“The mind operates most efficiently by relegating a good deal
of high-level, sophisticated thinking to the unconscious, just as a
modern jetliner is able to fly on automatic pilot with little or no
input from the human,
‘conscious’ pilot.."""
student_answer = """I dont the ans"""

# Weight values for different parameters
weight_values = {
    "Cosine Similarity": 0.5,
    "Jaccard Similarity": 0.05,
    "Bigram Similarity": 0.1,
    "Synonym Similarity": 0.4,
    "Grammar and Spelling": 0.00,
}

# Tokenization, Stop Word Removal, and Lemmatization (same as before)
def preprocess_text(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    return lemmatized_words

answer_key_processed = preprocess_text(answer_key)
student_answer_processed = preprocess_text(student_answer)



# Cosine Similarity
def cosine_similarity_score(text1, text2):
    text1 = ' '.join(text1)
    text2 = ' '.join(text2)
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]

cosine_score = cosine_similarity_score(answer_key_processed, student_answer_processed)

# Jaccard Similarity
def jaccard_similarity_score(text1, text2):
    set1 = set(text1)
    set2 = set(text2)
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return intersection / union

jaccard_score = jaccard_similarity_score(answer_key_processed, student_answer_processed)

# Bigram Similarity
def bigram_similarity_score(text1, text2):
    bigrams1 = list(ngrams(text1, 2))
    bigrams2 = list(ngrams(text2, 2))
    common_bigrams = len(set(bigrams1).intersection(bigrams2))
    total_bigrams = len(bigrams1) + len(bigrams2)
    return common_bigrams / total_bigrams

bigram_score = bigram_similarity_score(answer_key_processed, student_answer_processed)

def synonym_similarity_score(text1, text2):
    total_score = 0
    count = 0
    for word1 in text1:
        for word2 in text2:
            syn1 = set(wordnet.synsets(word1))
            syn2 = set(wordnet.synsets(word2))
            if syn1 and syn2:
                max_score = max(s1.wup_similarity(s2) for s1 in syn1 for s2 in syn2 if s1.wup_similarity(s2) is not None)
                total_score += max_score
                count += 1
    similarity = total_score / count if count > 0 else 0.0
    return similarity

synonym_score = synonym_similarity_score(answer_key_processed[0], student_answer_processed[0])


# Grammar and Spelling Check
def grammar_and_spelling_score(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    error_count = len(matches)
    return error_count

grammar_spelling_score = grammar_and_spelling_score(student_answer)

# Weighted Parameter Evaluation (including Grammar and Spelling)
total_marks = (
    weight_values["Cosine Similarity"] * cosine_score +
    weight_values["Jaccard Similarity"] * jaccard_score +
    weight_values["Bigram Similarity"] * bigram_score +
    weight_values["Synonym Similarity"] * synonym_score +
    weight_values["Grammar and Spelling"] * (1 / (1 + grammar_spelling_score))
)

# Print Total Marks
print("Total Marks:", total_marks)
