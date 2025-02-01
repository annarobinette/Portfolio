import csv

def clean_csv():
    # Read original file
    with open('/Users/anna/Documents/GitHub/Portfolio/projects/SewingPatternMarketDatabase/scraper/data/generated/patterns.csv', 'r', encoding='utf-8') as infile:
        content = infile.read()
        
        # Replace smart quotes and apostrophes with standard ones using Unicode escapes
        replacements = {
            '\u201c': '"',  # opening smart quote to standard quote
            '\u201d': '"',  # closing smart quote to standard quote
            '\u2018': "'",  # opening smart apostrophe to standard apostrophe
            '\u2019': "'",  # closing smart apostrophe to standard apostrophe
            '\u2026': '...' # ellipsis to periods
        }
        
        # Apply all replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Write cleaned content to a new file
        with open('/Users/anna/Documents/GitHub/Portfolio/projects/SewingPatternMarketDatabase/scraper/data/generated/patterns_cleaned.csv', 'w', encoding='utf-8', newline='') as outfile:
            # Process the cleaned content line by line
            lines = content.split('\n')
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
            
            # Write header
            header = next(csv.reader([lines[0]]))
            writer.writerow(header)
            
            # Process data rows
            reader = csv.reader(lines[1:])
            for row in reader:
                if row:  # Skip empty rows
                    # Clean each field
                    cleaned_row = [field.strip() for field in row]
                    writer.writerow(cleaned_row)

if __name__ == "__main__":
    clean_csv()