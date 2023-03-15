from drf_yasg import openapi
from rest_framework import status

weather_GET_responce = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'Город': openapi.Schema(type=openapi.TYPE_STRING),
            'Страна': openapi.Schema(type=openapi.TYPE_STRING),
            'Дата': openapi.Schema(type=openapi.FORMAT_DATE),
            'Температура': openapi.Schema(type=openapi.TYPE_STRING),
            'Сумма выпавших осадков': openapi.Schema(type=openapi.TYPE_STRING),
            'Сумма выпавшего дождя': openapi.Schema(type=openapi.TYPE_STRING),
            'Сумма выпавшиего снега': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
}