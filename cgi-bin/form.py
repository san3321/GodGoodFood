#!/usr/bin/env python3
import cgi
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from io import BytesIO



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
        self.places_response(body) #Обработка запроса
        
    def places_response(self,res):
        res = res.decode('utf-8')
        parsed_string = json.loads(res) #Парсим полученные координаты
        lat = str(parsed_string["lon"])
        lon = str(parsed_string["lat"])
        #Ключи запроса
        ll = lat + "," + lon #Координаты
        spn = "0.2,0.2" #Область поиска. Протяженности указываются в градусах, представленных в виде десятичной дроби
        text = "поесть"#Текст запроса
        results = "150" #Количество возвразаемых результатов
        apikey = "5c92e3f1-da73-4954-9231-5ad2cefe8fe2"
        #Формирование запроса
        url = 'https://search-maps.yandex.ru/v1/?type=biz&lang=ru_RU&ll='+ll+'&spn='+spn+'&text='+text+'&apikey='+apikey+'&results='+results
        response = requests.get(url)#Отправляем запрос в Яндекс
        data = response.json()
        number_of_places = data["properties"]["ResponseMetaData"]["SearchRequest"]["results"]#Определение количества найденых мест
        places=[]
        
        
        #Запись резултатов поиска в массив
        for i in range(0,number_of_places):
            places.append([])               
##            key = "hotels"#Проверка, гостиница ли?
##            if key in data["features"][i]["properties"]["CompanyMetaData"]["Categories"]:
##                print(ДА, data["features"][i]["properties"]["class"])
##            key = "Кальян-бар"#Проверка, кальянная ли?
##            if key in data["features"][i]["properties"]["CompanyMetaData"]["Categories"]:
##                print(ДА, data["features"][i]["properties"]["name"])
##             for name in data[



            key = "Hours"
            if key in data["features"][i]["properties"]["CompanyMetaData"]:#Проверка, работает ли заведение сейчас
                if data["features"][i]["properties"]["CompanyMetaData"]["Hours"]["State"]["is_open_now"] == "1":
                    places[i].append(data["features"][i]["properties"]["id"])
                    places[i].append(data["features"][i]["properties"]["name"])
                    places[i].append(data["features"][i]["properties"]["description"])
                    
                    key = "url"#Проверка, есть ли url в ответе
                    if key in data["features"][i]["properties"]["CompanyMetaData"]:
                        places[i].append(data["features"][i]["properties"]["CompanyMetaData"]["url"])
                        
                    places[i].append(data["features"][i]["geometry"]["coordinates"][1]) #Долгота
                    places[i].append(data["features"][i]["geometry"]["coordinates"][0]) #Широта
        
        res = "{'name': '" + places[0][1] + "', 'address': '" + places[0][2] + "'}"#Формирование ответа
        self.wfile.write(res.encode('utf-8'))#Отправка ответа
        
        

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
print ("Server started. localhost: 8000", )
httpd.serve_forever()



# проверочка на пустые координаьы

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
#Делать проверку на гостиница/не гостиница

# обработка Блюд ("ExperimentalMetaData": {"ExperimentalStorage"

                    


####Выбор места








