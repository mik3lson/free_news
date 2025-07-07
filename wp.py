import json
import re
import sys
from bs4 import BeautifulSoup

def extract_wp_content(html_file):
    """Extract Washington Post article content from HTML dump"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Look for the JSON content in the HTML
        # Washington Post stores article content in JSON format with Unicode escapes
        json_pattern = r'"content":"([^"]*)"'
        matches = re.findall(json_pattern, html_content)
        
        if not matches:
            print("No content found in HTML dump")
            return ""
        
        # Extract and decode the content
        extracted_text = []
        print(f"Found {len(matches)} content matches")
        
        for i, match in enumerate(matches):
            if match.strip():
                try:
                    # More robust cleaning of escape sequences
                    # First, handle the problematic backslashes at the end
                    cleaned_match = match
                    
                    # Remove trailing backslashes that cause issues
                    while cleaned_match.endswith('\\'):
                        cleaned_match = cleaned_match[:-1]
                    
                    # Handle common escape sequences
                    cleaned_match = cleaned_match.replace('\\"', '"')
                    cleaned_match = cleaned_match.replace('\\\\', '\\')
                    cleaned_match = cleaned_match.replace('\\/', '/')
                    
                    # Now try to decode Unicode sequences
                    try:
                        decoded = cleaned_match.encode('utf-8').decode('unicode_escape')
                    except UnicodeDecodeError:
                        # If that fails, try a more conservative approach
                        decoded = cleaned_match
                    
                    # Remove HTML tags
                    clean_text = re.sub(r'<[^>]+>', '', decoded)
                    
                    # Clean up encoding issues - fix quotes and apostrophes
                    # â€œ = left double quote (")
                    # â€ = right double quote (")
                    # â€™ = right single quote (')
                    # â€" = em dash (—)
                    clean_text = clean_text.replace('â€œ', '"')
                    clean_text = clean_text.replace('â€', '"')
                    clean_text = clean_text.replace('â€™', "'")
                    clean_text = clean_text.replace('â€"', '—')
                    
                    # Remove any remaining â characters that might be other encoding issues
                    clean_text = clean_text.replace('â', '')
                    clean_text = clean_text.replace('\\', '')  # Remove any remaining backslashes
                    
                    # Only keep substantial content (more than 20 characters)
                    if clean_text.strip() and len(clean_text.strip()) > 20:
                        extracted_text.append(clean_text.strip())
                        print(f"Match {i+1}: {clean_text.strip()[:100]}...")
                        
                except Exception as decode_error:
                    print(f"Error decoding content {i+1}: {decode_error}")
                    continue
        
        # Join all content pieces
        full_text = '\n\n'.join(extracted_text)
        
        return full_text
        
    except Exception as e:
        print(f"Error extracting Washington Post content: {e}")
        return ""

def main():
    if len(sys.argv) != 2:
        print('Usage: python wp.py <html_file>')
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    print(f"Extracting Washington Post content from {html_file}...")
    content = extract_wp_content(html_file)
    
    if content:
        with open('news.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Washington Post content written to news.txt ({len(content)} characters)")
    else:
        print("No content extracted")

if __name__ == '__main__':
    main() 