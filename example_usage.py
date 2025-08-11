#!/usr/bin/env python3
"""
Example usage of the Amazon Review Scraper
Demonstrates how to use the scraper programmatically
"""

from amazon_review_scraper import AmazonReviewScraper
import json

def example_basic_usage():
    """Basic example of scraping reviews"""
    print("=== Basic Usage Example ===")
    
    # Initialize scraper for US Amazon
    scraper = AmazonReviewScraper(region='US')
    
    # Example ASIN (Amazon Echo Dot)
    asin = 'B08N5WRWNW'
    
    # Scrape reviews (limit to 2 pages for demo)
    reviews = scraper.scrape_all_reviews(asin, max_pages=2)
    
    if reviews:
        print(f"Found {len(reviews)} reviews")
        
        # Export to both formats
        csv_file = scraper.export_to_csv(reviews, asin)
        json_file = scraper.export_to_json(reviews, asin)
        
        print(f"Exported to: {csv_file}, {json_file}")
    else:
        print("No reviews found")

def example_multiple_regions():
    """Example of scraping from different regions"""
    print("\n=== Multiple Regions Example ===")
    
    asin = 'B08N5WRWNW'  # Example ASIN
    
    regions = ['US', 'UK', 'DE']
    
    for region in regions:
        print(f"\nScraping from {region} Amazon...")
        scraper = AmazonReviewScraper(region=region)
        
        # Scrape just 1 page per region for demo
        reviews = scraper.scrape_all_reviews(asin, max_pages=1)
        
        if reviews:
            print(f"Found {len(reviews)} reviews from {region}")
            # Export with region-specific filename
            filename = f"reviews_{region.lower()}"
            scraper.export_to_csv(reviews, asin, filename)
        else:
            print(f"No reviews found for {region}")

def example_custom_processing():
    """Example of custom data processing"""
    print("\n=== Custom Processing Example ===")
    
    scraper = AmazonReviewScraper(region='US')
    asin = 'B08N5WRWNW'
    
    # Scrape reviews
    reviews = scraper.scrape_all_reviews(asin, max_pages=1)
    
    if reviews:
        # Custom analysis
        total_rating = sum(float(review['rating']) for review in reviews)
        avg_rating = total_rating / len(reviews)
        
        verified_purchases = sum(1 for review in reviews if review['verified_purchase'] == 'Yes')
        
        print(f"Average rating: {avg_rating:.2f}/5.0")
        print(f"Verified purchases: {verified_purchases}/{len(reviews)}")
        
        # Find 5-star reviews
        five_star_reviews = [r for r in reviews if r['rating'] == '5.0']
        print(f"5-star reviews: {len(five_star_reviews)}")
        
        # Show first 5-star review
        if five_star_reviews:
            print(f"\nSample 5-star review:")
            print(f"Title: {five_star_reviews[0]['title']}")
            print(f"Reviewer: {five_star_reviews[0]['reviewer']}")
            print(f"Text: {five_star_reviews[0]['text'][:100]}...")

def example_error_handling():
    """Example of error handling"""
    print("\n=== Error Handling Example ===")
    
    # Try with invalid ASIN
    scraper = AmazonReviewScraper(region='US')
    invalid_asin = 'INVALID123'
    
    try:
        reviews = scraper.scrape_all_reviews(invalid_asin, max_pages=1)
        if not reviews:
            print(f"No reviews found for invalid ASIN: {invalid_asin}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    print("Amazon Review Scraper - Example Usage")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_multiple_regions()
    example_custom_processing()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("Examples completed!") 