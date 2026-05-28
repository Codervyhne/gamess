import json
import os

# Configuration variables
INPUT_FILE = "games.json"
OUTPUT_FILE = "games_cleaned.json"

def clean_games_data():
    if not os.path.exists(INPUT_FILE):
        print(f"ERR: Target file '{INPUT_FILE}' not found in current directory.")
        return

    print(f"System // Initializing parse of '{INPUT_FILE}'...")
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERR: Failed to parse valid JSON data. Details: {e}")
        return

    # Ensure we are handling a list array
    if not isinstance(raw_data, list):
        print("ERR: Expected JSON root structure to be an array list.")
        return

    cleaned_list = []
    skipped_cloud_count = 0

    for idx, entry in enumerate(raw_data):
        # Extract properties safely
        raw_category = entry.get("category")
        
        # Ensure category is a valid string before running string operations
        if isinstance(raw_category, str):
            category = raw_category.lower().strip()
        else:
            category = "browser"
        
        # Explicitly ignore any entries marked under cloud provider tags
        if category == "cloud":
            skipped_cloud_count += 1
            continue

        # Map explicitly to the high-utility parameters required
        cleaned_entry = {
            "name": entry.get("name", f"Untitled Game {idx}"),
            "url": entry.get("url", ""),
            "img": entry.get("img", ""),
            "category": category if category in ["browser", "emulator"] else "browser"
        }
        
        cleaned_list.append(cleaned_entry)

    # Write structural output with a clean, unbloated vertical layout
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(cleaned_list, f, indent=2, ensure_ascii=False)
        
        print("\n--- PROCESS COMPLETED ---")
        print(f"Entries Processed: {len(raw_data)}")
        print(f"Cloud Items Expelled: {skipped_cloud_count}")
        print(f"Cleaned Items Retained: {len(cleaned_list)}")
        print(f"Success. View structured results inside '{OUTPUT_FILE}'.")
        
    except Exception as e:
        print(f"ERR: Write state failure. Details: {e}")

if __name__ == "__main__":
    clean_games_data()