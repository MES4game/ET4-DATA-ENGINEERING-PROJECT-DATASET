"""
main module
===========

Module to run the data pipeline and export to JSON

Functions
---------
- `main`
"""


import json
import src


def main() -> None:
    """
    Main function to collect, format and export data to JSON
    """
    print("Starting data collection...")
    
    # Get combined data
    data: list[src.models.Data] = src.getData()
    
    print(f"Collected {len(data)} game entries")
    
    # Convert to JSON-serializable format
    json_data = [d.to_dict() for d in data]
    
    # Export to JSON file
    output_file = "dataset.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"Dataset exported: {len(json_data)} entries saved to {output_file}")
    
    # Display some statistics
    with_notes = sum(1 for d in data if d.note is not None)
    with_editors = sum(1 for d in data if d.editor is not None)
    
    print(f"Statistics:")
    print(f"   - Games with ratings: {with_notes}/{len(data)}")
    print(f"   - Games with publisher data: {with_editors}/{len(data)}")


if __name__ == "__main__":
    main()
