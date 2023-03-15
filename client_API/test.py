from requests import get

from requests import get as req_get

#Запрашиваю координаты указанного города на русском языке
responce = req_get('https://geocoding-api.open-meteo.com/v1/search?name=Москва&language=ru&count=1')
if responce.status_code == 200 and 'results' in responce.json():
    json_responce = responce.json()['results'][0]
    latitude = json_responce['latitude']
    longitude = json_responce['longitude']
    country = json_responce['country']

    responce = req_get(f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2023-01-06&end_date=2023-01-06&daily=temperature_2m_mean,precipitation_sum,rain_sum,snowfall_sum&timezone=auto')
    if responce.status_code == 200 and 'daily' in responce.json():
        json_responce = responce.json()['daily']
        weather_info = {'Город': country, 
                        'Дата': json_responce['time'][0], 
                        'Температура': f"{json_responce['temperature_2m_mean'][0]} °C", 
                        'Сумма выпавших осадков': f"{json_responce['precipitation_sum'][0]} мм",
                        'Сумма выпавшего дождя': f"{json_responce['precipitation_sum'][0]} мм",
                        'Сумма выпавшиего снега': f"{json_responce['snowfall_sum'][0]} см"}
        print(weather_info)
    else:
        print({'Error': 'Что-то пошло не так'})
else:
    print({'Error': 'Введены не корректные данные'})


responce = req_get('https://geocoding-api.open-meteo.com/v1/search?name=йцу&language=ru&count=1')
json_responce = type(responce.json())
print(json_responce)