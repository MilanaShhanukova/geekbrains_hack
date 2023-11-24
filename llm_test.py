import os
import struct

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json


def get_key_llm(text, model, tokenizer, device, name):
    with torch.inference_mode():
        answer_list = []
        description_dict = {}
        for part in range(0, len(text["text"]) // 6000 + 1):
            context = text["text"][part*6000:(part+1)*6000]
            user_text = f'I have the following document:\n\n{context}\n\nBased on the information above, extract the keywords that best describe the topic of the text.\nMake sure to only extract keywords that appear in the text.\nUse the following format separated by commas:\n<keywords>\nAnswer in Russian.'
            #user_text = f'I have the following document:\n\n{context}\n\nBased on the information above, extract the most important topics that best describe the text to understand.\n.\nUse the following format separated by commas:\n<keywords>\nAnswer in Russian.'
            chat = [
                {"role": "system", "content": "The following is a conversation with an AI Large Language Model. The AI has been trained to answer questions, provide recommendations, and help with decision making. The AI follows user requests. The AI thinks outside the box."},
                {"role": "user", "content": user_text},
            ]

            input_tokens = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=False)
            print(f'Length of chat tokens (chat tokens + answer must be below 4096): {len(input_tokens)}')
            input_len = len(input_tokens)
            input_tokens = torch.LongTensor([input_tokens]).to(device=device)

            out = model.generate(
                input_ids=input_tokens,
                do_sample=False,
                max_new_tokens=400,
                repetition_penalty=1.2,
                #eos_token_id=[32000, 28705],
            )
            answer = tokenizer.batch_decode(out[:,input_len:], skip_special_tokens=True)[0]
            print(answer)
            answer_list.append(str.strip(answer))

            for keyword in str.split(str.strip(answer), ','):
                description_dict[keyword] = get_description_llm(keyword, context, model, tokenizer, device)

        with open(f'{str.replace(name, ".mp3", "_keywords.json")}', 'w', encoding='utf-8') as jsf:
            json.dump(answer_list, jsf, ensure_ascii=False, indent=4)
        with open(f'{str.replace(name, ".mp3", "_descriptions.json")}', 'w', encoding='utf-8') as jsf:
            json.dump(description_dict, jsf, ensure_ascii=False, indent=4)

    answer_full_list = []
    for ans in answer_list:
        split_ans = str.split(ans, ',')
        for s in split_ans:
            if str.replace(s, '.', '') not in answer_full_list:
                answer_full_list.append(str.replace(s, '.', ''))
    return answer_full_list

