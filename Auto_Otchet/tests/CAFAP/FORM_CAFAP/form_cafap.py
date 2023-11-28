import json
import re
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1024,720")

browser = webdriver.Chrome(options=chrome_options)
browser.implicitly_wait(10)

today_date = datetime.today()
today_unix_time = str(int(today_date.timestamp()))
past_date = (today_date - timedelta(days=8))
past_unix_time = str(int(past_date.timestamp()))

today = f'&from={today_unix_time}000'
past = f'&to={past_unix_time}000'

global_link = 'https://cmon.mos.ru/d/node-exporter/node-exporter-full?orgId=1&var-datasource=default&var-system=%D0%98%D0%A1%20%D0%A6%D0%90%D0%A4%D0%90%D0%9F&'
panel_cpu = '&viewPanel=77'
panel_ram = '&viewPanel=78'
panel_net = '&viewPanel=74'
panel_disk = '&viewPanel=152'
panel_time = '&viewPanel=40'
panel_success = '&viewPanel=157'

cpu = 'cpu'
ram = 'ram'
net = 'net'
disk = 'disk'
nginx_time = 'time'
nginx_success = 'nginx'

links = {
    'cafap-data01p': 'var-name=CAFAP-DATA01P&var-node=10.89.79.113&var-port=9182',
    'cafap-db1' : 'var-name=CAFAP-DB1&var-node=10.89.79.104&var-port=9182',
    'cafap-db2' : 'var-name=CAFAP-DB2&var-node=10.89.79.105&var-port=9182',
    'cafap-db3p' : 'var-name=CAFAP-DB3P&var-node=10.89.79.112&var-port=9182',
    'cafap-db4p' : 'var-name=CAFAP-DB4P&var-node=10.89.79.114&var-port=9182',
    'cafap-db5p' : 'var-name=CAFAP-DB5&var-node=10.89.79.10&var-port=9182',
    'cafap-deploy1p' : 'var-name=CAFAP-DEPLOY1P&var-node=10.89.79.31&var-port=9182',
    'cafap-gw1p' : 'var-name=CAFAP-GW1P&var-node=10.89.79.28&var-port=9182',
    'cafap-mon1p' : 'var-name=CAFAP-MON1P&var-node=10.89.79.25&var-port=9182',
    'cafap-nexus1p' : 'var-name=CAFAP-NEXUS1P&var-node=10.15.184.33&var-port=9182',
    'cafap-router1p' : 'var-name=CAFAP-ROUTER1P&var-node=10.89.79.27&var-port=9182',
    'cafap-web1' : 'var-name=CAFAP-WEB1&var-node=10.89.79.110&var-port=9182',
    'cafap-web2' : 'var-name=CAFAP-WEB2&var-node=10.89.79.111&var-port=9182'
}

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
    def screenshot_garaph(panel_cpu, cpu):
        for key, value in links.items():
            link = global_link + value + today + past + panel_cpu
            screen = browser.get(link)
            time.sleep(5)
            print(f'{key}{cpu}')
            browser.save_screenshot(f'{key}{cpu}.png')

    screenshot_garaph(panel_cpu, cpu)
    screenshot_garaph(panel_ram, ram)
    screenshot_garaph(panel_net, net)
    screenshot_garaph(panel_disk, disk)
    screenshot_garaph(panel_time, nginx_time)
    screenshot_garaph(panel_success, nginx_success)

finally:
    time.sleep(5)
    browser.quit()