from drf_yasg import openapi
from rest_framework import status


#Определяем схемы для swagger

client_POST_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя клиента'),
        'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия клиента'),
        'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='Дата рождения'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Пол клиента'),
        'client_photo': openapi.Schema(type=openapi.TYPE_FILE, description='Фото клиента'),
        'image_X': openapi.Schema(type=openapi.TYPE_INTEGER, description='Координата X'),
        'image_Y': openapi.Schema(type=openapi.TYPE_INTEGER, description='Координата X'),
        'image_heigh': openapi.Schema(type=openapi.TYPE_INTEGER, description='Высота обрезки'),
        'image_width': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ширина обрезки'),
    },
    required=['name', 'surname', 'birthday', 'gender', 'client_photo']
)

client_PUT_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID клиента'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя клиента'),
        'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия клиента'),
        'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='Дата рождения'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Пол клиента'),
        'client_photo': openapi.Schema(type=openapi.TYPE_FILE, description='Фото клиента'),
        'image_X': openapi.Schema(type=openapi.TYPE_INTEGER, description='Координата X'),
        'image_Y': openapi.Schema(type=openapi.TYPE_INTEGER, description='Координата X'),
        'image_heigh': openapi.Schema(type=openapi.TYPE_INTEGER, description='Высота обрезки'),
        'image_width': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ширина обрезки'),
    },
    required=['id', 'name', 'surname', 'birthday', 'gender', 'client_photo']
)

client_DELETE_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID клиента")
    },
    required=['id']
)

#client_POST_params = openapi.Parameter('client_photo', in_=openapi.IN_QUERY, type=openapi.TYPE_FILE)
#client_GET_params = openapi.Parameter('Authorization', in_=openapi.IN_QUERY, type=openapi.IN_HEADER)

client_register_POST_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя клиента'),
        'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия клиента'),
        'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='Дата рождения'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Пол клиента'),
        'client_photo': openapi.Schema(type=openapi.TYPE_FILE, description='Фото клиента'),
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Логин клиента'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль клиента'),
        'image_X': openapi.Schema(type=openapi.TYPE_INTEGER, description='Координата X'),
        'image_Y': openapi.Schema(type=openapi.TYPE_INTEGER, description='Координата X'),
        'image_heigh': openapi.Schema(type=openapi.TYPE_INTEGER, description='Высота обрезки'),
        'image_width': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ширина обрезки'),
    },
    required=['name', 'surname', 'birthday', 'gender', 'client_photo', 'username', 'password']
)

client_GET_responce = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID клиента'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя клиента'),
            'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия клиента'),
            'birthday': openapi.Schema(type=openapi.FORMAT_DATE, description='Дата рождения'),
            'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Пол клиента'),
            'client_photo': openapi.Schema(type=openapi.TYPE_FILE, description='Фото клиента'),
        },
        read_only = ['pk']
    ),
}

