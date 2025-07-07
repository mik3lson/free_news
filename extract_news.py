import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
except ImportError:
    service = None  # User must have chromedriver in PATH

def setup_driver(use_existing_session=False):
    """Setup Chrome driver with options to avoid detection"""
    options = Options()
    
    if use_existing_session:
        # Connect to existing Chrome session
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    else:
        # Headless mode with anti-detection options
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    
    # Anti-detection options
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Speed optimizations
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')  # Faster loading
    options.add_argument('--disable-css')  # Disable CSS for faster loading
    options.add_argument('--disable-fonts')  # Disable font loading
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-ipc-flooding-protection')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    
    # Page load strategy - eager (don't wait for all resources)
    options.page_load_strategy = 'eager'
    
    if service:
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Set timeouts
    driver.set_page_load_timeout(10)  # 10 seconds max for page load
    driver.implicitly_wait(2)  # 2 seconds for element finding
    
    return driver

def extract_article_content(driver, url):
    """Extract article text and HTML using various selectors"""
    try:
        print("Loading page...")
        driver.get(url)
        
        # Quick check for basic content - don't wait too long
        time.sleep(1)
        
        # Get the full page HTML immediately
        full_html = driver.page_source
        
        # Try to extract content quickly with multiple strategies
        text = ""
        article_html = ""
        
        # Strategy 1: Quick check for article tags
        try:
            articles = driver.find_elements(By.TAG_NAME, 'article')
            if articles:
                largest_article = max(articles, key=lambda x: len(x.text))
                if len(largest_article.text) > 200:  # Must have substantial content
                    text = largest_article.text
                    article_html = largest_article.get_attribute('outerHTML')
                    print("Found article content via <article> tag")
        except Exception:
            pass
        
        # Strategy 2: Check for common content selectors
        if not text or len(text.strip()) < 200:
            selectors = [
                '[class*="article"]',
                '[class*="content"]',
                '[class*="story"]',
                '[class*="post"]',
                'main',
                '.entry-content',
                '.post-content',
                '.article-content',
                '.story-content'
            ]
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        largest_element = max(elements, key=lambda x: len(x.text))
                        if len(largest_element.text) > len(text) and len(largest_element.text) > 200:
                            text = largest_element.text
                            article_html = largest_element.get_attribute('outerHTML')
                            print(f"Found content via selector: {selector}")
                            break
                except Exception:
                    continue
        
        # Strategy 3: Get all paragraphs as fallback
        if not text or len(text.strip()) < 200:
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, 'p')
                if paragraphs:
                    # Filter out short paragraphs (likely navigation/menu items)
                    long_paragraphs = [p.text.strip() for p in paragraphs if len(p.text.strip()) > 50]
                    if long_paragraphs:
                        text = '\n\n'.join(long_paragraphs)
                        article_html = '\n'.join([p.get_attribute('outerHTML') for p in paragraphs if len(p.text.strip()) > 50])
                        print("Extracted content from paragraphs")
            except Exception:
                pass
        
        return text.strip(), article_html, full_html
        
    except Exception as e:
        print(f"Error extracting content: {e}")
        return "", "", ""

def main():
    if len(sys.argv) < 2:
        print('Usage: python extract_news.py <news_url> [--use-existing-session] [-wp]')
        print('To use existing Chrome session, first start Chrome with:')
        print('chrome --remote-debugging-port=9222')
        print('Use -wp flag for Washington Post articles')
        sys.exit(1)
    
    url = sys.argv[1]
    use_existing_session = '--use-existing-session' in sys.argv
    is_washington_post = '-wp' in sys.argv
    
    if use_existing_session:
        print("Connecting to existing Chrome session...")
    else:
        print("Starting new Chrome session...")
    
    try:
        driver = setup_driver(use_existing_session)
        print(f"Extracting content from: {url}")
        
        text, article_html, full_html = extract_article_content(driver, url)
        
        if not text:
            print("Failed to extract article text.")
            sys.exit(1)
        
        # Write text to file
        with open('news.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Write HTML to file
        with open('site.html', 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"Article text written to news.txt ({len(text)} characters)")
        print(f"Full HTML written to site.html ({len(full_html)} characters)")
        
        # If it's a Washington Post article, also run the WP extractor
        if is_washington_post:
            print("Running Washington Post specific extractor...")
            import subprocess
            try:
                result = subprocess.run(['python', 'wp.py', 'site.html'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("Washington Post content extracted successfully")
                else:
                    print(f"WP extractor failed: {result.stderr}")
            except Exception as e:
                print(f"Error running WP extractor: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if not use_existing_session and 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    main() 