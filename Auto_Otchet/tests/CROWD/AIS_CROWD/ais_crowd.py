import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1280,1400")
browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(10)

today_date = datetime.today().strftime("%Y-%m-%d")
past_date = (datetime.today() - timedelta(days=8)).strftime("%Y-%m-%d")

try:
    browser.get('https://mon-dc.mos.ru/')
    time.sleep(5)
    input_login = browser.find_element(By.XPATH, '//form/div[1]/div[2]/div/div/input')
    input_login.send_keys("ambrazhevichav")
    input_passwrd = browser.find_element(By.XPATH, '//form/div[2]/div[2]/div/div/input')
    input_passwrd.send_keys("Lexicon321")
    button = browser.find_element(By.XPATH, '//form/button')
    button.click()
    time.sleep(10)

    browser.get('https://mon-dc.mos.ru/d/1_hpN8jWz/systems?orgId=1&var-system_name=%D0%9A%D0%9F%D0%9F%D0%9C')
    date_input_button = browser.find_element(By.XPATH, '//header/nav/div[2]/div[1]/div[1]/button[1]')
    date_input_button.click()
    past_input = browser.find_element(By.XPATH, '//section/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[1]/input')
    past_input.clear()
    past_input.send_keys(past_date)
    today_input = browser.find_element(By.XPATH, '//section/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[1]/input')
    today_input.clear()
    today_input.send_keys(today_date)
    apply_input_button = browser.find_element(By.XPATH, '//section/div/div[1]/div[2]/div[1]/div[2]/button')
    apply_input_button.click()
    time.sleep(5)
    test_hide_button = browser.find_element(By.XPATH, '//main/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[24]/div/button')
    test_hide_button.click()
    time.sleep(15)
    browser.save_screenshot("screenshot.png")

finally:
    time.sleep(5)
    browser.quit()
