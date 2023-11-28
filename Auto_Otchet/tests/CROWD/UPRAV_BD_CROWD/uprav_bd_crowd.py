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

# Получаем текущую дату и время
today_date = datetime.today()
# Переводим в формат Unix времени (timestamp)
today_unix_time = str(int(today_date.timestamp()))
# Получаем дату, предшествующую текущей на 8 дней
past_date = (today_date - timedelta(days=8))
# Переводим в формат Unix времени (timestamp)
past_unix_time = str(int(past_date.timestamp()))

today = f'&from={today_unix_time}000'
past = f'&to={past_unix_time}000'

try:
    browser.get('https://cmon.mos.ru/')
    switch_keycloak = browser.find_element(By.XPATH, '//main/div[3]/div/div[2]/div/div[2]/div[2]/a')
    switch_keycloak.click()
    time.sleep(5)
    input_login = browser.find_element(By.XPATH, '//form/div[1]/input')
    input_login.send_keys("ambrazhevich")
    input_passwrd = browser.find_element(By.XPATH, '//form/div[2]/input')
    input_passwrd.send_keys("wQANbm#Lz8dI")
    button = browser.find_element(By.XPATH, '//form/div[4]/input[2]')
    button.click()
    time.sleep(10)

    db_hdd = browser.get(
        f'https://cmon.mos.ru/dashboard/snapshot/neTYKWN4LHLPZddyAkphrefs2AQj6cVz?orgId=1{past}{today}')
    time.sleep(5)
    browser.save_screenshot("screenshot_DB.png")

finally:
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.quit()
