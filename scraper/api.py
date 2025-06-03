from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from uber_scraper import UberEatsScraper, CartData
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OrderSmarter API",
    description="API for scraping and analyzing Uber Eats carts",
    version="1.0.0"
)

class CartUrl(BaseModel):
    url: HttpUrl

@app.post("/scrape", response_model=CartData)
async def scrape_cart(cart_url: CartUrl):
    """
    Scrape an Uber Eats cart from the provided URL.
    
    Args:
        cart_url (CartUrl): The shareable Uber Eats cart URL
        
    Returns:
        CartData: The scraped cart data
    """
    try:
        with UberEatsScraper() as scraper:
            cart_data = scraper.scrape_cart(str(cart_url.url))
            return cart_data
    except Exception as e:
        logger.error(f"Error scraping cart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 