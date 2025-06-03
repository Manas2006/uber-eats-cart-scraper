import requests
import json
import asyncio
from uber_scraper_async import UberEatsAsyncScraper

async def test_scraper_direct():
    """
    Test the scraper directly without the API.
    """
    cart_url = "https://eats.uber.com/group-orders/05fb718f-5c17-4c9c-817e-ffd5f9f04c07/join"
    
    try:
        scraper = UberEatsAsyncScraper()
        cart_data = await scraper.scrape_cart(cart_url)
        print("Direct scraper test successful!")
        print(json.dumps(cart_data.dict(), indent=2))
    except Exception as e:
        print(f"Error in direct scraper test: {str(e)}")

def test_scraper_api():
    """
    Test the scraper through the API.
    """
    cart_url = "https://eats.uber.com/group-orders/05fb718f-5c17-4c9c-817e-ffd5f9f04c07/join"
    
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
    asyncio.run(test_scraper_direct())
    
    print("\nTesting API...")
    test_scraper_api() 