# matcher.py

import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def clean_text_spacy(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha and not token.is_punct]
    return " ".join(tokens)

def get_match_score(resume_text, job_description):
    cleaned_jd = clean_text_spacy(job_description)
    cleaned_resume = clean_text_spacy(resume_text)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([cleaned_jd, cleaned_resume])
    
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return score

def is_match(score, threshold=0.35):
    return score >= threshold
