#!/usr/bin/env python3
import cgi
import html
import requests
import json
from collections import namedtuple

#Обработка ответа
def places_response(x):
    i = 0
    for i in range(x):
        places.append([])
        places[i].append(data["features"][i]["properties"]["id"])
        places[i].append(data["features"][i]["properties"]["name"])
        places[i].append(data["features"][i]["properties"]["description"])
        #places[i].append(data["features"][i]["properties"]["CompanyMetaData"]["url"])
        places[i].append(data["features"][i]["properties"]["CompanyMetaData"]["Hours"]["State"]["is_open_now"])
        places[i].append(data["features"][i]["geometry"]["coordinates"][1]) #Долгота
        places[i].append(data["features"][i]["geometry"]["coordinates"][0]) #Широта
      
form = cgi.FieldStorage()
places=[]

####Надо сделать динамический запрос!!!!!!!!!!!!!!!!!!!!!!!!!!!
url = 'https://search-maps.yandex.ru/v1/?type=biz&text=кафе&lang=ru_RU&apikey=5c92e3f1-da73-4954-9231-5ad2cefe8fe2&results=3'
response = requests.get(url)
data = response.json()

####Количество мест в ответе
number_of_places = data["properties"]["ResponseMetaData"]["SearchRequest"]["results"]

####Цикл записи мест
places_response(number_of_places)

##for r in places:
##    for e in r:
##        print(e)

#часы работы сделать hours - > Availabilities есть everyday
#Категории
#Специальное меню
#оплата картой
#завтрак
#Бизнес ланч
#Цена ланча
#уровень цен
#cрендний счёт
#Тип кухни

# обработка Блюд ("ExperimentalMetaData": {"ExperimentalStorage"

                    


####Выбор места
#Проверка на время работы


mesto=places[0][1] + ", " + places[0][2]

####Изменение страницы
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <title>GodGoodFood</title>
        </head>
        <body>""")

print("<h1>ВОТ СЮДА ИДЁШЬ:</h1>")
print("<p>{}</p>".format(mesto))



print("""</body>
        </html>""")


