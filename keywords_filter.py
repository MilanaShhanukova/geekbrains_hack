from collections import Counter

import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

import numpy as np
import spacy
import re

from nltk import ngrams



def filter_keywords(keywords: list, text: str, common_words: list):
    nlp_spacy = spacy.load("ru_core_news_sm") # should be downloaded first? 
    text = re.sub(r'[^\w\s]', '', text)
    text = " ".join([w.lemma_ for w in nlp_spacy(text.lower()) if not w.is_stop])

    ngram_list = []
    for i in range(3):
        ngram_list.extend(list(ngrams(text.split(), i)))

    # Count the frequencies
    ngram_frequencies = Counter(ngram_list)

    median_value = np.median(list(ngram_frequencies.values()))

    keywords = list(set(keywords))

    # if it's a rare word, do not add it 
    print(f"Length of keywords BEFORE filtering common in text {len(keywords)}")
    keywords = [k for k in keywords if ngram_frequencies[k] <= median_value]
    
    print(f"Length of keywords AFTER filtering common {len(keywords)}")

    # filter in the 10000 words dictionary
    print(f"Length of keywords BEFORE filtering common in dictionary {len(keywords)}")
    keywords = [k for k in keywords if k not in common_words]
    print(f"Length of keywords AFTER filtering common in dictionary {len(keywords)}")

    english_words = []
    for w in keywords:
        is_english = bool(re.match('^[a-zA-Z\s]+$', w))
        if is_english:
            english_words.append(w)
            
    keywords = [k for k in keywords if k not in english_words]
    print(f"Length of keywords AFTER filtering english words {len(keywords)}")

    keywords = [k for k in keywords if len(k.split()) <= 3]

    return keywords, english_words


def filter_file(lecture_text_path: str, keywords_path: str, save_dir: str):
    with open("./10000-russian-words.txt", encoding='utf-8') as f:
        common_words = f.read().splitlines()
    #print(common_words)
    #exit()

    lecture_num = lecture_text_path.split('/')[-1][:-5]
    with open(lecture_text_path, encoding='utf-8') as f:
        text = json.load(f)["text"]

    with open(keywords_path, encoding='utf-8') as f:
        lecture_keywords = json.load(f)

    keywords_filtered, english_words = filter_keywords(lecture_keywords, text, common_words)

    with open(os.path.join(save_dir, lecture_num + "_keywords_filtered.json"), 'w', encoding='utf-8') as jsf:
        json.dump(keywords_filtered, jsf, ensure_ascii=False, indent=4)
    
    with open(os.path.join(save_dir, lecture_num + "_keywords_english.json"), 'w', encoding='utf-8') as jsf:
        json.dump(english_words, jsf, ensure_ascii=False, indent=4)

    return keywords_filtered, english_words
