from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Get cookie.
baking = driver.find_element(By.ID, value="cookie")

# Get upgrade items ids
items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

# 5 seconds
timeout = time.time() + 5

# 5 minutes
game_over = time.time() + 60*5



while True:
    # click on cookies
    baking.click()

    # Every 5 seconds:
    if time.time() > timeout:

        # Get all the upgrades:
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_prices = []

        # convert the tag text into integers:
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Create a dictionary of store items and prices:
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Get current cookie count
        money_element = driver.find_element(By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # find upgrades that we can currently afford:
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # purchase the most expensive upgrade that you can currently afford:
        can_purchase = max(affordable_upgrades)
        print(can_purchase)
        to_purchase_id = affordable_upgrades[can_purchase]

        driver.find_element(By.ID, value=to_purchase_id).click()

        # Add another 5 seconds until the next check:
        timeout = time.time() + 5


    # After 5 minutes stop the bot and check the cookies per second count:
    if time.time() > game_over:
        cookie_per_s = driver.find_element(By.ID, value="cps").text
        print(cookie_per_s)
        break