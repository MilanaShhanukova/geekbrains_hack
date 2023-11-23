import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

model = AutoModelForCausalLM.from_pretrained('Open-Orca/Mistral-7B-OpenOrca', device_map='cuda:0', torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained('Open-Orca/Mistral-7B-OpenOrca')

with torch.inference_mode():
    with open('audio1.json', 'r', encoding='utf-8') as jsf:
        text = json.load(jsf)

    user_text = f'I have the following document:\n\n{text["text"][0:8000]}\n\nBased on the information above, extract the keywords that best describe the topic of the text.\nMake sure to only extract keywords that appear in the text.\nUse the following format separated by commas:\n<keywords>\nAnswer in Russian.'
    chat = [
        {"role": "system", "content": "The following is a conversation with an AI Large Language Model. The AI has been trained to answer questions, provide recommendations, and help with decision making. The AI follows user requests. The AI thinks outside the box."},
        {"role": "user", "content": user_text},
    ]

    input_tokens = tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=False)
    print(f'len chat tokens (chat tokens + answer must be below 4096): {len(input_tokens)}')
    input_tokens = torch.LongTensor([input_tokens]).to(device=DEVICE)

    out = model.generate(
        input_ids=input_tokens,
        do_sample=False,
        max_new_tokens=400,
        repetition_penalty=1.2,
    )
    print(out.shape)
    answer = tokenizer.batch_decode(out, skip_special_tokens=True)[0]
    print(answer)