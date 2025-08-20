import sys
import os
# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from models.ner_model import regex_anonymize, ner_anonymize, full_anonymizer

def test_regex_anonymize_email():
    """Test email anonymization"""
    text = "Contact me at john.doe@example.com for details"
    result = regex_anonymize(text)
    assert "[EMAIL]" in result
    assert "john.doe@example.com" not in result

def test_regex_anonymize_phone():
    """Test phone number anonymization"""
    text = "Call me at +1 234 567 8900 today"
    result = regex_anonymize(text)
    assert "[PHONE]" in result
    assert "234 567 8900" not in result

def test_regex_anonymize_credit_card():
    """Test credit card anonymization"""
    text = "My card number is 1234 5678 9012 3456"
    result = regex_anonymize(text)
    assert "[CARD]" in result
    assert "1234 5678 9012 3456" not in result

def test_regex_anonymize_date():
    """Test date anonymization"""
    text = "The meeting is on 08/15/2025 and expires 11/24"
    result = regex_anonymize(text)
    assert result.count("[DATE]") == 2
    assert "08/15/2025" not in result

def test_ner_anonymize_person():
    """Test NER person name anonymization"""
    text = "Dr. John Smith visited the hospital"
    result = ner_anonymize(text)
    # Should contain a person entity (though exact detection may vary)
    assert "[PER]" in result or "John Smith" not in result

def test_full_anonymizer_combined():
    """Test full anonymization pipeline"""
    text = "Dr. John Doe from Springfield called +1 234 567 8900 and sent email to test@example.com"
    result = full_anonymizer(text)
    
    # Should anonymize phone and email
    assert "[PHONE]" in result
    assert "[EMAIL]" in result
    assert "test@example.com" not in result
    assert "+1 234 567 8900" not in result

def test_empty_text():
    """Test with empty text"""
    result = full_anonymizer("")
    assert result == ""

def test_no_sensitive_data():
    """Test with text containing no sensitive information"""
    text = "This is a simple sentence with no sensitive data."
    result = full_anonymizer(text)
    # Should return similar text (may have slight tokenization differences)
    assert len(result) > 0

if __name__ == "__main__":
    # Run all tests
    test_functions = [
        test_regex_anonymize_email,
        test_regex_anonymize_phone,
        test_regex_anonymize_credit_card,
        test_regex_anonymize_date,
        test_ner_anonymize_person,
        test_full_anonymizer_combined,
        test_empty_text,
        test_no_sensitive_data
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed! 🎉")
