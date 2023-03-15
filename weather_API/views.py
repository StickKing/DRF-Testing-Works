from rest_framework.generics import RetrieveAPIView
from requests import get as req_get
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import WeatherSerializer
from .swagger_schema import *

class WeatherView(RetrieveAPIView):
    @swagger_auto_schema(operation_description="""
    Данный запрос под капотом производит обращение к API https://geocoding-api.open-meteo.com.
    Первое обращение возвращает долготу и широту указанного города, второй запрос уже 
    по полученным данным запрашивает информацию о погоде.""",
    responses=weather_GET_responce)
    def get(self, request):
        #Преобразовываем данные и проверяем их корректность
        serializer = WeatherSerializer(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        #Запрашиваю координаты указанного города на русском языке
        responce = req_get(f"https://geocoding-api.open-meteo.com/v1/search?name={serializer.data['city']}&language=ru&count=1")
        #Проверяем корректность выполнения запроса
        if responce.status_code == 200 and 'results' in responce.json():
            json_responce = responce.json()['results'][0]
            latitude = json_responce['latitude']
            longitude = json_responce['longitude']
            country = json_responce['country']
            city = json_responce['name']

            #Запрашиваем погоду по координатам и дате
            responce = req_get(f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={serializer.data['date']}&end_date={serializer.data['date']}&daily=temperature_2m_mean,precipitation_sum,rain_sum,snowfall_sum&timezone=auto")
            #Проверяем корректность выполнения запроса
            if responce.status_code == 200 and 'daily' in responce.json():
                json_responce = responce.json()['daily']
                #Формируем ответ
                weather_info = {'Город': city,
                                'Страна': country,
                                'Дата': json_responce['time'][0], 
                                'Температура': f"{json_responce['temperature_2m_mean'][0]} °C", 
                                'Сумма выпавших осадков': f"{json_responce['precipitation_sum'][0]} мм",
                                'Сумма выпавшего дождя': f"{json_responce['precipitation_sum'][0]} мм",
                                'Сумма выпавшиего снега': f"{json_responce['snowfall_sum'][0]} см"}
                return Response(weather_info)
            else:
                return Response({'Error': 'Что-то пошло не так'})
        else:
            #Если введены некорректные данные возвращаем ошибку
            return Response({'Error': 'Введены не корректные данные'})
