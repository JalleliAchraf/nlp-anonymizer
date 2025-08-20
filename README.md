# NLP Anonymizer

Anonymize sensitive information in text using AI and regex patterns.

## What it does
- Names, locations, organizations
- Emails, phone numbers, credit cards, dates

## Install
```bash
pip install -r requirements.txt
```

## Usage
```python
from models.ner_model import full_anonymizer

text = "Dr. John Doe called +1 234 567 8900"
result = full_anonymizer(text)
print(result)  # "[PER] called [PHONE]"
```

## Run example
```bash
python models/ner_model.py
```

## Test with samples
```bash
python test_samples.py
```

## Predicted vs actual comparison
```bash
python predicted_vs_actual.py
```

## Run tests
```bash
python test_ner_model.py
```