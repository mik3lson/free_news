# 📰 Free News Extractor, Pay Wall Bypass

A Python-based web scraping tool designed to extract news article content from various news websites, with special optimization for The Washington Post.

## 🎯 Purpose

This tool is designed for **educational and research purposes** to demonstrate web scraping capabilities using Selenium. It allows users to extract clean, readable text content from news articles for:

- Academic research
- Content analysis
- Educational demonstrations
- Personal reading (when appropriate)

## ⚠️ Important Disclaimer

**This tool is for educational demonstration purposes only.**

- The author is **not responsible** for any legal issues arising from the use of this tool
- Users are responsible for ensuring their use complies with:
  - Website Terms of Service
  - Copyright laws
  - Fair use guidelines
  - Applicable local and international laws
- Use this tool **only when appropriate** and with proper authorization
- Respect website robots.txt files and rate limiting
- Consider the impact on website servers and resources

## 🚀 Features

- **Fast Selenium-based extraction** with anti-detection measures
- **Washington Post optimization** with specialized content parsing
- **Multiple extraction strategies** for robust content retrieval
- **HTML dump capability** for debugging and analysis
- **Existing browser session support** to avoid blocking
- **Unicode and encoding fix** for clean text output

## 📋 Requirements

### Python Dependencies
```bash
pip install -r requirements.txt
```

### System Requirements
- Python 3.7+
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/free_news.git
   cd free_news
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python extract_news.py --help
   ```

## 📖 Usage

### Basic Usage

```bash
python extract_news.py <news_url>
```

### Washington Post Articles

For Washington Post articles, use the `-wp` flag for optimized extraction:

```bash
python extract_news.py "https://www.washingtonpost.com/article-url" -wp
```

### Using Existing Browser Session

To avoid detection and use your existing browser profile:

1. **Start Chrome with debugging enabled:**
   ```bash
   chrome --remote-debugging-port=9222
   ```

2. **Run the extractor:**
   ```bash
   python extract_news.py "https://example.com/article" --use-existing-session
   ```

3. **For Washington Post with existing session:**
   ```bash
   python extract_news.py "https://www.washingtonpost.com/article" --use-existing-session -wp
   ```

## 📁 Output Files

The tool generates two output files:

- **`news.txt`** - Clean, extracted article text
- **`site.html`** - Full HTML source for debugging

## 🔧 Command Line Options

| Option | Description |
|--------|-------------|
| `<news_url>` | **Required.** The URL of the news article to extract |
| `-wp` | **Optional.** Optimize extraction for Washington Post articles |
| `--use-existing-session` | **Optional.** Connect to existing Chrome session |

## 🏗️ Architecture

### Main Script (`extract_news.py`)
- **Selenium WebDriver setup** with anti-detection measures
- **Multiple extraction strategies** for robust content retrieval
- **Speed optimizations** to beat paywall timers
- **Automatic WP extractor integration**

### Washington Post Extractor (`wp.py`)
- **Specialized JSON parsing** for WP content structure
- **Unicode escape sequence handling**
- **Encoding issue resolution**
- **Quote and apostrophe correction**

## ⚡ Performance Optimizations

- **Eager page loading** - Doesn't wait for all resources
- **CSS and font loading disabled** for faster rendering
- **Background processes disabled**
- **Multiple content detection strategies**
- **Early exit on successful extraction**

## 🛡️ Anti-Detection Features

- **WebDriver property removal**
- **Realistic user agent**
- **Automation flags disabled**
- **Headless mode support**
- **Existing session integration**

## 📝 Example Output

```bash
$ python extract_news.py "https://www.washingtonpost.com/politics/2025/07/01/ai-moratorium-big-beautiful-bill/" -wp

Starting new Chrome session...
Extracting content from: https://www.washingtonpost.com/politics/2025/07/01/ai-moratorium-big-beautiful-bill/
Loading page...
Found content via selector: [class*="story"]
Article text written to news.txt (615 characters)
Full HTML written to site.html (631412 characters)
Running Washington Post specific extractor...
Washington Post content extracted successfully
```

## 🔍 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   - The tool automatically downloads ChromeDriver via webdriver-manager
   - Ensure you have internet connection for the first run

2. **Content not extracted**
   - Try using the `-wp` flag for Washington Post articles
   - Use `--use-existing-session` to avoid blocking
   - Check the `site.html` file for debugging

3. **Encoding issues**
   - The WP extractor automatically handles Unicode and encoding problems
   - Check the output for any remaining garbled characters

### Debug Mode

To see detailed extraction information, the scripts provide verbose output showing:
- Number of content matches found
- Extraction strategy used
- Content preview for each match

## 🤝 Contributing

Contributions are welcome! Please ensure your changes:
- Include proper error handling
- Maintain the educational purpose
- Add appropriate documentation
- Follow existing code style

## 📄 License

This project is for educational purposes. Please use responsibly and in accordance with applicable laws and website terms of service.

## 🔗 Related Projects

- [Selenium WebDriver](https://selenium-python.readthedocs.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Newspaper3k](https://newspaper.readthedocs.io/)

---

**Remember: This tool is for educational demonstration. Use responsibly and legally.** 
