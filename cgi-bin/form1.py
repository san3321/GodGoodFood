#!/usr/bin/env python3
import cgi
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from io import BytesIO
import random
import sqlite3############





lat = "30.320404"

lon = "59.919115"
#Ключи запроса:
ll = lat + "," + lon #Координаты
spn = "0.2,0.2" #Область поиска. Протяженности указываются в градусах, представленных в виде десятичной дроби
text = "поесть"#Текст запроса
results = "250" #Количество возвразаемых результатов
rspn = "1" #Ограничить зону поиска заданным значением
apikey = "5c92e3f1-da73-4954-9231-5ad2cefe8fe2"

#Формирование запроса:
url = 'https://search-maps.yandex.ru/v1/?type=biz&lang=ru_RU&ll='+ll+'&spn='+spn+'&text='+text+'&apikey='+apikey+'&results='+results+'&rspn='+rspn
response = requests.get(url)#Отправляем запрос в Яндекс
data = response.json()

#Подсчёт мест:
number_of_places = data["properties"]["ResponseMetaData"]["SearchResponse"]["found"]#Определение количества найденых мест
if number_of_places > int(results):#чтобы не выйти за граници массива
    number_of_places = int(results)

#Запись резултатов поиска в массив:
places=[] #Создание массива
result_places = 0 #Чтобы считать хорошие места
for i in range(0,number_of_places):
    goodplace = 1
    x = data["features"][i]["properties"]["CompanyMetaData"]["Categories"]
    for item in x:
        if item["name"]=="Кальян-бар" or item["name"]=="Сауна":
            goodplace = 0
    if goodplace==1:
        if "Hours" in data["features"][i]["properties"]["CompanyMetaData"]:#Проверка, работает ли заведение сейчас
            if data["features"][i]["properties"]["CompanyMetaData"]["Hours"]["State"]["is_open_now"] == "1":
                places.append([])
                places[result_places].append(data["features"][i]["properties"]["id"])#1
                places[result_places].append(data["features"][i]["properties"]["name"])#2
                places[result_places].append(data["features"][i]["properties"]["description"])#3
                places[result_places].append(data["features"][i]["geometry"]["coordinates"][1])#4 Долгота
                places[result_places].append(data["features"][i]["geometry"]["coordinates"][0])#5 Широта

                if "url" in data["features"][i]["properties"]["CompanyMetaData"]:#Проверка, есть ли url в ответе
                    places[result_places].append(data["features"][i]["properties"]["CompanyMetaData"]["url"])
                else:
                    places[result_places].append("Нет сайта")

                if "Features" in data["features"][i]["properties"]["CompanyMetaData"]:
                    x = data["features"][i]["properties"]["CompanyMetaData"]["Features"]
                    places[result_places].append("Нет инфы")#6 Обед
                    places[result_places].append("Нет инфы")#7 Оплата кредиткой
                    places[result_places].append("Нет инфы")#8 Средний счёт
                    places[result_places].append("Нет инфы")#9 Завтрак
                    places[result_places].append("Нет инфы")#10 Тип кухни
                    places[result_places].append("Нет инфы")#11 Спец меню
                    places[result_places].append("Нет инфы")#12 Стоимость обеда
                    count = 0
                    for item in x:
                        if item['id']=='business_lunch':
                            places[result_places][6] = item['value']
                        if item['id']=='payment_by_credit_card':
                            places[result_places][7] = item['value']
                        if item['id']=='average_bill2':
                            places[result_places][8] = item['value']
                        if item['id']=='breakfast':
                            places[result_places][9] = item['value']
                        if item['id']=='type_cuisine':
                            places[result_places][10] = ''
                            y = data["features"][i]["properties"]["CompanyMetaData"]["Features"][count]["values"]
                            for item in y:
                                places[result_places][10] = places[result_places][10] + " " + item['value']
                        if item['id']=='special_menu':
                            places[result_places][11] = ''
                            y = data["features"][i]["properties"]["CompanyMetaData"]["Features"][count]["values"]
                            for item in y:
                                places[result_places][11] = places[result_places][11] + " " + item['value']
                        if item['id']=='business lunch price':
                            places[result_places][12] = item['value']
                        count = count + 1
                else:
                    places[result_places].append("Нет инфы")#Обед
                    places[result_places].append("Нет инфы")#Оплата кредиткой
                    places[result_places].append("Нет инфы")#Средний счёт
                    places[result_places].append("Нет инфы")#Завтрак
                    places[result_places].append("Нет инфы")#Тип кухни
                    places[result_places].append("Нет инфы")#Спец меню
                    places[result_places].append("Нет инфы")#Стоимость обеда
                if "Availabilities" in data["features"][i]["properties"]["CompanyMetaData"]["Hours"]:
                    x = data["features"][i]["properties"]["CompanyMetaData"]["Hours"]["Availabilities"]
                    places[result_places].append("")#13 Понедельник открытие
                    places[result_places].append("")#14 Понедельник закрытие                            
                    places[result_places].append("")#15 Вторник открытие
                    places[result_places].append("")#16 Вторник закрытие
                    places[result_places].append("")#17 Среда открытие
                    places[result_places].append("")#18 Среда закрытие
                    places[result_places].append("")#19 Четверг открытие
                    places[result_places].append("")#20 Четверг закрытие
                    places[result_places].append("")#21 Пятница открытие
                    places[result_places].append("")#22 Пятница закрытие
                    places[result_places].append("")#23 Суббота открытие
                    places[result_places].append("")#24 Суббота закрытие
                    places[result_places].append("")#25 Воскресенье открытие
                    places[result_places].append("")#26 Воскресенье закрытие
                    for item in x:
                        if "Everyday" in item:
                            places[result_places][13]=item["Intervals"][0]["from"]
                            places[result_places][14]=item["Intervals"][0]["to"]
                            places[result_places][15]=item["Intervals"][0]["from"]
                            places[result_places][16]=item["Intervals"][0]["to"]
                            places[result_places][17]=item["Intervals"][0]["from"]
                            places[result_places][18]=item["Intervals"][0]["to"]
                            places[result_places][19]=item["Intervals"][0]["from"]
                            places[result_places][20]=item["Intervals"][0]["to"]
                            places[result_places][21]=item["Intervals"][0]["from"]
                            places[result_places][22]=item["Intervals"][0]["to"]
                            places[result_places][23]=item["Intervals"][0]["from"]
                            places[result_places][24]=item["Intervals"][0]["to"]
                            places[result_places][25]=item["Intervals"][0]["from"]
                            places[result_places][26]=item["Intervals"][0]["to"]
                        else:
                            if "Monday" in item:
                                places[result_places][13]=item["Intervals"][0]["from"]
                                places[result_places][14]=item["Intervals"][0]["to"]
                            if "Tuesday" in item:
                                places[result_places][15]=item["Intervals"][0]["from"]
                                places[result_places][16]=item["Intervals"][0]["to"]
                            if "Wednesday" in item:
                                places[result_places][17]=item["Intervals"][0]["from"]
                                places[result_places][18]=item["Intervals"][0]["to"]
                            if "Thursday" in item:
                                places[result_places][19]=item["Intervals"][0]["from"]
                                places[result_places][20]=item["Intervals"][0]["to"]
                            if "Friday" in item:
                                places[result_places][21]=item["Intervals"][0]["from"]
                                places[result_places][22]=item["Intervals"][0]["to"]
                            if "Saturday" in item:
                                places[result_places][23]=item["Intervals"][0]["from"]
                                places[result_places][24]=item["Intervals"][0]["to"]
                            if "Sunday" in item:
                                places[result_places][25]=item["Intervals"][0]["from"]
                                places[result_places][26]=item["Intervals"][0]["to"]
                if "ExperimentalMetaData" in data["features"][i]["properties"]:
                    x = data["features"][i]["properties"]["ExperimentalMetaData"]["ExperimentalStorage"]
                    num = 27
                    for item in x:
                        if item["key"]=="advProductTitle":
                            places[result_places].append("")
                            places[result_places][num]=item["value"]
                        if item["key"]=="advProductPrice":
                            places[result_places].append("")
                            places[result_places][num+1]=item["value"]
                            num = num + 2
                    for i in range(27, num-2):
                        print (places[result_places][i])             
                print (" ")
                result_places = result_places + 1
                


