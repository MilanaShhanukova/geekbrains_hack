import pandas as pd
import os
import json
import csv
from typing import List


def get_timestamp_text(input_file_path, directory_path):
    input_file_path = directory_path + 'raw/' + input_file_path
    with open(input_file_path, 'r', encoding='utf-8') as file:
        all_items = json.load(file)['chunks']

    timestamps, texts = [], []

    for item in all_items:
        timestamps.append(item['timestamp'])
        texts.append(item['text'])
    return (timestamps, texts)


def format_seconds_to_minutes_seconds(time):
    minutes = int(time // 60)
    seconds = int(time % 60)
    return f"{minutes:02d}:{seconds:02d}"


def matching(lecture, timestamps: List[List[int]], texts: List[str], lst: List[str], directory_path='geekbrains_hack/data/textfiles/'):
    data = []
    found_keywords = set()

    for i, text in enumerate(texts):
        for keyword in lst:
            if keyword in text and keyword not in found_keywords:
                with open(directory_path + 'submit/timecodes.csv', 'a', newline='', encoding='utf-8') as file:
                    time_list = timestamps[i]
                    formatted_times = [format_seconds_to_minutes_seconds(time) for time in time_list]
                    formatted_range = f"{formatted_times[0]} - {formatted_times[1]}"

                    capitalized_keyword = keyword.capitalize()
                    df = pd.DataFrame([[lecture, capitalized_keyword, formatted_range]], columns=['File', 'Term', 'Time'])
                    df.to_csv(file, header=not file.tell(), index=False)
                found_keywords.add(keyword)
                break



def main(directory_path):
    raw_file_list = []
    keywords_file_list = []
    for root, dirs, files in os.walk(directory_path + 'raw'):
        for file in files:
            raw_file_list.append(file)
    
    for raw_file in raw_file_list:
        rfke = raw_file[:-5] + '_keywords_english' + raw_file[-5:]
        rfkf = raw_file[:-5] + '_keywords_filtered' + raw_file[-5:]
        eng_and_filt = (rfke, rfkf)
        keywords_file_list.append(eng_and_filt)
    return keywords_file_list, raw_file_list


def get_list(input_files_path, directory_path):
    input_kwe_path = directory_path + 'keywords/' + input_files_path[0]
    input_fwf_path = directory_path + 'keywords/' + input_files_path[1]

    with open(input_kwe_path, 'r', encoding='utf-8') as file:
            lst1 = json.load(file)
    with open(input_fwf_path, 'r', encoding='utf-8') as file:
            lst2 = json.load(file)
    
    return lst1 + lst2
 

if __name__ == '__main__':
    directory_path = f'E:/dev/geekbrains_hack/data/textfiles/'
    keywords_file_list, raw_file_list = main(directory_path)
    for idx, keywords_file in enumerate(keywords_file_list):
        lst = get_list(keywords_file, directory_path)
        timestamps, texts = get_timestamp_text(raw_file_list[idx], directory_path)
        matching(raw_file_list[idx], timestamps, texts, lst, directory_path)
