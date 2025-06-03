from playwright.sync_api import sync_playwright
from typing import List, Dict, Optional
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class CartItem(BaseModel):
    name: str
    quantity: int
    price: float
    description: Optional[str] = None
    person: Optional[str] = None

class CartData(BaseModel):
    restaurant: str
    items: List[CartItem]
    total_price: float

class UberEatsScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def _join_as_guest(self):
        try:
            self.page.wait_for_selector('input[placeholder="Enter your name"]', timeout=5000)
            name_input = self.page.locator('input[placeholder="Enter your name"]')
            join_button = self.page.locator('button:has-text("Join order")')
            random_name = f"OrderSmarterBot{random.randint(1000,9999)}"
            name_input.fill(random_name)
            join_button.click()
            logger.info(f"Joined as guest with name: {random_name}")
            self.page.wait_for_load_state("networkidle")
            time.sleep(2)
        except Exception as e:
            logger.info("No guest join form detected or already joined.")

    def _click_view_order(self):
        try:
            # Use a highly specific selector for the 'View Order' button
            self.page.wait_for_selector('a:has(div.al.aq.bc > div.bo.bp.co.dy:has-text("View Order"))', timeout=15000)
            view_order_btn = self.page.locator('a:has(div.al.aq.bc > div.bo.bp.co.dy:has-text("View Order"))').first
            view_order_btn.click()
            logger.info("Clicked 'View Order' button.")
            # Wait for the group order summary to appear (e.g., a person's avatar or order section)
            self.page.wait_for_selector('div[role="img"], div.al.aq.ci', timeout=15000)
            time.sleep(2)
        except Exception as e:
            logger.error("Could not find or click 'View Order' button.")
            with open("debug_view_order_page.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            logger.error("Saved current page HTML to debug_view_order_page.html")
            raise

    def _scrape_group_order(self) -> List[CartItem]:
        items = []
        try:
            # Each person's section (look for avatar or name)
            person_sections = self.page.locator('div:has(div[role="img"])').all()
            for section in person_sections:
                try:
                    # Person's name (avatar alt or sibling text)
                    person_name = section.locator('div[role="img"]').get_attribute('aria-label')
                    if not person_name:
                        # fallback: try to get text from the section
                        person_name = section.inner_text().split('\n')[0]
                    # Each food item (look for div.al.aq.ci)
                    food_items = section.locator('div.al.aq.ci').all()
                    for food in food_items:
                        try:
                            name = food.locator('div').first.inner_text()
                            # Price is in a sibling div with $ sign
                            price = None
                            price_divs = food.locator('div').all()
                            for div in price_divs:
                                text = div.inner_text()
                                if '$' in text:
                                    price = float(text.replace('$','').strip())
                                    break
                            if name and price is not None:
                                items.append(CartItem(
                                    name=name,
                                    quantity=1,
                                    price=price,
                                    person=person_name
                                ))
                        except Exception as e:
                            logger.error(f"Error scraping food item: {str(e)}")
                            continue
                except Exception as e:
                    logger.error(f"Error scraping person section: {str(e)}")
                    continue
        except Exception as e:
            logger.error(f"Error scraping group order: {str(e)}")
        return items

    def scrape_cart(self, cart_url: str) -> CartData:
        try:
            logger.info(f"Scraping cart from URL: {cart_url}")
            self.page.goto(cart_url)
            self.page.wait_for_load_state("networkidle")
            self._join_as_guest()
            self._click_view_order()
            # Restaurant name from the main page
            restaurant = "Unknown Restaurant"
            try:
                restaurant = self.page.locator('h1').first.inner_text()
            except Exception:
                pass
            items = self._scrape_group_order()
            total_price = sum(item.price * item.quantity for item in items)
            return CartData(
                restaurant=restaurant,
                items=items,
                total_price=total_price
            )
        except Exception as e:
            logger.error(f"Error scraping cart: {str(e)}")
            raise

def main():
    cart_url = "https://eats.uber.com/group-orders/7938685b-f05c-419c-a8aa-6e03fc41f840/join"
    try:
        with UberEatsScraper() as scraper:
            cart_data = scraper.scrape_cart(cart_url)
            print(json.dumps(cart_data.dict(), indent=2))
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 