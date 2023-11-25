import torch
import json
from tqdm import tqdm
from summarization_model_saiga_mistral import interact


def summarize(model_path, input_file_path, output_file_path, max_chunk_length=4000):

    with open(input_file_path, 'r', encoding='utf-8') as file:
        article_text = json.load(file)['text']
        print(len(article_text))

   
    chunks = [article_text[i:i + max_chunk_length] for i in range(0, len(article_text), max_chunk_length)]

    summaries = []
    with tqdm(total=len(chunks)) as pbar:
        for chunk in chunks:
            prompt_text = 'Напиши суммаризацию следующего текста в пяти предложениях:'
            input_text = f"{prompt_text} '{chunk}'"
            print()
            print('INPUT_TEXT: ', input_text, '\n')
            summary = interact(model_path, input_text, output_file_path)
            # summaries.append(summary)
            pbar.update(1)
    # final_summary = ' '.join(summaries)
    # return final_summary


# Пока для одной лекции 
model_path = 'E:/dev/hacks3/llm_formalization_text/model-q4_K.gguf'
input_file_path = 'E:/dev/geekbrains_hack/data/textfiles/raw/lecture_3.json'
output_file_path = 'E:/dev/geekbrains_hack/data/textfiles/summarized_lectures/lecture_3.txt'

summarize(model_path, input_file_path, output_file_path)