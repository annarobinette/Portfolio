import csv

def fix_patterns_csv():
    # First read garment types to get valid categories
    with open('/Users/anna/Documents/GitHub/Portfolio/projects/SewingPatternMarketDatabase/scraper/data/generated/garment_types.csv', 'r', encoding='utf-8') as f:
        garment_types = list(csv.DictReader(f))
        valid_categories = set(gt['category'] for gt in garment_types)
        # Create lookup for garment type categories
        garment_type_lookup = {int(gt['garment_type_id']): gt['category'] 
                             for gt in garment_types}
    
    # Read and fix patterns
    fixed_rows = []
    with open('/Users/anna/Documents/GitHub/Portfolio/projects/SewingPatternMarketDatabase/scraper/data/generated/patterns_cleaned.csv', 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Convert garment_type_id to int for lookup
            try:
                gtid = int(row['garment_type_id'])
                if gtid in garment_type_lookup:
                    # Update type to match category from garment types
                    row['type'] = garment_type_lookup[gtid]
            except (ValueError, KeyError):
                print(f"Warning: Invalid garment_type_id {row['garment_type_id']}")
            
            # Fix pattern_includes if it doesn't start with Instructions
            if not str(row['pattern_includes']).startswith('Instructions'):
                print(f"Fixing pattern_includes for {row['pattern_name']}")
                row['pattern_includes'] = 'Instructions; ' + str(row['pattern_includes'])
            
            fixed_rows.append(row)
    
    # Write fixed data
    with open('/Users/anna/Documents/GitHub/Portfolio/projects/SewingPatternMarketDatabase/scraper/data/generated/patterns_fixed.csv', 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fixed_rows[0].keys())
        writer.writeheader()
        writer.writerows(fixed_rows)
        print(f"\nProcessed {len(fixed_rows)} rows")

if __name__ == "__main__":
    fix_patterns_csv()
