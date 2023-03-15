from rest_framework import viewsets, permissions, status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from .serializers import ClientGetSerialize, PhotoSerialize, ClientSerialize, ClientRegisterSerializer
from .models import Client, Photo
from .swagger_schema import *


#Представление клиентов
class ClientView(APIView):
    #Указываем параметры авторизации
    permission_classes = [permissions.IsAuthenticated]
    #Указываем аутентификацию через JWT
    authentication_classes = [JWTAuthentication]
    
    #Метод GET запроса
    @swagger_auto_schema(operation_description="Вывод информации обо всех клиентах.",
                         responses=client_GET_responce)
    def get(self, request):
        queryset = Client.objects.all()
        serializer = ClientGetSerialize(instance=queryset,
                                     many=True,
                                     context={'request': request})
        return Response(serializer.data)

    #Метод POST запроса
    @swagger_auto_schema(operation_description="""
    Добавление клиента производится при передачи всех полей модели клиента.
    Для осуществления обрезки фото можно указать координаты X,Y - место с которого будет 
    производиться обрезка и image_width, image_height - ширина и длина на которые мы обрежем фото.
    Обрезка производится только при условии, пользователь ввёл ширину или длину желаемой обрезки""",
    request_body=client_POST_request)
    def post(self, request, formate=None):
        serializer = ClientSerialize(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    #Метод PUT
    @swagger_auto_schema(operation_description="Изменение клиента производится только при передаче всех полей модели и ID клиента",
                         request_body=client_PUT_request)
    def put(self, request):
        pk = request.data.get('id', None)
        if not pk:
            return Response({"Error": "Изменение не произведено"})
        try:
            instance = Client.objects.get(pk=pk)
        except:
            return Response({"Error": "Объект не найден"})
        serializer = ClientSerialize(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    
    #Метод DELETE
    @swagger_auto_schema(operation_description="Для удаления клиента необходимо указать его ID. \nВо время операции удаляется как клиент так и фотография привязанная к нему",
                         request_body=client_DELETE_request)
    def delete(self, request):
        pk = request.data.get('id', None)
        if not pk:
            return Response({"Error": "Укажите ID удаляемого клиента"})
        try:
            instance = Client.objects.get(pk=pk)
        except:
            return Response({"Error": "Объект не найден"})
        #Удаляем фото клиента
        instance.client_photo.delete()
        #Удаляем самого клиента
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Представление регистрации клиента
class ClientRegisterView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(operation_description="""Регистрация клиента происходит подобно запросу POST api/client/
    за тем исключением, что так же передаются значения username и password для регистрации пользователя в системе""",
                         request_body=client_register_POST_request)
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(username=request.data['username']).exists():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'Пользователь с таким именем (username) уже существует'}, status=status.HTTP_403_FORBIDDEN)

    

@swagger_auto_schema(auto_schema=None)
#Представление фото
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerialize
    #Указываем параметры авторизации
    permission_classes = [permissions.IsAuthenticated]
    #Указываем аутентификацию через JWT
    authentication_classes = [JWTAuthentication]



