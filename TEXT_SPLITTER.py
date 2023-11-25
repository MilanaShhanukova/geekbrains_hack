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
import pymorphy2


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
        # line = f"# Абзац {idx}:\n{paragraph}\n\n"
        line = f"# Абзац\n{paragraph}\n\n"
        paragraphs += line
    return paragraphs


def replace_headers(text, keywords):
    lemmatizer = WordNetLemmatizer()
    morph = pymorphy2.MorphAnalyzer()

    paragraphs = text.split('\n\n')
    new_paragraphs = []

    for paragraph in paragraphs:
        words_in_paragraph = word_tokenize(paragraph)

        lemmatized_words = [lemmatizer.lemmatize(word.lower(), pos='n') for word in words_in_paragraph]
        lemmatized_keywords = [lemmatizer.lemmatize(word.lower(), pos='n') for word in keywords]

        unique_lemmatized = list(set(lemmatized_words))
        lemmatized_keywords = list(set(lemmatized_keywords))

        matches = [word for word in lemmatized_keywords if word in unique_lemmatized]
        print(matches)

        words_to_replace = []
        for word in matches:
            parsed_word = morph.parse(word)[0]
            normal_form = parsed_word.normal_form
            print(word, normal_form)
            words_to_replace.append(normal_form)

        words_to_replace = [word.capitalize() for word in words_to_replace]
        words_to_replace = [f'{word} |' for word in words_to_replace]

        words_to_replace = list(set(words_to_replace))
        words_to_replace = ' '.join(words_to_replace)
        words_to_replace = '# ' + words_to_replace

        if 'приветствую' in paragraph.lower() or 'приветствуем' in paragraph.lower() or 'всем привет' in paragraph.lower() or 'добрый день' in paragraph.lower():
            replaced_paragraph = paragraph.replace('# Абзац', '# Вступление')
        
        elif 'на этом, друзья' in paragraph.lower() or 'всем большое спасибо' in paragraph.lower() or 'до связи' in paragraph.lower() or 'подведем итоги' in paragraph.lower() or 'на сегодня все' in paragraph.lower() or 'до встречи ' in paragraph.lower() or 'счастливо' in paragraph.lower():
            replaced_paragraph = paragraph.replace('# Абзац', '# Заключение')

        elif words_to_replace and words_to_replace != '# ':
            replaced_paragraph = paragraph.replace('# Абзац', words_to_replace)
        else:
            replaced_paragraph = paragraph
        
        new_paragraphs.append(replaced_paragraph)

    return '\n\n'.join(new_paragraphs)

# def replace_headers(text, keywords):
#     paragraphs = text.split('\n\n')
#     new_paragraphs = []

#     for paragraph in paragraphs:
#         words_in_paragraph = set(word_tokenize(paragraph))  # Получаем уникальные слова в параграфе
#         words_to_replace = [word for word in keywords if word in words_in_paragraph]
        
#         if words_to_replace:
#             combined_words = ' '.join(words_to_replace)
#             replaced_paragraph = paragraph.replace('# Абзац', combined_words)
#         else:
#             replaced_paragraph = paragraph  # Сохраняем исходный параграф без замены
        
#         new_paragraphs.append(replaced_paragraph)

#     return '\n\n'.join(new_paragraphs)


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

        final_text = frame_stars_without_lemmat(final_text, keywords_1 + keywords_2)
        final_text = replace_headers(final_text, keywords_1 + keywords_2)

        doc = Document()
        doc.add_paragraph(final_text)
        output_docx_path = directory_path + 'files/' + file_path[:-5] + '.docx'
        if os.path.exists(output_docx_path):
            os.remove(output_docx_path)

        doc.save(output_docx_path)


if __name__ == '__main__':
    directory_path = f'E:/dev/geekbrains_hack/data/textfiles/'
    main(directory_path)


