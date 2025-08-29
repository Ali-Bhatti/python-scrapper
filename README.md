# Amazon Product Review Scraper

A lightweight Python script to scrape Amazon product reviews by ASIN and export them to CSV and/or JSON formats. Supports multiple Amazon regions (US, UK, DE) with automatic pagination handling.

## Features

- ✅ Scrape reviews by ASIN (Amazon Standard Identification Number)
- ✅ Support for multiple Amazon regions (US, UK, DE)
- ✅ Automatic pagination handling
- ✅ Export to CSV and/or JSON formats
- ✅ Extract all required data: review title, text, rating, reviewer name, date, verified purchase status
- ✅ Built-in error handling and rate limiting
- ✅ No login required (works without Amazon account)
- ✅ Random delays to respect Amazon's servers
- ✅ Command-line interface with flexible options

## Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd python-scrapper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install requests beautifulsoup4 lxml pandas fake-useragent python-dotenv
   ```

## Usage

### Basic Usage

```bash
# Scrape all reviews for a product (US Amazon)
python amazon_review_scraper.py B08N5WRWNW

# Scrape using a full review URL (either syntax works)
python amazon_review_scraper.py --url "https://www.amazon.com/product-reviews/B08N5WRWNW?pageNumber=1"
python amazon_review_scraper.py "https://www.amazon.com/product-reviews/B08N5WRWNW?pageNumber=1"

# Scrape from UK Amazon
python amazon_review_scraper.py B08N5WRWNW --region UK

# Scrape from German Amazon
python amazon_review_scraper.py B08N5WRWNW --region DE
```

### Advanced Usage

```bash
# Limit to first 5 pages
python amazon_review_scraper.py B08N5WRWNW --max-pages 5

# Export only to CSV
python amazon_review_scraper.py B08N5WRWNW --format csv

# Export only to JSON
python amazon_review_scraper.py B08N5WRWNW --format json

# Custom output filename
python amazon_review_scraper.py B08N5WRWNW --output my_reviews

# Combine options
python amazon_review_scraper.py B08N5WRWNW --region UK --max-pages 3 --format csv --output uk_reviews
```

### Command Line Options

- `asin`: Amazon ASIN (or a full review URL)
- `--url`: Full Amazon review page URL (optional if URL is the first argument)
- `--region, -r`: Amazon region (US, UK, DE) - default: US
- `--max-pages, -m`: Maximum pages to scrape - default: all pages
- `--format, -f`: Export format (csv, json, both) - default: both
- `--output, -o`: Custom output filename (without extension)

## Output Files

The script generates files with the following naming convention:
- `amazon_reviews_{ASIN}_{REGION}_{TIMESTAMP}.csv`
- `amazon_reviews_{ASIN}_{REGION}_{TIMESTAMP}.json`

### CSV Output Columns
- `title`: Review title
- `text`: Review text/body
- `rating`: Star rating (1-5)
- `reviewer`: Reviewer name
- `date`: Review date
- `verified_purchase`: Whether it's a verified purchase (Yes/No)

### JSON Output Format
```json
[
  {
    "title": "Great product!",
    "text": "This product exceeded my expectations...",
    "rating": "5.0",
    "reviewer": "John Doe",
    "date": "Reviewed in the United States on January 15, 2024",
    "verified_purchase": "Yes"
  }
]
```

## Finding Product ASINs

1. **From Amazon URL**: Look for the ASIN in the product URL
   - Example: `https://www.amazon.com/dp/B08N5WRWNW` → ASIN is `B08N5WRWNW`

2. **From Product Page**: 
   - Scroll down to "Product details" section
   - Look for "ASIN" field

3. **From Browser Developer Tools**:
   - Right-click on product page → Inspect
   - Search for "ASIN" in the page source

## Important Notes

### Rate Limiting
- The script includes random delays (2-5 seconds) between page requests
- This helps avoid being blocked by Amazon
- Don't run multiple instances simultaneously

### Legal Considerations
- This tool is for educational and research purposes
- Respect Amazon's Terms of Service and robots.txt
- Don't overload their servers with excessive requests
- Consider using Amazon's official API for commercial use

### Troubleshooting

**No reviews found:**
- Verify the ASIN is correct
- Check if the product has reviews
- Try a different region if the product exists in multiple markets

**Connection errors:**
- Check your internet connection
- Amazon might be blocking requests temporarily
- Try again later or use a VPN

**Permission denied:**
- Make sure the script is executable: `chmod +x amazon_review_scraper.py`

## Example Output

```
Starting to scrape reviews for ASIN: B08N5WRWNW from US Amazon
Scraping page 1...
Found 10 reviews on page 1
Waiting 3.2 seconds before next page...
Scraping page 2...
Found 10 reviews on page 2
Waiting 4.1 seconds before next page...
Scraping page 3...
Found 5 reviews on page 3
Total reviews scraped: 25
Reviews exported to CSV: amazon_reviews_B08N5WRWNW_US_20241201_143022.csv
Reviews exported to JSON: amazon_reviews_B08N5WRWNW_US_20241201_143022.json

Scraping completed successfully!
Total reviews: 25
ASIN: B08N5WRWNW
Region: US
```

## Dependencies

- `requests`: HTTP library for making requests
- `beautifulsoup4`: HTML parsing library
- `lxml`: XML/HTML parser
- `pandas`: Data manipulation and CSV export
- `fake-useragent`: Random user agent generation
- `python-dotenv`: Environment variable management
