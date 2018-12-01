#!/usr/bin/env python3
import cgi
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
from io import BytesIO
import random
import sqlite3





lat = "30.349281"

lon = "59.944639"
#Ключи запроса:
ll = lat + "," + lon #Координаты
spn = "0.5,0.5" #Область поиска. Протяженности указываются в градусах, представленных в виде десятичной дроби
text = "поесть"#Текст запроса
results = "1500" #Количество возвразаемых результатов
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
    goodplace = 0
    x = data["features"][i]["properties"]["CompanyMetaData"]["Categories"]
    for item in x:
        if item["name"]=="Кальян-бар" or item["name"]=="Сауна":
            goodplace = 0
        else:
            if "Hours" in data["features"][i]["properties"]["CompanyMetaData"] and "Availabilities" in data["features"][i]["properties"]["CompanyMetaData"]["Hours"] and "Features" in data["features"][i]["properties"]["CompanyMetaData"]:
                goodplace = 1
    if goodplace==1:
        places.append([])
        places[result_places].append(data["features"][i]["properties"]["id"])#0
        places[result_places].append(data["features"][i]["properties"]["name"])#1
        places[result_places].append(data["features"][i]["properties"]["description"])#2
        places[result_places].append(data["features"][i]["geometry"]["coordinates"][1])#3 Долгота
        places[result_places].append(data["features"][i]["geometry"]["coordinates"][0])#4 Широта
        if "url" in data["features"][i]["properties"]["CompanyMetaData"]:#Проверка, есть ли url в ответе
            places[result_places].append(data["features"][i]["properties"]["CompanyMetaData"]["url"])#5
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
                    bill = str(item['value'])
                    len_bill = len(bill)
                    z = bill.find("тыс.р",0,len_bill) 
                    if z!=-1:
                        places[result_places][8] = "Нет инфы"
                    else:
                        z = bill.find("г",0,len_bill) 
                        if z!=-1:
                            places[result_places][8] = "Нет инфы"
                        else:
                            bill = bill[0:len_bill-2]
                            z = bill.find("–",0,len_bill)
                            if z!=-1:
                                bill_number_1 = bill[0:z]
                                bill_number_2 = bill[z+1:len_bill-2]
                                bill_result = int((int(bill_number_1) + int(bill_number_2))/2)
                            else:
                                z = bill.find("о",0,len_bill-2)
                                if z!=-1:
                                    bill_result = int(bill[3:len_bill-2])
                                else:
                                    bill_result = int (bill)
                            places[result_places][8] = bill_result
                if item['id']=='breakfast':
                    places[result_places][9] = item['value']
                if item['id']=='type_cuisine':
                    places[result_places][10] = str(i)
                if item['id']=='special_menu':
                    places[result_places][11] = str(i)
                if item['id']=='business lunch price':
                    places[result_places][12] = item['value']
                count = count + 1
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
                        if "TwentyFourHours" in item:
                            places[result_places][13]="24h"
                            places[result_places][14]="24h"
                            places[result_places][15]="24h"
                            places[result_places][16]="24h"
                            places[result_places][17]="24h"
                            places[result_places][18]="24h"
                            places[result_places][19]="24h"
                            places[result_places][20]="24h"
                            places[result_places][21]="24h"
                            places[result_places][22]="24h"
                            places[result_places][23]="24h"
                            places[result_places][24]="24h"
                            places[result_places][25]="24h"
                            places[result_places][26]="24h"
                        else: 
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
                            if "TwentyFourHours" in item:
                                places[result_places][13]="24h"
                                places[result_places][14]="24h"
                            else:
                                places[result_places][13]=item["Intervals"][0]["from"]
                                places[result_places][14]=item["Intervals"][0]["to"]
                        if "Tuesday" in item:
                            if "TwentyFourHours" in item:
                                places[result_places][15]="24h"
                                places[result_places][16]="24h"
                            else:
                                places[result_places][15]=item["Intervals"][0]["from"]
                                places[result_places][16]=item["Intervals"][0]["to"]
                        if "Wednesday" in item:
                            if "TwentyFourHours" in item:
                                places[result_places][17]="24h"
                                places[result_places][18]="24h"
                            else:
                                places[result_places][17]=item["Intervals"][0]["from"]
                                places[result_places][18]=item["Intervals"][0]["to"]
                        if "Thursday" in item:
                            if "TwentyFourHours" in item:
                                places[result_places][19]="24h"
                                places[result_places][20]="24h"
                            else:
                                places[result_places][19]=item["Intervals"][0]["from"]
                                places[result_places][20]=item["Intervals"][0]["to"]
                        if "Friday" in item:
                            if "TwentyFourHours" in item:

                                places[result_places][21]="24h"
                                places[result_places][22]="24h"
                            else:
                                places[result_places][21]=item["Intervals"][0]["from"]
                                places[result_places][22]=item["Intervals"][0]["to"]
                        if "Saturday" in item:
                            if "TwentyFourHours" in item:
                                places[result_places][23]="24h"
                                places[result_places][24]="24h"
                            else:
                                places[result_places][23]=item["Intervals"][0]["from"]
                                places[result_places][24]=item["Intervals"][0]["to"]
                        if "Sunday" in item:
                            if "TwentyFourHours" in item:
                                places[result_places][25]="24h"
                                places[result_places][26]="24h"
                            else:
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
        result_places = result_places + 1
                
