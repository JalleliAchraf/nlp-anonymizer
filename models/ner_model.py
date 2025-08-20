# ner_model.py
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import re

# Load NER model
MODEL_NAME = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

def ner_anonymize(text):
    """Anonymize entities detected by the NER model: PER, LOC, ORG."""
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    predicted_indices = torch.argmax(outputs.logits, dim=-1)
    predicted_tags = [model.config.id2label[idx.item()] for idx in predicted_indices[0]]

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    # Remove special tokens
    filtered_tokens = [t for t in tokens if t not in ["[CLS]", "[SEP]"]]
    filtered_tags = predicted_tags[1:-1]

    # Merge WordPiece tokens
    merged_tokens = []
    merged_tags = []
    for t, tag in zip(filtered_tokens, filtered_tags):
        if t.startswith("##"):
            merged_tokens[-1] += t[2:]
        else:
            merged_tokens.append(t)
            merged_tags.append(tag)

    # Replace NER entities with [TAG]
    anonymized_tokens = []
    i = 0
    while i < len(merged_tokens):
        tag = merged_tags[i]
        if tag.startswith("B-"):
            entity_type = tag[2:]
            # Consume subsequent I- tokens
            i += 1
            while i < len(merged_tokens) and merged_tags[i].startswith("I-"):
                i += 1
            anonymized_tokens.append(f"[{entity_type}]")
        else:
            anonymized_tokens.append(merged_tokens[i])
            i += 1

    return " ".join(anonymized_tokens)

def regex_anonymize(text):
    """Anonymize emails, phone numbers, credit cards, and dates using regex."""
    # Credit cards first (13-16 digits, possibly spaced/dashed) - more specific than phone
    card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    text = re.sub(card_pattern, '[CARD]', text)
    
    # Emails (handles spaces around dots and @)
    email_pattern = r'\b[\w\.-]+\s*@\s*[\w\.-]+\s*\.\s*\w+\b'
    text = re.sub(email_pattern, '[EMAIL]', text)

    # Phone numbers (various formats with flexible spacing) 
    phone_pattern = r'(?:\+?\s*1\s*)?(?:\(\s*\d{3}\s*\)|\d{3})\s*[\-\s]*\s*\d{3}\s*[\-\s]*\s*\d{4}'
    text = re.sub(phone_pattern, '[PHONE]', text)

    # Dates (formats like 08 / 15 / 2025 or 11 / 24)
    date_pattern = r'\b\d{1,2}\s*/\s*\d{1,2}(?:\s*/\s*\d{2,4})?\b'
    text = re.sub(date_pattern, '[DATE]', text)

    return text

def full_anonymizer(text):
    """Run NER anonymization first, then regex anonymization."""
    text = ner_anonymize(text)
    text = regex_anonymize(text)
    return text

if __name__ == "__main__":
    # Example usage with neutral data
    example_text = (
        "Dr. John Doe from Springfield called +1 234 567 8900 "
        "to confirm her appointment on 08 / 15 / 2025. "
        "Send the invoice to example.user@company.com. "
        "Her card 1234 5678 9012 3456 expires 11 / 24."
    )
    anonymized = full_anonymizer(example_text)
    print("Anonymized:", anonymized)
