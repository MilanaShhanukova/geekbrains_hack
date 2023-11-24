import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json


def get_key_llm(text, model, tokenizer, device="cuda:0"):
    with torch.inference_mode():
        answer_list = []
        description_dict = {}
        for part in range(0, len(text["text"]) // 6000 + 1):
            context = text["text"][part*6000:(part+1)*6000]
            user_text = f'I have the following document:\n\n{context}\n\nBased on the information above, extract the keywords that best describe the topic of the text.\nMake sure to only extract keywords that appear in the text.\nUse the following format separated by commas:\n<keywords>\nAnswer in Russian.'
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
            answer_list.append(str.strip(answer))

            for keyword in str.split(str.strip(answer), ','):
                description_dict[keyword] = get_description_llm(keyword, context, model, tokenizer)

        with open(f'{str.replace(name, ".mp3", "_keywords.json")}', 'w', encoding='utf-8') as jsf:
            json.dump(answer_list, jsf, ensure_ascii=False, indent=4)
        with open(f'{str.replace(name, ".mp3", "_descriptions.json")}', 'w', encoding='utf-8') as jsf:
            json.dump(description_dict, jsf, ensure_ascii=False, indent=4)
        
    return answer_list

def get_description_llm(keyword, text, model, tokenizer, device="cuda:0"):
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


if __name__ == "__main__":
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    model = AutoModelForCausalLM.from_pretrained('Open-Orca/Mistral-7B-OpenOrca', device_map=device,
                                                torch_dtype=torch.float16, use_flash_attention_2=True)
    tokenizer = AutoTokenizer.from_pretrained('Open-Orca/Mistral-7B-OpenOrca')

    if os.path.exists('./train_data/audiofiles/'):
        # mac
        filepath = './train_data/audiofiles/'
    else:
        # win
        filepath = 'train_data/audiofiles/'
    for name in os.listdir(filepath):
        with open(str.replace(name, ".mp3", ".json"), 'r', encoding='utf-8') as jsf:
            text = json.load(jsf)

            get_key_llm(text, model, tokenizer, device)



