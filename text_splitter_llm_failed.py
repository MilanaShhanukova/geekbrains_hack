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

import torch
from tqdm import tqdm
from summarization_model_saiga_mistral import interact

# nltk.download('punkt')
# nltk.download('wordnet')



def formatter(model_path, input_file_path, output_file_path, max_chunk_length=4000):

    with open(input_file_path, 'r', encoding='utf-8') as file:
        article_text = json.load(file)['text']
        print(len(article_text))
    
    summaries = []
    chunks = [article_text[i:i + max_chunk_length] for i in range(0, len(article_text), max_chunk_length)]
    with tqdm(total=len(chunks)) as pbar:
        for chunk in chunks:
            llm_prompt = '''You are a helpfull data quality assistant that is tasked with generate notes using Markdown syntax from raw text data.
Write headers for every topics discussed, use unordered list to enumerate anything, hyperlinks for urls and code blocks to format code.

Here is Markdown syntax:
- To create a headers, add up to three # symbols before your heading text. The number of # symbols determines the size of the heading.
- To enumerate anything add a -, *, or + before the text.
- You can format code within a sentence using single backticks. To format a block of code, surround the code with tripple backticks.

Here is the raw text to process:
{chunk}

Write in Russian please 
Note in Markdown format:
'''

            input_text = llm_prompt.format(chunk=chunk)
            print()
            print('INPUT_TEXT: ', input_text, '\n')
            summary = interact(model_path, input_text, output_file_path)
            # summaries.append(summary)
            pbar.update(1)
    # final_summary = ' '.join(summaries)
    # return final_summary


if __name__ == '__main__':
    model_path = 'E:/dev/hacks3/llm_formalization_text/model-q4_K.gguf'
    input_file_path = 'E:/dev/geekbrains_hack/data/textfiles/raw/lecture_1.json'
    output_file_path = 'E:/dev/geekbrains_hack/data/textfiles/files/lecture_1_test_llm.txt'

    formatter(model_path, input_file_path, output_file_path)