def get_key_stage2_llm(keywords, text, model, tokenizer, device, name):
    with torch.inference_mode():
        answer_list = []
        for part in range(0, len(text["text"]) // 6000 + 1):
            context = text["text"][part * 6000:(part + 1) * 6000]
            keywords_string = '            [\n'
            for k in keywords:
                keywords_string = keywords_string + '    ' + '"' + k + '",\n'
            keywords_string = keywords_string[:-2] + '\n]'
            #print(keywords_string)
            #keywords_string = '''
            '''
            [
    "проверка четности",
    "итеративные процессы",
    "бесконечный цикл",
    "элементы",
    "чтение файла",
    "язык программирования c-sharp",
    "гири",
    "специальности",
    "быстро рекомендация",
    "английский язык",
    "методы вывода.",
    "алгоритмы",
    "язык программирования c#",
    "переменные",
    "участок память",
    "кодировка",
    "разработка программного обеспечения",
    "условные операторы",
    "итерационные процессы",
    "циклические структуры",
    "упражнения",
    "автоматизированное тестирование.",
    "представить пример",
    "массив array",
    "averagedialedtemperatures сократить",
    "структура данных",
    "csharp цикл",
    "именование объектов",
    "массив формирование",
    "блок-схема",
    "индекс элемента массива",
    "задачи",
    "сообщения об ошибках",
    "изучение документации",
    "заполнение массива",
    "деление по модулю",
    "utf-8",
    "типы данных",
    "запустить проект",
    "основные характеристики",
    "условия",
    "тестировщик программного обеспечения",
    "среднее значение",
    "язык c-sharp",
    "c-sharp",
    "итерации",
    "функциональные свойства",
    "элемент массив",
    "весовые гири",
    "создание массива",
    "length раз",
    "элементы массива",
    "ключевые слова foreach",
    "цикл for",
    "вывод на экран",
    "технический английский язык",
    "среднее арифметическое",
    "переменные счетчиков",
    "операторы сравнения",
    "репозиторий",
    "максимальное значение",
    "обращение к элементам",
    "язык программирования",
    "массивы",
    "форматирование кода",
    "индексация",
    "utf8 unicode",
    "блок-схемы",
    "арифметические операторы",
    "операции ввода-вывода",
    "циклы",
    "цикл while",
    "алгоритмическое мышление",
    "суммирование"
]
            '''
            #print(keywords_string)
            #print(keywords_string[0:15])
            #print('-----------------------')
            #print(keywords_string)
            user_text = f'You are a student who is studying computer science. I have the following keywords:\n\n{keywords_string}\n\nfrom the lesson:\n\n{context}\n\nBased on the both keywords and the text of the lesson above, pick three most important terms and output them.\nMake sure to only extract keywords that appear in the text.\nUse the following format separated by commas:\n<keywords>\nAnswer in Russian.'

            chat = [
                {"role": "system",
                 "content": "The following is a conversation with an AI Large Language Model. The AI has been trained to answer questions, provide recommendations, and help with decision making. The AI follows user requests. The AI thinks outside the box."},
                {"role": "user", "content": user_text},
            ]

            input_tokens = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=False)
            input_tokens = input_tokens + tokenizer.encode('\n[')
            print(f'Length of chat tokens (chat tokens + answer must be below 4096): {len(input_tokens)}')
            input_len = len(input_tokens)
            input_tokens = torch.LongTensor([input_tokens]).to(device=device)

            out = model.generate(
                input_ids=input_tokens,
                do_sample=False,
                max_new_tokens=400,
                repetition_penalty=1.2,
                # eos_token_id=[32000, 28705],
            )
            answer = tokenizer.batch_decode(out[:, input_len:], skip_special_tokens=True)[0]
            if '```' in answer:
                answer = str.split(answer, '```')[0]
            if 'In English' in answer:
                answer = str.split(answer, 'In English')[0]
            print(f'answer: {answer}')
            answer_split = str.split(answer, '\n')
            chars_to_remove = ['[', ']', '"', ',', '.', '\'']
            #print(answer_split)
            for ans in answer_split:
                #cleaned = str.strip(ans)
                #cleaned = ans[4:]
                #for c in chars_to_remove:
                #    cleaned = str.replace(cleaned, c, '')
                #print(ans)
                if '"' in ans:
                    cleaned = str.split(ans, '"')[1]
                    #print(cleaned)
                    if not cleaned in answer_list and len(cleaned) > 0:
                        print(cleaned)
                        answer_list.append(cleaned)

        with open(f'{str.replace(name, ".mp3", "_keywords_cleaned.json")}', 'w', encoding='utf-8') as jsf:
            json.dump(answer_list, jsf, ensure_ascii=False, indent=4)

    return answer_list

def get_description_llm(keyword, text, model, tokenizer, device):
    with torch.inference_mode():
        user_text = f'I have the following document:\n\n{text}\n\nBased on the information above, give me a definition of the {keyword}.\nMake sure to only use definition that appear in the text.\nAnswer in Russian.'
        chat = [
            {"role": "system", "content": "The following is a conversation with an AI Large Language Model. The AI has been trained to answer questions, provide recommendations, and help with decision making. The AI follows user requests. The AI thinks outside the box."},
            {"role": "user", "content": user_text},
        ]
        input_tokens = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=False)
        input_len = len(input_tokens)
        input_tokens = torch.LongTensor([input_tokens]).to(device=device)
        out = model.generate(
            input_ids=input_tokens,
            do_sample=False,
            max_new_tokens=400,
            repetition_penalty=1.2,
        )
        answer = tokenizer.batch_decode(out[:, input_len:], skip_special_tokens=True)[0]
        print(f'answer for {keyword}: {answer}')
        return answer

def get_model_and_tokenizer():
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    # local cached file, non-docker run
    if os.path.exists('backend/docker/models/Mistral-7B-OpenOrca/'):
        repo_path = "backend/docker/models/Mistral-7B-OpenOrca/"
    # docker run
    elif os.path.exists('models/Mistral-7B-OpenOrca/'):
        repo_path = "models/Mistral-7B-OpenOrca/"
    # default to huggingface hub download
    else:
        repo_path = "Open-Orca/Mistral-7B-OpenOrca"

    print(f'Loading LLM from {repo_path}')
    model = AutoModelForCausalLM.from_pretrained(repo_path, device_map=device,
                                                 torch_dtype=torch.float16, use_flash_attention_2=True)
    tokenizer = AutoTokenizer.from_pretrained(repo_path)

    return model, tokenizer, device


if __name__ == "__main__":
    model, tokenizer, device = get_model_and_tokenizer()

    # mac
    if os.path.exists('./train_data/audiofiles/'):
        filepath = './train_data/audiofiles/'
    # win
    else:
        filepath = 'train_data/audiofiles/'

    for name in os.listdir(filepath):
        with open(str.replace(name, ".mp3", ".json"), 'r', encoding='utf-8') as jsf:
            text = json.load(jsf)

            get_key_llm(text, model, tokenizer, device)



