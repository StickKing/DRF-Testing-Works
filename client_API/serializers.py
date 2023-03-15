from django.contrib.auth.models import User, Group
from drf_yasg import openapi
from .models import Client, Photo
from rest_framework import serializers
from PIL import Image

#Сериализатор для вывода информации о клиентах
class ClientGetSerialize(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
    pk = serializers.ReadOnlyField()
    #Вывлжу вместо id photo само фото 
    client_photo = serializers.ImageField(source="client_photo.photo_file")

#Сериализатор для добавления и изменения клиентов
class ClientSerialize(serializers.Serializer):
    #Поля модели клиентов
    name = serializers.CharField()
    surname = serializers.CharField()
    birthday = serializers.DateField()
    gender_choices = [('Мужчина', 'М'),
                      ('Женщина', 'Ж'),]
    gender = serializers.ChoiceField(gender_choices)
    client_photo = serializers.ImageField()

    #Поля для обрезания фотографии делаем их необязательными
    #Координаты начала обрезки
    image_X = serializers.IntegerField(min_value=0, required=False)
    image_Y = serializers.IntegerField(min_value=0, required=False)
    #Ширина и высота обрезки
    image_heigh = serializers.IntegerField(min_value=0, required=False)
    image_width = serializers.IntegerField(min_value=0, required=False)
    
    #Метод обработки данных для POST
    def create(self, validated_data):
        #Получаем фото из словаря и удаляем его
        photo = validated_data.pop('client_photo')

        #Проверяем указал ли пользователь данные для обрезки фото
        #Если не указал то записываем значение ноль в переменные
        x = validated_data.get('image_X', 0)
        y = validated_data.pop('image_Y', 0)
        
        new_photo = Photo.objects.create(photo_file=photo)
        
        #Открываем pillow фотографию
        photo_for_cropped = Image.open(new_photo.photo_file)
        #Определяем изначальный размер фото 
        origin_width, origin_heigh = photo_for_cropped.size
        #Проверяем указанные ширину и высоту фото
        heigh = validated_data.pop('image_heigh', origin_heigh)
        width = validated_data.pop('image_width', origin_width)
        
        #Если указан параметр ширины или высоты до обрезаем фото
        if heigh != origin_heigh or width != origin_width:
            
            photo_for_cropped = photo_for_cropped.crop((x, y, 
                                                        heigh + x, 
                                                        width + y))
            photo_for_cropped.save(new_photo.photo_file.path)


        #Добавляем нового клиента в БД
        new_client = Client.objects.create(**validated_data,
                                           client_photo=new_photo)

        #Возвращаем словать с изменёнными данными
        answer = new_client.__dict__
        answer['client_photo'] = new_client.client_photo.photo_file
        return answer
    
    #Метод обработки данных для PUT 
    #Данный метод предполагает что все данные об клиенте будут заполнены
    def update(self, instance, validated_data):
        #Заменяем данные на новые
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        #Заменяем фотографию и сохраняем её
        #instance.client_photo.photo_file = validated_data['client_photo']
        instance.client_photo.photo_file = validated_data.get('client_photo', instance.client_photo)
        instance.client_photo.save()
        instance.save()

        #Проверяем указал ли пользователь данные для обрезки фото
        #Если не указал то записываем значение ноль в переменные
        x = validated_data.get('image_X', 0)
        y = validated_data.pop('image_Y', 0)

        #Открываем pillow фотографию
        photo_for_cropped = Image.open(instance.client_photo.photo_file)
        #Определяем изначальный размер фото 
        origin_width, origin_heigh = photo_for_cropped.size
        #Проверяем указанные ширину и высоту фото
        heigh = validated_data.pop('image_heigh', origin_heigh)
        width = validated_data.pop('image_width', origin_width)
        
        #Если указан параметр ширины или высоты до обрезаем фото
        if heigh != origin_heigh or width != origin_width:
            #Обрезаю фотографию
            photo_for_cropped = photo_for_cropped.crop((x, y, 
                                                        heigh + x, 
                                                        width + y))
            #Сохраняем обрезаную фотографию
            photo_for_cropped.save(instance.client_photo.photo_file.path)


        #Возвращаем словать с изменёнными данными
        answer = instance.__dict__
        answer['client_photo'] = instance.client_photo.photo_file
        return answer

#Сериализатор для регистрации клиента
class ClientRegisterSerializer(ClientSerialize):
    
    #Поля для регистрации клиента как пользователя
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        #Получаем фото из словаря и удаляем его
        photo = validated_data.pop('client_photo')

        #Проверяем указал ли пользователь данные для обрезки фото
        #Если не указал то записываем значение ноль в переменные
        x = validated_data.get('image_X', 0)
        y = validated_data.pop('image_Y', 0)
        
        new_photo = Photo.objects.create(photo_file=photo)
        
        #Открываем pillow фотографию
        photo_for_cropped = Image.open(new_photo.photo_file)
        #Определяем изначальный размер фото 
        origin_width, origin_heigh = photo_for_cropped.size
        #Проверяем указанные ширину и высоту фото
        heigh = validated_data.pop('image_heigh', origin_heigh)
        width = validated_data.pop('image_width', origin_width)
        
        #Если указан параметр ширины или высоты до обрезаем фото
        if heigh != origin_heigh or width != origin_width:
            
            photo_for_cropped = photo_for_cropped.crop((x, y, 
                                                        heigh + x, 
                                                        width + y))
            photo_for_cropped.save(new_photo.photo_file.path)

        #Записываем пользовательский логин пароль и удаляем его из словаря
        new_username = validated_data.pop('username')
        new_password = validated_data.pop('password')

        #Создаём нового пользователя django
        new_user = User.objects.create(username=new_username,
                                        password=new_password)
            
        #Проверяем существование группы clients или создаём её
        group, gp_exists = Group.objects.get_or_create(name='Clients')

        new_user.groups.add(group)

        #Добавляем нового клиента в БД
        new_client = Client.objects.create(**validated_data,
                                            client_photo=new_photo)

        #Возвращаем словать с изменёнными данными
        answer = new_client.__dict__
        answer['client_photo'] = new_client.client_photo.photo_file
        return answer


#Сериализатор для преобразования модели фотографий 
class PhotoSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'