#Фомирование ответа:
mesto = random.randint(0,(result_places - 1))#Рандомно определяем заведение
##print(places[mesto][1], places[mesto][2],places[mesto][3], places[mesto][4], places[mesto][11])
res = {"name": places[mesto][1], "address": places[mesto][2], "lat": places[mesto][3], "lon": places[mesto][4], "lunch": places[mesto][6], "credit_card": places[mesto][7], "average_bill": places[mesto][8], "breakfast": places[mesto][9]}
responseJS = json.dumps(res)#Подготовка JS




##conn = sqlite3.connect('DataBase.db')#Открытие базы
##cursor = conn.cursor()#Установка курсора
##
###ВЗапрос на внесение инфы
##cursor.execute('insert into Places values (Null, :name,:address);', {'name': places[mesto][1], 'address': places[mesto][2]})
##cursor.execute('insert into Places values (Null, :name,:address);', {'name': places[mesto+1][1], 'address': places[mesto+1][2]})
##
##
##conn.commit()#Сохраняем транзакцию
##
##
##for row in cursor.execute('SELECT Name, Address FROM Places ORDER BY Name'):
##    print(row)
##
##
####cursor.execute("SELECT Name, Address FROM Places ORDER BY Name")#Запрос инфы
####results = cursor.fetchall()#Получение результата запроса
####responseJS = json.dumps(results)
######parsed_string = json.loads(responseJS)
##
##conn.close()#Закрытие базы






#часы работы сделать hours - > Availabilities есть everyday



