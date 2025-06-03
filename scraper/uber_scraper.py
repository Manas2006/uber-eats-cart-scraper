from playwright.sync_api import sync_playwright
from typing import List, Dict, Optional
import json
from dotenv import load_dotenv
import logging
import time
import random
import re
from bs4 import BeautifulSoup
from .models import CartItem, CartData  # <-- import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

CART_URL = "https://eats.uber.com/group-orders/925d1d17-c833-4c96-915c-831e3027e67d/join"

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
            # Wait for the 'Others in your group' header
            self.page.wait_for_selector('h6:has-text("Others in your group")', timeout=15000)
            others_header = self.page.locator('h6:has-text("Others in your group")').first
            # Wait for all participant lis to be present
            self.page.wait_for_selector('li.al.aq.fa', timeout=10000)
            participant_lis = self.page.locator('li.al.aq.fa').all()
            if len(participant_lis) > 1:
                target_li = participant_lis[1]  # Second participant
                dropdown_button = target_li.locator('button.bh.al.ci.dq').first
                if dropdown_button:
                    try:
                        dropdown_button.wait_for(state="visible", timeout=5000)
                        dropdown_button.scroll_into_view_if_needed()
                        self.page.wait_for_timeout(1000)
                        dropdown_button.click()
                        # More robust wait for items to appear
                        max_retries = 5
                        for attempt in range(max_retries):
                            try:
                                self.page.wait_for_selector('div.bo.bp.co.dy.b1, div.cy.bo.bp.bq.br.jf', timeout=4000)
                                self.page.wait_for_timeout(1000)  # Give extra time for rendering
                                break
                            except Exception:
                                if attempt == max_retries - 1:
                                    raise
                                self.page.wait_for_timeout(1000)  # Wait and retry
                        # Dump the HTML of the expanded second participant li for debugging
                        try:
                            html = target_li.inner_html()
                            with open("debug_second_participant_li_expanded.html", "w", encoding="utf-8") as f:
                                f.write(html)
                            logger.info("Dumped HTML of expanded second participant li to debug_second_participant_li_expanded.html")
                        except Exception as e:
                            logger.error(f"Failed to dump HTML of expanded second participant li: {str(e)}")
                        # Scrape items for the expanded second participant using in-memory HTML parsing
                        html = target_li.inner_html()
                        soup = BeautifulSoup(html, "html.parser")
                        for a in soup.find_all("a"):
                            name_div = a.find("div", class_="bo bp co dy b1")
                            price_div = a.find("div", class_=lambda c: c and c.startswith("cy bo bp bq br"))
                            if name_div and price_div:
                                item_name = name_div.get_text(strip=True)
                                price_text = price_div.get_text()
                                match = re.search(r"\$([0-9]+(?:\.[0-9]{2})?)", price_text)
                                if match:
                                    price = float(match.group(1))
                                    items.append(CartItem(
                                        name=item_name,
                                        quantity=1,
                                        price=price,
                                        person="Manas"
                                    ))
                    except Exception as e:
                        logger.error(f"Failed to click dropdown button: {str(e)}")
                else:
                    logger.error("Could not find dropdown button in second participant li.")
            else:
                logger.error("Could not find second participant li.al.aq.fa.")
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
    try:
        with UberEatsScraper() as scraper:
            cart_data = scraper.scrape_cart(CART_URL)
            # Output JSON file with names and prices
            output = [{"name": item.name, "price": item.price} for item in cart_data.items]
            with open("scraped_items.json", "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)
            print(json.dumps(output, indent=2))
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 