from keybert import KeyBERT

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import spacy
import keyword_spacy
import json
import os
import re
import argparse
from llm_test import get_key_llm
from tqdm import tqdm
import glob


def get_keywords_tfidf(text: str):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()

    tfidf_array = tfidf_matrix.toarray()

    avg_tfidf_values = np.mean(tfidf_array, axis=0)

    tfidf_dict = dict(zip(feature_names, avg_tfidf_values))
    sorted_tfidf_dict = dict(
        sorted(tfidf_dict.items(), key=lambda x: x[1], reverse=True)
    )

    lowest_tfidf_words = list(sorted_tfidf_dict.keys())
    return lowest_tfidf_words


def get_keywords_spacy(text: str, nlp_spacy):
    nlp_spacy.add_pipe(
        "keyword_extractor",
        last=True,
        config={"top_n": 11, "min_ngram": 1, "max_ngram": 2},
    )

    doc = nlp_spacy(text.lower())
    keywords = [d[0] for d in doc._.keywords]

    for sent in doc.sents:
        keywords.extend([d[0] for d in sent._.sent_keywords])
    return keywords


def get_keywords(
    text: str,
    lecture_name: str,
    keywords_folder: str,
    modes=["llm", "keybert", "tfidf", "spacy"],
    all_paths={"llm": "./model_path", "keybert": "all-MiniLM-L6-v2"},
) -> list:
    all_key_words = []

    # clean text
    nlp_spacy = spacy.load("ru_core_news_sm")  # should be downloaded first?
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join([w.lemma_ for w in nlp_spacy(text.lower()) if not w.is_stop])

    if "llm" in modes:
        print("Start processing LLM keywords")
        llm_keywords_file = os.path.join(
            keywords_folder, lecture_name + "_llm" + ".json"
        )
        print(llm_keywords_file)

        if os.path.exists(llm_keywords_file):
            with open(llm_keywords_file) as f:
                keywords = json.load(f)
        else:
            # load model every time (?)
            keywords = get_key_llm(model_llm, tokenizer_llm, text)
        all_key_words.extend(keywords)

    # keybert
    if "keybert" in modes:
        print("Start processing KeyBert keywords")

        kw_model = KeyBERT(model="all-MiniLM-L6-v2")

        keywords = kw_model.extract_keywords(
            text, keyphrase_ngram_range=(1, 2), use_mmr=True, nr_candidates=10, top_n=10
        )
        keywords = [w[0] for w in keywords]

        all_key_words.extend(keywords)

    # tfidf
    if "tfidf" in modes:
        print("Start processing TfIdf keywords")

        keywords = get_keywords_tfidf(text)[:20]
        all_key_words.extend(keywords)

    # spacy
    if "spacy" in modes:
        print("Start processing Spacy keywords")

        keywords = get_keywords_spacy(text, nlp_spacy)
        all_key_words.extend(keywords)

    return all_key_words


def parse_files(files_folder: str, save_dir: str):

    for f_path in tqdm(glob.iglob(f"{files_folder}/*.json")):
        with open(f_path) as f:
            text = json.load(f)["text"]

        file_name = f_path.split("/")[-1]

        lecture_keywords = get_keywords(text, file_name[:-5], 
                                "./data/textfiles/keywords/")


        with open(os.path.join(save_dir, file_name), 'w', encoding='utf-8') as jsf:
            lecture_keywords = list(set([d.strip() for d in lecture_keywords if len(d) > 2]))
            json.dump(lecture_keywords, jsf, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parse_files("./train_data/textfiles/raw",
            "./train_data/textfiles/keywords")