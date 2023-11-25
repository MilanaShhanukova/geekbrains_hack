import re
from typing import List, Dict


def extract_info(input_text, definitions):
    result = []
    start = input_text.find('*')
    
    while start != -1:
        end = input_text.find('*', start + 1)
        
        if end != -1:
            text_before = input_text[:start].strip()
            word = input_text[start + 1:end].strip()

            if word not in definitions:
                print(word)
            else:
                result.append({"text": text_before, "word": word, "definition": definitions[word]})

            input_text = input_text[end + 1:]
            start = input_text.find('*')
        else:
            break
    
    return result


def frame_stars_without_lemmat(final_text: str, keywords: List) -> str:
    marked_text = final_text

    for phrase in keywords:
        pattern = re.compile(r'\b{}\b'.format(re.escape(phrase)), re.IGNORECASE)
        
        marked_text = pattern.sub(lambda match: '*' + match.group(0) + '*', marked_text, count=1)
    return marked_text


def parse_file(text: str, definitions: Dict) -> List[Dict]:
    keywords = list(definitions.keys())
    marked_text = frame_stars_without_lemmat(text, keywords)

    text_with_defs = extract_info(marked_text, definitions)

    return text_with_defs