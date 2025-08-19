"""
Script to process discussion forum threads CSV file, remove duplicates, and extract title/body data.

Input data sources: recent_threads_Aug2025.csv
Output destinations: threads_cleaned.json
Dependencies: csv, json
Key exports: clean_and_extract_threads()
Side effects: Creates JSON file, reads CSV file
"""

import csv
import json
import hashlib

def clean_and_extract_threads():
    print("Reading CSV file...")
    
    threads = []
    seen_bodies = set()
    duplicates_found = 0
    
    with open('recent_threads_Aug2025.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            thread_title = row['thread_title']
            thread_body = row['thread_body']
            
            # Skip rows with empty title or body
            if not thread_title or not thread_body:
                continue
            
            # Create a hash of the thread body to check for duplicates
            body_hash = hashlib.md5(thread_body.encode('utf-8')).hexdigest()
            
            if body_hash not in seen_bodies:
                seen_bodies.add(body_hash)
                threads.append({
                    'thread_title': thread_title,
                    'thread_body': thread_body
                })
            else:
                duplicates_found += 1
    
    print(f"Total threads processed: {len(threads) + duplicates_found}")
    print(f"Duplicates removed: {duplicates_found}")
    print(f"Unique threads extracted: {len(threads)}")
    
    # Create JSON output
    output_data = {
        'threads': threads,
        'metadata': {
            'total_unique_threads': len(threads),
            'duplicates_removed': duplicates_found
        }
    }
    
    # Write to JSON file
    with open('threads_cleaned.json', 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, indent=2, ensure_ascii=False)
    
    print("JSON file created: threads_cleaned.json")
    
    return output_data

if __name__ == "__main__":
    result = clean_and_extract_threads()