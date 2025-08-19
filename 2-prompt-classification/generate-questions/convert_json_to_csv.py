"""
Converts generated prompt classification questions JSON file to CSV format with specified columns.

Input data sources: generated_prompt_classification_questions.json (same folder)
Output destinations: generated_prompt_classification_questions.csv (same folder)
Dependencies: json, csv (standard library)
Key exports: convert_json_to_csv()
Side effects: Creates CSV file
"""

import json
import csv
from pathlib import Path


def convert_json_to_csv():
    """Convert the JSON file to CSV format with question, category, instruction, examples columns."""
    
    # Define file paths (script is in generate-questions folder)
    json_file = Path("generated_prompt_classification_questions.json")
    csv_file = Path("generated_prompt_classification_questions.csv")
    
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
        category_info = question_data.get('category_info', {})
        
        # Extract category information
        category = category_info.get('category', '')
        instruction = category_info.get('instruction', '')
        examples = category_info.get('examples', [])
        
        # Join examples with " | " separator
        examples_text = " | ".join(examples) if examples else ""
        
        # Add row to CSV data
        csv_rows.append({
            'question': question_text,
            'category': category,
            'instruction': instruction,
            'examples': examples_text
        })
        
        # Progress indicator
        if i % 10 == 0:
            print(f"Processed {i}/{len(questions)} questions...")
    
    # Write CSV file
    print(f"Writing {len(csv_rows)} rows to CSV file: {csv_file}")
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['question', 'category', 'instruction', 'examples']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        writer.writerows(csv_rows)
    
    print(f"✅ Successfully converted {len(questions)} questions to CSV with {len(csv_rows)} total rows")
    print(f"📊 Output file: {csv_file}")
    
    return csv_file


if __name__ == "__main__":
    try:
        output_file = convert_json_to_csv()
        print(f"\n🎉 Conversion complete! CSV file created: {output_file}")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        raise