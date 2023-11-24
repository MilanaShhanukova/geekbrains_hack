# -*- coding: utf-8 -*-

import json
import re
import os
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import blankline_tokenize
from nltk.stem import WordNetLemmatizer
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX
from typing import List

nltk.download('punkt')
nltk.download('wordnet')


def split_chunck(data):
    threshold = 9
    combined_text = ''

    for i, chunk in enumerate(data['chunks']):
        start = chunk['timestamp'][0]
        stop = chunk['timestamp'][1]
        chunk_text = chunk['text']
        # print(start, stop, chunk_text)

        combined_text += chunk_text

        if i < len(data['chunks']) - 1:
            next_start = data['chunks'][i + 1]['timestamp'][0]
            if next_start - stop > threshold:
                combined_text += f'\n\n'

    return combined_text


def split_into_paragraphs(text, keywords):
    paragraphs = text.split('\n\n')
    new_paragraphs = []

    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph)
        current_paragraph = []
        
        for sentence in sentences:
            words = nltk.word_tokenize(sentence.lower())  # Convert to lowercase for case-insensitive comparison
            contains_keyword = any(word.strip() in keywords for word in words)

            if contains_keyword:
                if current_paragraph:
                    new_paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
            current_paragraph.append(sentence)

        if current_paragraph:
            new_paragraphs.append(' '.join(current_paragraph))

    return new_paragraphs

def get_paragraphs(input_text):
    keywords = {
        'немножко подробнее', 'для лучшего понимания', 'друзья, давайте', 'следующий этап', 'следующим пунктом',
        'давайте забежим', 'давайте рассмотрим', 'итак', 'работать', 'второй', 'введение', 'глава', 'раздел',
        'далее', 'приступим', 'рассмотрим', 'давайте подведем ее итоги', 'давайте подведем итоги', 'подведем итоги',
        'ну что , друзья', 'ну что, друзья', 'в заключении'
    }
    result = split_into_paragraphs(input_text, keywords)

    paragraphs = ''
    for idx, paragraph in enumerate(result, 1):
        formatted_paragraph = '\t' + paragraph.replace('\n', '\n\t')
        line = f"\t# Абзац {idx}:\n{formatted_paragraph}\n\n"
        paragraphs += line
    return paragraphs




# def split_into_paragraphs(text, keywords):
#     paragraphs = text.split('\n\n')
#     new_paragraphs = []

#     for paragraph in paragraphs:
#         sentences = sent_tokenize(paragraph)
#         current_paragraph = []
        
#         for sentence in sentences:
#             words = nltk.word_tokenize(sentence)
#             contains_keyword = any(word.strip().lower() in keywords for word in words)

#             if contains_keyword:
#                 if current_paragraph:
#                     new_paragraphs.append(' '.join(current_paragraph))
#                     current_paragraph = []
#             current_paragraph.append(sentence)

#         if current_paragraph:
#             new_paragraphs.append(' '.join(current_paragraph))

#     return new_paragraphs


# def get_paragraphs(input_text):
#     keywords = {
#         'немножко подробнее', 'для лучшего понимания', 'друзья, давайте', 'следующий этап', 'следующим пунктом', 'давайте забежим', 'давайте рассмотрим', 'итак', 'работать',
#         'второй', 'введение', 'глава', 'раздел', 'далее', 'приступим', 'рассмотрим', 'давайте подведем ее итоги', 'давайте подведем итоги',
#         'подведем итоги', 'ну что , друзья', 'ну что, друзья', 'в заключении'}
#     result = split_into_paragraphs(input_text, keywords)

#     paragraphs = ''
#     for idx, paragraph in enumerate(result, 1):
#         formatted_paragraph = '\t' + paragraph.replace('\n', '\n\t')
#         line = f"\t# Абзац {idx}:\n{formatted_paragraph}\n\n"
#         paragraphs += line
#     return paragraphs


