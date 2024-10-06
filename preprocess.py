import re
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords


# methods will be a list like ["lower", "stopwords"]
# And the function will first convert to lower case
# Then remove stopwords.
def preprocess(methods, text):
    # print(f"BEFORE: {text}")
    methods_dict = {
        "lower": to_lower,
        "stopwords": remove_stopwords,
        "expand": expand_contractions,
    }
    for method in methods:
        text = methods_dict[method](text)
    # print(f"AFTER: {text}")
    return text


def to_lower(text: str):
    return text.lower()


CONTRADICTIONS = {
    "aren't": "are not",
    "can't": "cannot",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "I'd": "I would",
    "I'll": "I will",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it's": "it is",
    "let's": "let us",
    "mightn't": "might not",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "we'd": "we would",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what's": "what is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
}

contractions_re = re.compile("(%s)" % "|".join(CONTRADICTIONS.keys()))


def expand_contractions(text):
    def replace(match):
        return CONTRADICTIONS[match.group(0)]

    return contractions_re.sub(replace, text)


def remove_stopwords(text):
    # Can customize stopword_list
    stopword_list = stopwords.words("english")
    text = " ".join(word for word in text.split() if word not in stopword_list)
    return text
