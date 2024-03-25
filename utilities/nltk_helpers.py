import json
import re
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize




def download_nltk_packages():
    """Download necessary NLTK packages."""
    packages = ['punkt', 'stopwords']

    for package in packages:
        try:
            if package == 'punkt':
                word_tokenize("The word_tokenize function will raise an error if 'punkt' is not available.")
            elif package == 'stopwords':
                stopwords.words('English')
        except LookupError:
            nltk.download(package)


def load_keywords():
    """Load keywords for each category from a JSON file."""
    keywords_file_path = 'resources/email_categories.json'

    with open(keywords_file_path, 'r') as file:
        categories_keywords = json.load(file)

    return categories_keywords


def preprocess_and_tokenize(text):
    """Preprocess and tokenize text into unique tokens using NLTK."""

    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]

    return set(tokens)

def categorize_email(subject, body):
    """Categorize an email based on its subject and body content."""

    download_nltk_packages()
    categories_keywords = load_keywords()
    content_tokens = preprocess_and_tokenize(subject + " " + body)

    category_counts = {category: 0 for category in categories_keywords.keys()}
    
    for token in content_tokens:
        for category, keywords in categories_keywords.items():
            if token in keywords:
                category_counts[category] += 1

    max_category = max(category_counts, key=category_counts.get)

    return max_category