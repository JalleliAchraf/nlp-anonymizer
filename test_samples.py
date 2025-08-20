#!/usr/bin/env python3
"""
Test script to run anonymization on sample texts from data/sample_texts.txt
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from models.ner_model import full_anonymizer

def test_sample_texts():
    """Read sample texts and test anonymization"""
    
    # Read sample texts
    sample_file = os.path.join(os.path.dirname(__file__), 'data', 'sample_texts.txt')
    
    try:
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Could not find {sample_file}")
        return
    
    # Split by double newlines (paragraph breaks)
    texts = [text.strip() for text in content.split('\n\n') if text.strip()]
    
    print("=" * 80)
    print("ANONYMIZATION TEST RESULTS")
    print("=" * 80)
    
    for i, text in enumerate(texts, 1):
        print(f"\n--- Sample Text #{i} ---")
        print("ORIGINAL:")
        print(text)
        print("\nANONYMIZED:")
        
        try:
            anonymized = full_anonymizer(text)
            print(anonymized)
            
            # Count anonymized entities
            entities = ['[PER]', '[LOC]', '[ORG]', '[EMAIL]', '[PHONE]', '[CARD]', '[DATE]']
            counts = {entity: anonymized.count(entity) for entity in entities}
            total_entities = sum(counts.values())
            
            print(f"\nEntities found: {total_entities} total")
            for entity, count in counts.items():
                if count > 0:
                    print(f"  {entity}: {count}")
                    
        except Exception as e:
            print(f"ERROR: {e}")
        
        print("-" * 60)
    
    print(f"\nTested {len(texts)} sample texts")
    print("=" * 80)

if __name__ == "__main__":
    test_sample_texts()
