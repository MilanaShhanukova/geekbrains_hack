import os
import json
from keywords_pipe import get_keywords
from whisper_test import process_file_whisper
from keywords_filter import filter_file
from llm_test import get_key_stage2_llm, get_model_and_tokenizer
import pandas as pd

test_dir = 'test_data/audiofiles/'
save_dir_raw = 'test_result/raw/'
save_dir_key = 'test_result/keywords/'
save_dir_end = 'test_result/'

#submission_data = pd.DataFrame(columns=['File', 'Term'])
file_list = []
key_list = []
for f in os.listdir(test_dir):
    if '.mp3' in f:
        text = process_file_whisper(os.path.join(test_dir, f))
        with open(os.path.join(save_dir_raw, f'{f[:-4]}.json'), 'w', encoding='utf-8') as jsf:
            json.dump(text, jsf, ensure_ascii=False, indent=4)
        keywords = get_keywords(text['text'], f, save_dir_raw, gen_description=False)
        with open(os.path.join(save_dir_key, f'{f[:-4]}.json'), 'w', encoding='utf-8') as jsf:
            json.dump(keywords, jsf, ensure_ascii=False, indent=4)

        keywords_filtered, english_words = filter_file(f'{save_dir_raw}{f[:-4]}.json',
                                                       f'{save_dir_key}{f[:-4]}.json', '')

        model_llm, tokenizer_llm, device = get_model_and_tokenizer()
        final_keywords = get_key_stage2_llm(keywords_filtered, text, model_llm, tokenizer_llm, device, f)
        del model_llm, tokenizer_llm, device
        with open(os.path.join(save_dir_end, f'{f[:-4]}_final_keywords.json'), 'w', encoding='utf-8') as jsf:
            json.dump(final_keywords, jsf, ensure_ascii=False, indent=4)
        print(final_keywords)
        file_list = file_list + [f] * len(final_keywords)
        print(file_list)
        key_list = key_list + final_keywords
        print(key_list)
        sub_df = pd.DataFrame(columns=['File', 'Term'])
        sub_df['File'] = file_list
        sub_df['Term'] = key_list
        sub_df.to_csv(f'{save_dir_end}submission.csv', index=False)