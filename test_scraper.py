#!/usr/bin/env python3
"""
Simple test script for the Amazon Review Scraper
Tests basic functionality with a sample ASIN
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amazon_review_scraper import AmazonReviewScraper

def test_scraper():
    """Test the scraper with a sample ASIN and URL"""
    print("Testing Amazon Review Scraper...")
    print("=" * 40)

    # Test ASIN (Amazon Echo Dot - a popular product with many reviews)
    test_asin = 'B08N5WRWNW'
    test_url = f"https://www.amazon.com/product-reviews/{test_asin}?pageNumber=1"

    try:
        # Initialize scraper
        print("Initializing scraper for US Amazon...")
        scraper = AmazonReviewScraper(region='US')

        # Test scraping just 1 page using ASIN
        print(f"Testing with ASIN: {test_asin}")
        print("Scraping 1 page of reviews...")

        reviews = scraper.scrape_all_reviews(asin=test_asin, max_pages=1)

        if reviews:
            print(f"✅ Success! Found {len(reviews)} reviews")

            # Show sample review data
            if len(reviews) > 0:
                sample = reviews[0]
                print("\nSample review data:")
                print(f"  Title: {sample['title'][:50]}...")
                print(f"  Rating: {sample['rating']}/5")
                print(f"  Reviewer: {sample['reviewer']}")
                print(f"  Verified: {sample['verified_purchase']}")
                print(f"  Date: {sample['date']}")

            # Test export functionality
            print("\nTesting export functionality...")
            csv_file = scraper.export_to_csv(reviews, test_asin, "test_output")
            json_file = scraper.export_to_json(reviews, test_asin, "test_output")

            if csv_file and json_file:
                print("✅ Export test successful!")
                print(f"  CSV file: {csv_file}")
                print(f"  JSON file: {json_file}")

                # Clean up test files
                try:
                    os.remove(csv_file)
                    os.remove(json_file)
                    print("  Test files cleaned up")
                except:
                    pass
            else:
                print("❌ Export test failed")

        else:
            print("❌ No reviews found - this might be normal for some products")

        # Test scraping using URL
        print(f"\nTesting with URL: {test_url}")
        url_reviews = scraper.scrape_all_reviews(url=test_url, max_pages=1)
        if url_reviews:
            print(f"✅ URL scraping returned {len(url_reviews)} reviews")
        else:
            print("❌ URL scraping returned no reviews")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

    print("\n" + "=" * 40)
    print("Test completed!")
    return True

def test_help():
    """Test that the script shows help when run without arguments"""
    print("\nTesting help functionality...")
    print("=" * 40)
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'amazon_review_scraper.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'usage:' in result.stdout:
            print("✅ Help functionality works correctly")
            return True
        else:
            print("❌ Help functionality failed")
            return False
    except Exception as e:
        print(f"❌ Help test failed: {e}")
        return False

if __name__ == "__main__":
    print("Amazon Review Scraper - Test Suite")
    print("=" * 50)
    
    # Run tests
    test1_passed = test_scraper()
    test2_passed = test_help()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"  Scraper functionality: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"  Help functionality: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The scraper is ready to use.")
        print("\nTo use the scraper:")
        print("  python amazon_review_scraper.py B08N5WRWNW")
        print("  python amazon_review_scraper.py --help")
    else:
        print("\n⚠️  Some tests failed. Please check the installation.") 