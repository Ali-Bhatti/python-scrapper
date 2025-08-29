#!/usr/bin/env python3
"""
Amazon Product Review Scraper
Scrapes product reviews from Amazon by ASIN and exports to CSV/JSON
Supports multiple regions (US, UK, DE) with pagination handling
"""

import requests
import json
import csv
import time
import random
import argparse
import sys
from datetime import datetime
from urllib.parse import (
    urljoin,
    urlparse,
    parse_qs,
    urlencode,
    urlunparse,
)
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import os
import re

class AmazonReviewScraper:
    def __init__(self, region='US'):
        self.region = region.upper()
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Region-specific configurations
        self.regions = {
            'US': {
                'domain': 'amazon.com',
                'base_url': 'https://www.amazon.com',
                'review_url_template': 'https://www.amazon.com/product-reviews/{asin}'
            },
            'UK': {
                'domain': 'amazon.co.uk',
                'base_url': 'https://www.amazon.co.uk',
                'review_url_template': 'https://www.amazon.co.uk/product-reviews/{asin}'
            },
            'DE': {
                'domain': 'amazon.de',
                'base_url': 'https://www.amazon.de',
                'review_url_template': 'https://www.amazon.de/product-reviews/{asin}'
            }
        }
        
        if self.region not in self.regions:
            raise ValueError(f"Unsupported region: {self.region}. Supported regions: {', '.join(self.regions.keys())}")
        
        self.config = self.regions[self.region]
    
    def get_review_url(self, asin=None, page=1, base_url=None):
        """Generate review URL for given ASIN or base URL and page number"""
        if base_url:
            parsed = urlparse(base_url)
            query = parse_qs(parsed.query)
            query['pageNumber'] = [str(page)]
            new_query = urlencode(query, doseq=True)
            parsed = parsed._replace(query=new_query)
            return urlunparse(parsed)

        if asin is None:
            raise ValueError("ASIN must be provided if base_url is not specified")

        base = self.config['review_url_template'].format(asin=asin)
        if page > 1:
            return f"{base}/ref=cm_cr_arp_d_paging_btm_next_{page}?pageNumber={page}"
        return base
    
    def extract_review_data(self, review_element):
        """Extract review data from a single review element"""
        try:
            # Review title
            title_element = review_element.find('a', {'data-hook': 'review-title'})
            title = title_element.get_text(strip=True) if title_element else "No title"
            
            # Review text
            text_element = review_element.find('span', {'data-hook': 'review-body'})
            text = text_element.get_text(strip=True) if text_element else "No review text"
            
            # Rating
            rating_element = review_element.find('i', {'data-hook': 'review-star-rating'})
            if not rating_element:
                rating_element = review_element.find('i', {'data-hook': 'cmps-review-star-rating'})
            
            rating = "0"
            if rating_element:
                rating_text = rating_element.get_text(strip=True)
                # Extract numeric rating from text like "4.0 out of 5 stars"
                rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                if rating_match:
                    rating = rating_match.group(1)
            
            # Reviewer name
            reviewer_element = review_element.find('span', {'class': 'a-profile-name'})
            reviewer = reviewer_element.get_text(strip=True) if reviewer_element else "Anonymous"
            
            # Date
            date_element = review_element.find('span', {'data-hook': 'review-date'})
            date = date_element.get_text(strip=True) if date_element else "Unknown date"
            
            # Verified purchase status
            verified_element = review_element.find('span', {'data-hook': 'avp-badge'})
            verified = "Yes" if verified_element else "No"
            
            return {
                'title': title,
                'text': text,
                'rating': rating,
                'reviewer': reviewer,
                'date': date,
                'verified_purchase': verified
            }
        except Exception as e:
            print(f"Error extracting review data: {e}")
            return None
    
    def scrape_page(self, asin=None, page=1, base_url=None):
        """Scrape reviews from a single page"""
        url = self.get_review_url(asin=asin, page=page, base_url=base_url)
        
        try:
            print(f"Scraping page {page}...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find review containers
            review_elements = soup.find_all('div', {'data-hook': 'review'})
            
            if not review_elements:
                # Try alternative selectors
                review_elements = soup.find_all('div', {'class': 'review'})
            
            reviews = []
            for review_element in review_elements:
                review_data = self.extract_review_data(review_element)
                if review_data:
                    reviews.append(review_data)
            
            # Check if there are more pages
            next_button = soup.find('li', {'class': 'a-last'})
            has_next = next_button and next_button.find('a') is not None
            
            return reviews, has_next
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            return [], False
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            return [], False
    
    def scrape_all_reviews(self, asin=None, url=None, max_pages=None):
        """Scrape all reviews for a given ASIN or full review URL"""
        if not asin and not url:
            raise ValueError("Either asin or url must be provided")

        all_reviews = []
        page = 1
        has_next = True

        target = asin if asin else url
        print(f"Starting to scrape reviews for: {target} from {self.region} Amazon")

        while has_next and (max_pages is None or page <= max_pages):
            reviews, has_next = self.scrape_page(asin=asin, page=page, base_url=url)
            
            if reviews:
                all_reviews.extend(reviews)
                print(f"Found {len(reviews)} reviews on page {page}")
            else:
                print(f"No reviews found on page {page}")
                break
            
            page += 1
            
            # Add delay to be respectful to Amazon's servers
            if has_next:
                delay = random.uniform(2, 5)
                print(f"Waiting {delay:.1f} seconds before next page...")
                time.sleep(delay)
        
        print(f"Total reviews scraped: {len(all_reviews)}")
        return all_reviews
    
    def export_to_csv(self, reviews, asin, filename=None):
        """Export reviews to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"amazon_reviews_{asin}_{self.region}_{timestamp}.csv"
        
        if not reviews:
            print("No reviews to export")
            return filename
        
        try:
            df = pd.DataFrame(reviews)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Reviews exported to CSV: {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    def export_to_json(self, reviews, asin, filename=None):
        """Export reviews to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"amazon_reviews_{asin}_{self.region}_{timestamp}.json"
        
        if not reviews:
            print("No reviews to export")
            return filename
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(reviews, f, indent=2, ensure_ascii=False)
            print(f"Reviews exported to JSON: {filename}")
            return filename
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Scrape Amazon product reviews by ASIN or URL')
    parser.add_argument('asin', nargs='?', help='Amazon ASIN (e.g., B08N5WRWNW)')
    parser.add_argument('--url', help='Full Amazon review page URL')
    parser.add_argument('--region', '-r', default='US', choices=['US', 'UK', 'DE'],
                       help='Amazon region (default: US)')
    parser.add_argument('--max-pages', '-m', type=int, default=None,
                       help='Maximum number of pages to scrape (default: all pages)')
    parser.add_argument('--format', '-f', choices=['csv', 'json', 'both'], default='both',
                       help='Export format (default: both)')
    parser.add_argument('--output', '-o', help='Output filename (without extension)')

    args = parser.parse_args()

    if not args.asin and not args.url:
        print("Error: provide either an ASIN or a URL")
        sys.exit(1)

    asin = args.asin
    if args.url and not asin:
        match = re.search(r'/product-reviews/([A-Z0-9]{5,})', args.url)
        if match:
            asin = match.group(1)

    try:
        # Initialize scraper
        scraper = AmazonReviewScraper(region=args.region)

        # Scrape reviews
        reviews = scraper.scrape_all_reviews(asin=asin, url=args.url, max_pages=args.max_pages)

        if not reviews:
            print("No reviews found for this input")
            sys.exit(1)
        
        # Export reviews
        if args.format in ['csv', 'both']:
            csv_filename = None
            if args.output:
                csv_filename = f"{args.output}.csv"
            scraper.export_to_csv(reviews, asin if asin else 'reviews', csv_filename)

        if args.format in ['json', 'both']:
            json_filename = None
            if args.output:
                json_filename = f"{args.output}.json"
            scraper.export_to_json(reviews, asin if asin else 'reviews', json_filename)
        
        print(f"\nScraping completed successfully!")
        print(f"Total reviews: {len(reviews)}")
        if asin:
            print(f"ASIN: {asin}")
        if args.url:
            print(f"URL: {args.url}")
        print(f"Region: {args.region}")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 