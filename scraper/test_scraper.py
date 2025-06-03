import requests
import json
from uber_scraper import UberEatsScraper

def test_scraper_direct():
    """
    Test the scraper directly without the API.
    """
    cart_url = "https://eats.uber.com/group-orders/7938685b-f05c-419c-a8aa-6e03fc41f840/join"
    
    try:
        with UberEatsScraper() as scraper:
            cart_data = scraper.scrape_cart(cart_url)
            print("Direct scraper test successful!")
            print(json.dumps(cart_data.dict(), indent=2))
    except Exception as e:
        print(f"Error in direct scraper test: {str(e)}")

def test_scraper_api():
    """
    Test the scraper through the API.
    """
    cart_url = "https://eats.uber.com/group-orders/7938685b-f05c-419c-a8aa-6e03fc41f840/join"
    
    try:
        response = requests.post(
            "http://localhost:8000/scrape",
            json={"url": cart_url}
        )
        response.raise_for_status()
        print("API test successful!")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error in API test: {str(e)}")

if __name__ == "__main__":
    print("Testing direct scraper...")
    test_scraper_direct()
    
    print("\nTesting API...")
    test_scraper_api() 