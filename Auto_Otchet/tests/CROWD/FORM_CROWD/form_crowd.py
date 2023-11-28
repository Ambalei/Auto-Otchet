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

global_link = 'https://cmon.mos.ru/d/node-exporter/node-exporter-full?orgId=1&var-datasource=default&var-system=%D0%98%D0%A1+%D0%9A%D0%9F%D0%9F%D0%9C&var-name='
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

severs = 'crowd-core1-10.89.81.67, crowd-core2-10.89.81.68, crowd-core3-10.89.81.75, crowd-core4-10.89.81.76, crowd-db1-10.89.81.69, crowd-db2-10.89.81.70, crowd-db3-10.89.81.77, crowd-db4-10.89.81.78, crowd-db5p-10.89.81.92, crowd-balance1p-10.89.81.83, crowd-balance2-10.89.81.79, crowd-mon1p-10.89.81.84, crowd-admin-10.89.81.65, crowd-promo-10.89.81.72, crowd-promo02p-10.89.81.80, crowd-gw1p-10.89.81.85, crowd-data01p-10.89.81.81, crowd-deploy1p-10.89.81.86, crowd-nexus1p-10.15.184.1, crowd-minio1p-172.17.24.8, crowd-minio2p-172.17.24.1, crowd-minio3p-10.89.81.85, crowd-minio4p-10.89.81.83'
server_list = severs.split(', ')

# Переименовываю сервера в убодоваримый вид с помощью regex(регулярные выражения)
def update_server_name(name):
    search = re.sub('-[\d\.]+', '', name)
    return search.replace('crowd-', '')

def update_server_link(link):
    return link.replace('-10.', '&var-node=10.')

links = {update_server_name(name): update_server_link(name) for name in server_list}

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

    photos_names = []
    photos_files = []
    def screenshot_garaph(panel_cpu, cpu):
        for key, value in links.items():
            link = global_link + value + today + past + panel_cpu
            screen = browser.get(link)
            time.sleep(5)
            browser.save_screenshot(f'{key}{cpu}.png')
            photos_names.append(f'{key}{cpu}')
            photos_files.append(f'{key}{cpu}.png')
            print(f'{key}{cpu}')

    screenshot_garaph(panel_cpu, cpu)
    screenshot_garaph(panel_ram, ram)
    screenshot_garaph(panel_net, net)
    screenshot_garaph(panel_disk, disk)
    screenshot_garaph(panel_time, nginx_time)
    screenshot_garaph(panel_success, nginx_success)

    photos_dict = dict(zip(photos_names, photos_files))

    # Записываем словарь в файл в формате JSON
    with open('photos_dict.json', 'w') as file:
        json.dump(photos_dict, file)

finally:
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.quit()
