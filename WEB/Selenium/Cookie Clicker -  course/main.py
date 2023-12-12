from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

time_off = time.time() + 60*5
time_click = 5

driver.get("http://orteil.dashnet.org/experiments/cookie/")

while time.time() < time_off:
    click_start = time.time()
    while time.time() < click_start + time_click:
        driver.find_element(By.ID, "cookie").click()
        
    try:
        money = int(driver.find_element(By.ID, "money").text)
    except:
        money = int(driver.find_element(By.ID, "money").text.replace(',', ''))
        
    buy_options = driver.find_elements(By.CSS_SELECTOR, "#store div b")
    prices = [int(price.text.split()[-1].replace(',', '')) for price in buy_options if price.text != ""]
    expensive = 0
    for price in prices:
        if money > price:
            expensive = prices.index(price)
    try:
        driver.find_element(By.XPATH, f"/html/body/div[4]/div[5]/div/div[{expensive + 1}]").click()
    except:
        driver.find_element(By.XPATH, f"/html/body/div[3]/div[5]/div/div[{expensive + 1}]").click()

cps = driver.find_element(By.ID, "cps").text
print(cps[cps.find(":") + 1:])