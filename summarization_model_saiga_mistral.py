# 1. Download model
# wget https://huggingface.co/IlyaGusev/saiga2_7b_gguf/resolve/main/model-q4_K.gguf
# wget https://raw.githubusercontent.com/IlyaGusev/rulm/master/self_instruct/src/interact_llamacpp.py

import fire
from llama_cpp import Llama
from docx import Document


SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."
SYSTEM_TOKEN = 1587
USER_TOKEN = 4096
BOT_TOKEN = 12435
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}

def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens

def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)

def interact(
    model_path,
    user_message,
    output_file_path,
    n_ctx=4096,
    top_k=30,
    top_p=0.9,
    temperature=0.2,
    repeat_penalty=1.1
):
    model = Llama(
        model_path=model_path,
        n_gpu_layers=100,
        n_ctx=n_ctx,
        n_parts=1,
    )

    system_tokens = get_system_tokens(model)
    tokens = system_tokens
    model.eval(tokens)


    message_tokens = get_message_tokens(model=model, role="user", content=user_message)
    role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    tokens += message_tokens + role_tokens
    # print(tokens)
    full_prompt = model.detokenize(tokens)
    # print(model.tokenize(full_prompt))

    generator = model.generate(
        tokens,
        top_k=top_k,
        top_p=top_p,
        temp=temperature,
        repeat_penalty=repeat_penalty
    )
    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        if token == model.token_eos():
            tokens.append('\n')
            break
        print(token_str, end="", flush=True)
        with open(output_file_path, 'a', encoding='utf-8') as file:
            file.write(f'{token_str}')


