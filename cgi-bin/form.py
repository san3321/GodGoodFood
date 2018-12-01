#!/usr/bin/env python3
import cgi
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from io import BytesIO
import random
import sqlite3



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Server has been started')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = BytesIO()
        response.write(body)
        print(self.path)
        self.places_response(body) #Обработка запроса
        
    def places_response(self,res):
        res = res.decode('utf-8')
        parsed_string = json.loads(res) #Парсим полученные координаты
        lat = str(parsed_string["lon"])
        lon = str(parsed_string["lat"])
        
        #Ключи запроса:
        ll = lat + "," + lon #Координаты
        spn = "0.02,0.02" #Область поиска. Протяженности указываются в градусах, представленных в виде десятичной дроби
        text = "поесть"#Текст запроса
        results = "150" #Количество возвразаемых результатов
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
                        places[result_places].append(data["features"][i]["properties"]["id"])
                        places[result_places].append(data["features"][i]["properties"]["name"])
                        places[result_places].append(data["features"][i]["properties"]["description"])
                        places[result_places].append(data["features"][i]["geometry"]["coordinates"][1]) #Долгота
                        places[result_places].append(data["features"][i]["geometry"]["coordinates"][0]) #Широта
                        
                        if "url" in data["features"][i]["properties"]["CompanyMetaData"]:#Проверка, есть ли url в ответе
                            places[result_places].append(data["features"][i]["properties"]["CompanyMetaData"]["url"])
                        else:
                            places[result_places].append("Нет сайта")
                            
                        if "Features" in data["features"][i]["properties"]["CompanyMetaData"]:
                            x = data["features"][i]["properties"]["CompanyMetaData"]["Features"]
                            places[result_places].append("Нет инфы")#Обед
                            places[result_places].append("Нет инфы")#Оплата кредиткой
                            places[result_places].append("Нет инфы")#Средний счёт
                            places[result_places].append("Нет инфы")#Завтрак
                            places[result_places].append("Нет инфы")#Тип кухни
                            places[result_places].append("Нет инфы")#Спец меню
                            places[result_places].append("Нет инфы")#Стоимость обеда
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
                        result_places = result_places + 1

        

        #Фомирование ответа:
        mesto = random.randint(0, (result_places - 1))#Рандомно определяем заведение
        print(places[mesto][1], places[mesto][2],places[mesto][3], places[mesto][4], places[mesto][11])
        res = {"name": places[mesto][1], "address": places[mesto][2], "lat": places[mesto][3], "lon": places[mesto][4], "lunch": places[mesto][6], "credit_card": places[mesto][7], "average_bill": places[mesto][8], "breakfast": places[mesto][9]}
        responseJS = json.dumps(res)#Подготовка JS 
        self.wfile.write(responseJS.encode('utf-8'))#Отправка ответа
    
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print ("Server started. localhost: 8000", )
httpd.serve_forever()





#часы работы сделать hours - > Availabilities есть everyday

# обработка Блюд ("ExperimentalMetaData": {"ExperimentalStorage"

                    
####Выбор места








