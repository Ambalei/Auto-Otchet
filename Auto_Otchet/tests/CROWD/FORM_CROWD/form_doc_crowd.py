from datetime import datetime
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
import requests
import json

doc = DocxTemplate('form_crowd_tpl.docx')

# Данные для заполнения шаблона
name = "Амбражевич А.В."
today_date = datetime.today().strftime("%d.%m.%Y")
today_time = datetime.today().strftime("%H:%M")

# Загружаем данные серверов из файла
with open('photos_dict.json', 'r') as file:
    photos_dict = json.load(file)

# Работа с API HPSM для получения номера ЗНИ

url = 'http://sm.mos.ru:8090/SM/9/rest/ditMFSMAPI'
headers = {'Authorization': 'Basic RWFpc3RFQjo0a1FDeGFLWEdLMjc='}

# Создаем тело запроса в формате JSON
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
            " and (\"Поле: Направление\"=\"Поддержка и сопровождение КП ПМ\")"
        ]
    }
}
# отправляем запрос
response = requests.post(url, headers=headers, json=payload)
json_data = response.json()
number = str(json_data['ditMFSMAPI']['Response'][1])
def load_images(my_dict):
    images_dict = {}
    for key, value in my_dict.items():
        graph = InlineImage(doc, value, width=Cm(14), height=Cm(8))
        images_dict[key] = graph
    return images_dict

images = load_images(photos_dict)
context = {'number': number, 'emp_name': name, 'date': today_date, 'time': today_time}
context.update(images)
doc.render(context)
file_name = f'form_crowd.docx'
doc.save(file_name)