# def frame_stars(final_text: str, keyword: List[str]) -> str:
#     lemmatizer = WordNetLemmatizer()
#     lines = final_text.split('\n')
#     marked_words = set()
#     processed_lines = []

#     for line in lines:
#         words = word_tokenize(line)
#         processed_words = []

#         for word in words:
#             lemma_word = lemmatizer.lemmatize(word.lower())
#             if lemma_word in keyword and lemma_word not in marked_words:
#                 processed_words.append(f'*{word}*')
#                 marked_words.add(lemma_word)
#             else:
#                 processed_words.append(word)

#         processed_lines.append(' '.join(processed_words))

#     return '\n'.join(processed_lines)


def frame_stars_without_lemmat(final_text: str, keywords: List[str]) -> str:
    marked_text = final_text

    for phrase in keywords:
        pattern = re.compile(r'\b{}\b'.format(re.escape(phrase)), re.IGNORECASE)
        marked_text = pattern.sub(lambda match: '*' + match.group(0) + '*', marked_text, count=1)
    
    return marked_text


def main(directory_path):
    files_list = []
    for root, dirs, files in os.walk(directory_path + 'raw'):
        for file in files:
            files_list.append(file)

    for file_path in files_list:
        print(file_path)
        input_file_path = directory_path + 'raw/' + file_path
        keywords_file_path_eng = directory_path + 'keywords/' + file_path[:-5] + '_keywords_english.json'
        keywords_file_path_fil = directory_path + 'keywords/' + file_path[:-5] + '_keywords_filtered.json'

        with open(input_file_path, 'r', encoding='utf-8') as file:
            final_text = json.load(file)
            final_text = split_chunck(final_text)
            final_text = get_paragraphs(final_text)
        
        with open(keywords_file_path_eng, 'r', encoding='utf-8') as file:
            keywords_1 = json.load(file)
        
        with open(keywords_file_path_fil, 'r', encoding='utf-8') as file:
            keywords_2 = json.load(file)
        
        
        # final_text = frame_stars(final_text, keywords_1 + keywords_2)
        final_text = frame_stars_without_lemmat(final_text, keywords_1 + keywords_2)


        doc = Document()
        doc.add_paragraph(final_text)
        output_docx_path = directory_path + 'files/' + file_path[:-5] + '.docx'
        if os.path.exists(output_docx_path):
            os.remove(output_docx_path)

        doc.save(output_docx_path)

        # highlighting
        # doc = Document(output_docx_path)

        # for keyword in keywords:
        #     doc = split_Runs(doc, keyword)
        # for keyword in keywords:
        #     doc = style_Token(doc, keyword)
    
        # if os.path.exists(output_docx_path):
        #     os.remove(output_docx_path)

        # doc.save(output_docx_path)



# def split_text(text, word):
#     pattern = re.compile(r'([\S\s]*)(\b{})([\S\s]*)'.format(word))
#     match = pattern.search(text)
#     if match:
#         return match.groups()
#     return ('', '', '')


# def split_Runs(doc,word):
#     for p in doc.paragraphs:
#         if p.text.find(word) != -1:
#             virtualRuns=p.runs
#             p.text = ""
#             for r in virtualRuns:
#                 if r.text.find(word) != -1:
#                     before, word, after = split_text(r.text, word)
#                     p.add_run(before)
#                     p.add_run()
#                     p.add_run(word)
#                     p.add_run(after)
#                 else:
#                     p.add_run(r.text)
#     return doc

# def style_Token(doc,word):
#     for p in doc.paragraphs:
#         for i,r in enumerate(p.runs):
#             if p.runs[i].text.find(word) != -1:
#                 p.runs[i].font.highlight_color = WD_COLOR_INDEX.YELLOW
#     return doc


if __name__ == '__main__':
    directory_path = f'E:/dev/geekbrains_hack/data/textfiles/'
    main(directory_path)


