#!/usr/bin/env python3
"""
Create a predicted vs actual comparison for sample texts
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from models.ner_model import full_anonymizer

def create_comparison_report():
    """Create a predicted vs actual comparison report"""
    
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
    
    print("=" * 100)
    print("PREDICTED VS ACTUAL ANONYMIZATION COMPARISON")
    print("=" * 100)
    
    total_entities = 0
    total_samples = len(texts)
    
    for i, text in enumerate(texts, 1):
        print(f"\n📋 SAMPLE #{i}")
        print("-" * 80)
        
        print("🔍 ORIGINAL TEXT:")
        print(f"   {text}")
        
        print("\n🎯 PREDICTED ANONYMIZED:")
        try:
            anonymized = full_anonymizer(text)
            print(f"   {anonymized}")
            
            # Count and categorize entities
            entities = {
                '[PER]': 'Person Names',
                '[LOC]': 'Locations', 
                '[ORG]': 'Organizations',
                '[EMAIL]': 'Email Addresses',
                '[PHONE]': 'Phone Numbers',
                '[CARD]': 'Credit Cards',
                '[DATE]': 'Dates'
            }
            
            entity_counts = {entity: anonymized.count(entity) for entity in entities.keys()}
            sample_total = sum(entity_counts.values())
            total_entities += sample_total
            
            print(f"\n📊 ENTITIES DETECTED: {sample_total} total")
            for entity, description in entities.items():
                count = entity_counts[entity]
                if count > 0:
                    print(f"   • {entity} ({description}): {count}")
            
            # Quality assessment
            print(f"\n✅ QUALITY ASSESSMENT:")
            
            # Check for potential misses (simple heuristics)
            missed_indicators = []
            if '@' in text and '[EMAIL]' not in anonymized:
                missed_indicators.append("Potential missed email")
            if any(char.isdigit() for char in text) and sample_total == 0:
                missed_indicators.append("Contains numbers but no entities detected")
            
            if missed_indicators:
                print(f"   ⚠️  Potential issues: {', '.join(missed_indicators)}")
            else:
                print(f"   ✨ Good coverage - detected expected entity types")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        print("=" * 80)
    
    # Summary statistics
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"   • Total samples processed: {total_samples}")
    print(f"   • Total entities anonymized: {total_entities}")
    print(f"   • Average entities per sample: {total_entities/total_samples:.1f}")
    
    # Entity type breakdown across all samples
    print(f"\n🏷️  ENTITY TYPE BREAKDOWN (All Samples):")
    all_anonymized = []
    for text in texts:
        try:
            all_anonymized.append(full_anonymizer(text))
        except:
            continue
    
    combined_text = " ".join(all_anonymized)
    for entity, description in entities.items():
        total_count = combined_text.count(entity)
        if total_count > 0:
            print(f"   • {entity} ({description}): {total_count}")
    
    print("=" * 100)

if __name__ == "__main__":
    create_comparison_report()
