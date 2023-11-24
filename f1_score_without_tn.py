def calculate_f1_score(y_true, y_pred):
    true_positives = len(set(y_true) & set(y_pred))
    false_negatives = len(set(y_true) - set(y_pred))

    precision = true_positives / len(y_pred) if len(y_pred) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return f1_score

if __name__ == '__main__':
    y_true = ["c-sharp", "типы данных", 'среднее арифметическое', "структура данных", 'блок-схемы', 'циклы']
    y_pred = ["структура данных", "типы данных", "c-sharp", "массив", 'среднее арифметическое', 'блок-схемы', 'циклы', 'операторы сравнения', 'алгоритмы', 'базы данных']

    f1 = calculate_f1_score(y_true, y_pred)
    print("F1 Score без учета ложных срабатываний:", f1)
