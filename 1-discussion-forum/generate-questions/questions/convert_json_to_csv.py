"""
Converts generated discussion questions JSON file to CSV format with specified columns.

Input data sources: generated_discussion_questions.json (same folder)
Output destinations: generated_discussion_questions.csv (same folder)  
Dependencies: json, csv (standard library)
Key exports: convert_json_to_csv()
Side effects: Creates CSV file
"""

import json
import csv
import os
from pathlib import Path


def convert_json_to_csv():
    """Convert the JSON file to CSV format with Question and separate columns for each dimension type."""
    
    # Define file paths (script is now in questions folder)
    json_file = Path("generated_discussion_questions.json")
    csv_file = Path("generated_discussion_questions.csv")
    
    # Check if JSON file exists
    if not json_file.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")
    
    # Read JSON data
    print(f"Reading JSON data from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    print(f"Found {len(questions)} questions to process")
    
    # Prepare CSV data
    csv_rows = []
    
    for i, question_data in enumerate(questions, 1):
        question_text = question_data.get('question', '')
        
        # Extract dimension names for each type
        intent_dim = question_data.get('intent_dimension', {}).get('dimension', '')
        specificity_dim = question_data.get('specificity_dimension', {}).get('dimension', '')
        domain_dim = question_data.get('domain_dimension', {}).get('dimension', '')
        persona_dim = question_data.get('persona_dimension', {}).get('dimension', '')
        
        # Add row to CSV data with separate columns for each dimension
        csv_rows.append({
            'Question': question_text,
            'Intent_Dimension': intent_dim,
            'Specificity_Dimension': specificity_dim,
            'Domain_Dimension': domain_dim,
            'Persona_Dimension': persona_dim
        })
        
        # Progress indicator
        if i % 10 == 0:
            print(f"Processed {i}/{len(questions)} questions...")
    
    # Write CSV file
    print(f"Writing {len(csv_rows)} rows to CSV file: {csv_file}")
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Question', 'Intent_Dimension', 'Specificity_Dimension', 'Domain_Dimension', 'Persona_Dimension']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        writer.writerows(csv_rows)
    
    print(f"✅ Successfully converted {len(questions)} questions to CSV with {len(csv_rows)} total rows")
    print(f"📋 Each row contains: Question + 4 dimension columns (Intent, Specificity, Domain, Persona)")
    print(f"📊 Output file: {csv_file}")
    
    return csv_file


if __name__ == "__main__":
    try:
        output_file = convert_json_to_csv()
        print(f"\n🎉 Conversion complete! CSV file created: {output_file}")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        raise