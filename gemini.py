import requests
import google.generativeai as genai
from bs4 import BeautifulSoup

try:
    genai.configure(api_key="AIzaSyCoI4k-dZ-wjtk_iV741UIZRBjrarD5a88")
except KeyError:
    print("="*50)
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
    print("Please set the environment variable to run this script.")
    print("="*50)
    exit()

MODEL_NAME = "gemini-2.5-flash"

URL_TO_ANALYZE = "https://en.wikipedia.org/wiki/Artificial_intelligence"
# URL_TO_ANALYZE = "https://www.bbc.com/news/technology"
# URL_TO_ANALYZE = "https://edition.cnn.com/business"

SUMMARY_FILENAME = "summary_output.txt"


def fetch_and_clean_webpage(url: str) -> str:
    print(f"Step 1: Fetching content from {url}...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch URL: {e}")
        return ""

    print("Step 2: Cleaning HTML...")
    soup = BeautifulSoup(response.text, 'html.parser')

    tags_to_remove = [
        'script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 
        '.navbar', '.sidebar', '.ad-slot', '.advertisement', '.noprint',
        '.mw-jump-link'
    ]
    
    for selector in tags_to_remove:
        for tag in soup.select(selector):
            tag.decompose()

    main_content = soup.find('div', id='bodyContent')
    if not main_content:
        main_content = soup.find('body')
        if not main_content:
            print("Error: Could not find main content/body of the webpage.")
            return ""

    text = main_content.get_text(separator=' ', strip=True)
    cleaned_text = ' '.join(text.split())
    
    print(f"Step 3: Extracted {len(cleaned_text)} characters of text.")
    
    max_chars = 150000
    if len(cleaned_text) > max_chars:
        print(f"Warning: Text too long, truncating to {max_chars} characters.")
        cleaned_text = cleaned_text[:max_chars]

    return cleaned_text

def analyze_text_with_gemini(text: str, url: str) -> str:
    print(f"Step 4: Connecting to Gemini ({MODEL_NAME})...")
    
    prompt = f"""
You are an expert strategic analyst. Your task is to analyze the provided text content from the webpage: {url}

Focus your analysis on the societal, ethical, and business implications of the topics presented.

Your response MUST strictly follow this format:
1.  **Summary:** Provide exactly 5 concise bullet points. Each bullet point must start with the '•' character.
2.  **Insight:** After the summary, provide a single-line analytical insight. This insight should interpret the *overall trend* or *underlying theme* of the content, not just restate a fact.

Provide *only* the requested text in the specified format. Do not add any other text before or after.

Here is the exact format to follow:
Summary:
• <bullet point 1>
• <bullet point 2>
• <bullet point 3>
• <bullet point 4>
• <bullet point 5>
Insight:
<Your single-line insight here>

Here is the webpage text:
---
{text}
---
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error during Gemini API call: {e}"

def save_output_to_file(text_content: str, filename: str):
    print(f"\nStep 6: Saving output to {filename}...")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"Successfully saved analysis to {filename}")
    except IOError as e:
        print(f"Error: Failed to write to file: {e}")

def main():
    cleaned_text = fetch_and_clean_webpage(URL_TO_ANALYZE)
    
    if cleaned_text:
        analysis = analyze_text_with_gemini(cleaned_text, URL_TO_ANALYZE)
        
        if analysis and not analysis.startswith("Error"):
            print("\nStep 5: Analysis Complete.")
            print("\n" + "="*40 + " CONSOLE OUTPUT " + "="*40 + "\n")
            print(analysis)
            print("\n" + "="*96)
            save_output_to_file(analysis, SUMMARY_FILENAME)
        else:
            print(f"\nAnalysis failed:\n{analysis}")

if __name__ == "__main__":
    main()