conn = sqlite3.connect('DataBase.db')#Открытие базы
cursor = conn.cursor()#Установка курсора
for i in range(0,result_places - 1):
    if places[i][6]!="Нет инфы" and places[i][7]!="Нет инфы" and places[i][8]!="Нет инфы":#проверка, указана ли инфа по карте и по обеду, среднем счёте
        if places[i][6]==False or (places[i][6]==True and places[i][12]!="Нет инфы"):
            #Загрузка видов кухни
            if places[i][10]!="Нет инфы" and "Features" in data["features"][i]["properties"]["CompanyMetaData"]:
                x = data["features"][int(places[i][10])]["properties"]["CompanyMetaData"]["Features"]
                count = 0
                for item in x:
                    if item['id']=='type_cuisine':
                        y = data["features"][int(places[i][10])]["properties"]["CompanyMetaData"]["Features"][count]["values"]
                        places[i][10] = ""
                        for item in y:
                            cursor.execute('INSERT OR IGNORE INTO Cousine_category (Name) VALUES (:name)',{"name": item['value']})
                            cursor.execute('SELECT ID FROM Cousine_category WHERE Name =:name',{'name': item['value']})
                            results = cursor.fetchall()
                            places[i][10] = places[i][10] + str(results[0][0]) + ", "                    
                    count = count + 1
            #Загрузка Особого меню
            if places[i][11]!="Нет инфы" and "Features" in data["features"][i]["properties"]["CompanyMetaData"]:
                x = data["features"][int(places[i][11])]["properties"]["CompanyMetaData"]["Features"]
                count = 0
                for item in x:
                    if item['id']=='special_menu':
                        y = data["features"][int(places[i][11])]["properties"]["CompanyMetaData"]["Features"][count]["values"]
                        places[i][11] = ""
                        for item in y:
                            cursor.execute('INSERT OR IGNORE INTO Special_Cousine (Name) VALUES (:name)',{"name": item['value']})
                            cursor.execute('SELECT ID FROM Special_Cousine WHERE Name =:name',{'name': item['value']})
                            results = cursor.fetchall()
                            places[i][11] = places[i][11] + str(results[0][0]) + ", "                    
                    count = count + 1
            dishes = ""
            #Загрузка блюд
            if len(places[i])>27:
                num = 27
                for j in range(0,int((len(places[i])-26)/2)):
                    cursor.execute('INSERT INTO Dish VALUES (Null,:name, "", "", "", :cost, :restID, "", "", "")',{"name":places[i][num], "cost":places[i][num+1], "restID":i})
                    cursor.execute('SELECT ID FROM Dish WHERE Name =:name',{'name': places[i][num]})
                    results = cursor.fetchall()
                    dishes = dishes + str(results[0][0]) + ", "
                    num = num + 2
            #Загруpка ретсорана        
            cursor.execute('''INSERT INTO Restourants VALUES
        (:i,:name,:address, :lat, :lon,"", :lunch, :lunch_cost, :breakfast, :breakfast_cost, :card, :bill, :cousine,
        :special, :dishes, :url, :mon_o, :mon_c, :tue_o, :tue_c, :wed_o, :wed_c, :tho_o, :tho_c, :fr_o, :fr_c, :sat_o, :sat_c, :sun_o, :sun_c)''',
                           {"i": i, "name":places[i][1], "address":places[i][2], "lat":places[i][3], "lon":places[i][4], "lunch":places[i][6],
                            "lunch_cost":places[i][12], "breakfast":places[i][9], "breakfast_cost":"", "card":places[i][7], "bill":places[i][8],
                            "cousine":places[i][10], "special":places[i][11], "dishes":dishes, "url":places[i][5], "mon_o":places[i][13],
                            "mon_c":places[i][14], "tue_o":places[i][15], "tue_c":places[i][16], "wed_o":places[i][17], "wed_c":places[i][18],
                            "tho_o":places[i][19], "tho_c":places[i][20], "fr_o":places[i][21], "fr_c":places[i][22], "sat_o":places[i][23],
                            "sat_c":places[i][24], "sun_o":places[i][25], "sun_c":places[i][26]})


conn.commit()#Сохраняем транзакцию
conn.close()#Закрытие базы










##cursor.execute("SELECT Name, Address FROM Places ORDER BY Name")#Запрос инфы
##results = cursor.fetchall()#Получение результата запроса
##responseJS = json.dumps(results)
####parsed_string = json.loads(responseJS)


    

###Фомирование ответа:
##mesto = random.randint(0,(result_places - 1))#Рандомно определяем заведение
####print(places[mesto][1], places[mesto][2],places[mesto][3], places[mesto][4], places[mesto][11])
##res = {"name": places[mesto][1], "address": places[mesto][2], "lat": places[mesto][3], "lon": places[mesto][4], "lunch": places[mesto][6], "credit_card": places[mesto][7], "average_bill": places[mesto][8], "breakfast": places[mesto][9]}
##responseJS = json.dumps(res)#Подготовка JS






