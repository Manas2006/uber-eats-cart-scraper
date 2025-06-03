import random
import re
import asyncio
import logging
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from .models import CartItem, CartData

logger = logging.getLogger(__name__)

class UberEatsAsyncScraper:
    def __init__(self):
        pass

    async def scrape_cart(self, cart_url: str) -> CartData:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            try:
                logger.info(f"Scraping cart from URL: {cart_url}")
                await page.goto(cart_url, timeout=60000)
                await page.wait_for_load_state("networkidle", timeout=60000)
                # Join as guest
                try:
                    await page.wait_for_selector('input[placeholder="Enter your name"]', timeout=5000)
                    name_input = page.locator('input[placeholder="Enter your name"]')
                    join_button = page.locator('button:has-text("Join order")')
                    random_name = f"OrderSmarterBot{random.randint(1000,9999)}"
                    await name_input.fill(random_name)
                    await join_button.click()
                    logger.info(f"Joined as guest with name: {random_name}")
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(2)
                except Exception:
                    logger.info("No guest join form detected or already joined.")
                # Click view order
                try:
                    await page.wait_for_selector('a:has(div.al.aq.bc > div.bo.bp.co.dy:has-text("View Order"))', timeout=15000)
                    view_order_btn = page.locator('a:has(div.al.aq.bc > div.bo.bp.co.dy:has-text("View Order"))').first
                    await view_order_btn.click()
                    logger.info("Clicked 'View Order' button.")
                    await page.wait_for_selector('div[role="img"], div.al.aq.ci', timeout=15000)
                    await asyncio.sleep(2)
                except Exception:
                    logger.error("Could not find or click 'View Order' button.")
                    await page.screenshot(path="debug_view_order_page.png")
                    logger.error("Saved screenshot to debug_view_order_page.png")
                    raise
                # Get restaurant name
                restaurant = "Unknown Restaurant"
                try:
                    restaurant = await page.locator('h1').first.inner_text()
                except Exception:
                    pass
                # Scrape items
                items = []
                try:
                    await page.wait_for_selector('h6:has-text("Others in your group")', timeout=15000)
                    await page.wait_for_selector('li.al.aq.fa', timeout=10000)
                    participant_lis = await page.locator('li.al.aq.fa').all()
                    if len(participant_lis) > 1:
                        target_li = participant_lis[1]
                        dropdown_button = target_li.locator('button.bh.al.ci.dq').first
                        if dropdown_button:
                            await dropdown_button.wait_for(state="visible", timeout=5000)
                            await dropdown_button.scroll_into_view_if_needed()
                            await asyncio.sleep(1)
                            await dropdown_button.click()
                            max_retries = 5
                            for attempt in range(max_retries):
                                try:
                                    await page.wait_for_selector('div.bo.bp.co.dy.b1, div.cy.bo.bp.bq.br.jf', timeout=4000)
                                    await asyncio.sleep(1)
                                    break
                                except Exception:
                                    if attempt == max_retries - 1:
                                        raise
                                    await asyncio.sleep(1)
                            html = await target_li.inner_html()
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
                    logger.error(f"Error scraping group order: {str(e)}")
                total_price = sum(item.price * item.quantity for item in items)
                return CartData(
                    restaurant=restaurant,
                    items=items,
                    total_price=total_price
                )
            except Exception as e:
                logger.error(f"Error scraping cart: {str(e)}")
                raise
            finally:
                await context.close()
                await browser.close() 