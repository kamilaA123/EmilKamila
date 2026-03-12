import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
import emoji
import numpy as np

MAX_LENGTH = 32
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
NUM_LABELS = 4

class RussianTextClassifier(nn.Module):
    def __init__(self, num_labels):
        super(RussianTextClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[1]
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits

def remove_emoji(text):
    return emoji.demojize(text)

def preprocess_text(text):
    text = remove_emoji(text)
    return text

def load_tokenizer():
    return BertTokenizer.from_pretrained('bert-base-multilingual-cased')

def load_model(model_path):
    model = RussianTextClassifier(NUM_LABELS).to(DEVICE)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model.eval()
    return model

def predict_comment(comment, model, tokenizer):
    comment = preprocess_text(comment)

    encoded_dict = tokenizer(
        comment,
        add_special_tokens=True,
        max_length=MAX_LENGTH,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt',
    )

    input_id = encoded_dict['input_ids'].to(DEVICE)
    attention_mask = encoded_dict['attention_mask'].to(DEVICE)

    with torch.no_grad():
        output = model(input_id, attention_mask)
        probabilities = torch.sigmoid(output).cpu().numpy()

    return probabilities[0]

def get_label_mapping():
    return {
        0: "__label__INSULT",
        1: "__label__NORMAL",
        2: "__label__THREAT",
        3: "__label__OBSCENITY"
    }

def get_readable_labels():
    return {
        "__label__NORMAL": "Норма",
        "__label__INSULT": "Оскорбление или нецензурная брань",
        "__label__THREAT": "Грозное преднамерение",
        "__label__OBSCENITY": "Вульгарность"
    }

def diagnose_model(model, tokenizer):
    test_comments = {
        "нейтральный": ["молодец", "хороший день", "спасибо"],
        "оскорбительный": ["сука тупорылая", "козел", "идиот"],
        "угроза": ["убью", "зарежу", "посажу на кол"],
        "вульгарный": ["трахнуть", "задница", "писька"]
    }

    print("=" * 60)
    print("ДИАГНОСТИКА МОДЕЛИ")
    print("=" * 60)

    for category, examples in test_comments.items():
        print(f"\n📌 Категория: {category.upper()}")
        for comment in examples:
            probs = predict_comment(comment, model, tokenizer)
            mapping = get_label_mapping()
            readable = get_readable_labels()

            print(f"\n  Текст: '{comment}'")
            print(f"  Сырые вероятности: {['{:.3f}'.format(p) for p in probs]}")

            predicted_indices = [i for i, p in enumerate(probs) if p > 0.5]
            if predicted_indices:
                for idx in predicted_indices:
                    mapped_label = mapping[idx]
                    print(f"  ➡ Предсказано: {readable.get(mapped_label, 'Unknown')} (индекс {idx} -> {mapped_label})")
            else:
                max_idx = np.argmax(probs)
                mapped_label = mapping[max_idx]
                print(f"  ➡ Максимальная вероятность: {readable.get(mapped_label, 'Unknown')} ({probs[max_idx]:.3f})")

    print("\n" + "=" * 60)

def format_results(probabilities):
    mapping = get_label_mapping()
    readable = get_readable_labels()

    results = []
    print("\n=== Сырые вероятности (индексы модели) ===")
    for i, prob in enumerate(probabilities):
        prob_percent = prob * 100
        raw_label = mapping[i]
        readable_label = readable.get(raw_label, "Unknown")
        print(f"  Индекс {i} -> {raw_label}: {prob_percent:.2f}%")

        results.append({
            'model_index': i,
            'raw_label': raw_label,
            'label': readable_label,
            'probability': prob_percent,
            'is_detected': prob > 0.5
        })

    results.sort(key=lambda x: x['probability'], reverse=True)

    return results

def get_overall_verdict(results):
    toxic_categories = []

    for r in results:
        if r['is_detected'] and r['raw_label'] != "__label__NORMAL":
            toxic_categories.append(r['label'])

    if not toxic_categories:
        return "✅ Норма (нетоксичный комментарий)"
    else:
        return f"⚠️ Обнаружена токсичность: {', '.join(toxic_categories)}"