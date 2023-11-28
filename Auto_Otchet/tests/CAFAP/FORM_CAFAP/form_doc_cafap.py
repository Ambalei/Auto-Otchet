from datetime import datetime
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
import requests

doc = DocxTemplate('form_cafap_tpl.docx')

name = "Амбражевич А.В."
today_date = datetime.today().strftime("%d.%m.%Y")
today_time = datetime.today().strftime("%H:%M")

servers = ['data01pcpu', 'data01pdisk', 'data01pnet', 'data01pnginx', 'data01pram',
           'data01ptime', 'db1cpu', 'db1disk', 'db1net', 'db1nginx', 'db1ram',
           'db1time', 'db2cpu', 'db2disk', 'db2net', 'db2nginx', 'db2ram',
           'db2time', 'db3pcpu', 'db3pdisk', 'db3pnet', 'db3pnginx', 'db3pram',
           'db3ptime', 'db4pcpu', 'db4pdisk', 'db4pnet', 'db4pnginx', 'db4pram',
           'db4ptime', 'db5pcpu', 'db5pdisk', 'db5pnet', 'db5pnginx', 'db5pram',
           'db5ptime', 'deploy1pcpu', 'deploy1pdisk', 'deploy1pnet', 'deploy1pnginx',
           'deploy1pram', 'deploy1ptime', 'gw1pcpu', 'gw1pdisk', 'gw1pnet',
           'gw1pnginx', 'gw1pram', 'gw1ptime', 'mon1pcpu', 'mon1pdisk', 'mon1pnet',
           'mon1pnginx', 'mon1pram', 'mon1ptime', 'nexus1pcpu', 'nexus1pdisk',
           'nexus1pnet', 'nexus1pnginx', 'nexus1pram', 'nexus1ptime', 'router1pcpu',
           'router1pdisk', 'router1pnet', 'router1pnginx', 'router1pram', 'router1ptime',
           'web1cpu', 'web1disk', 'web1net', 'web1nginx', 'web1ram', 'web1time',
           'web2cpu', 'web2disk', 'web2net', 'web2nginx', 'web2ram', 'web2time']

screenshot = ['cafap-data01pcpu.png', 'cafap-data01pdisk.png', 'cafap-data01pnet.png', 'cafap-data01pnginx.png',
              'cafap-data01pram.png', 'cafap-data01ptime.png', 'cafap-db1cpu.png', 'cafap-db1disk.png',
              'cafap-db1net.png', 'cafap-db1nginx.png', 'cafap-db1ram.png', 'cafap-db1time.png', 'cafap-db2cpu.png',
              'cafap-db2disk.png', 'cafap-db2net.png', 'cafap-db2nginx.png', 'cafap-db2ram.png', 'cafap-db2time.png',
              'cafap-db3pcpu.png', 'cafap-db3pdisk.png', 'cafap-db3pnet.png', 'cafap-db3pnginx.png',
              'cafap-db3pram.png', 'cafap-db3ptime.png', 'cafap-db4pcpu.png', 'cafap-db4pdisk.png', 'cafap-db4pnet.png',
              'cafap-db4pnginx.png', 'cafap-db4pram.png', 'cafap-db4ptime.png', 'cafap-db5pcpu.png',
              'cafap-db5pdisk.png', 'cafap-db5pnet.png', 'cafap-db5pnginx.png', 'cafap-db5pram.png',
              'cafap-db5ptime.png', 'cafap-deploy1pcpu.png', 'cafap-deploy1pdisk.png', 'cafap-deploy1pnet.png',
              'cafap-deploy1pnginx.png', 'cafap-deploy1pram.png', 'cafap-deploy1ptime.png', 'cafap-gw1pcpu.png',
              'cafap-gw1pdisk.png', 'cafap-gw1pnet.png', 'cafap-gw1pnginx.png', 'cafap-gw1pram.png',
              'cafap-gw1ptime.png', 'cafap-mon1pcpu.png', 'cafap-mon1pdisk.png', 'cafap-mon1pnet.png',
              'cafap-mon1pnginx.png', 'cafap-mon1pram.png', 'cafap-mon1ptime.png', 'cafap-nexus1pcpu.png',
              'cafap-nexus1pdisk.png', 'cafap-nexus1pnet.png', 'cafap-nexus1pnginx.png', 'cafap-nexus1pram.png',
              'cafap-nexus1ptime.png', 'cafap-router1pcpu.png', 'cafap-router1pdisk.png', 'cafap-router1pnet.png',
              'cafap-router1pnginx.png', 'cafap-router1pram.png', 'cafap-router1ptime.png', 'cafap-web1cpu.png',
              'cafap-web1disk.png', 'cafap-web1net.png', 'cafap-web1nginx.png', 'cafap-web1ram.png',
              'cafap-web1time.png', 'cafap-web2cpu.png', 'cafap-web2disk.png', 'cafap-web2net.png',
              'cafap-web2nginx.png', 'cafap-web2ram.png', 'cafap-web2time.png']

my_dict = dict(zip(servers, screenshot))

url = 'http://sm.mos.ru:8090/SM/9/rest/ditMFSMAPI'
headers = {'Authorization': 'Basic RWFpc3RFQjo0a1FDeGFLWEdLMjc='}

payload = {
    "ditMFSMAPI": {
        "Action": "getObjectList",
        "Filename": "Изменение",
        "ParamsNames": [
            "Поисковый запрос"
        ],
        "ParamsValues": [
            "(\"Поле: Статус\"=\"Зарегистрирован\")"
            " and (\"Поле: Сервис\"=\"Формирование отчётов о произошедших событиях\")"
            " and (\"Поле: Направление\"=\"Поддержка и сопровождение ЦАФАП\")"
        ]
    }
}
response = requests.post(url, headers=headers, json=payload)
json_data = response.json()
number = str(json_data['ditMFSMAPI']['Response'][1])
def load_images(my_dict):
    images_dict = {}
    for key, value in my_dict.items():
        graph = InlineImage(doc, value, width=Cm(14), height=Cm(8))
        images_dict[key] = graph
    return images_dict

images = load_images(my_dict)
context = {'number': number, 'emp_name': name, 'date': today_date, 'time': today_time, }
context.update(images)
doc.render(context)
file_name = f'form_cafap.docx'
doc.save(file_name)
