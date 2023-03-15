from django.db import models
from django.contrib.auth.models import User

#Модель для фото
class Photo(models.Model):
    #Поле фото
    photo_file = models.ImageField(upload_to='client-photo/')

    #Переопределяю метод str для более информативной работы в web-интерфейсе админки
    def __str__(self):
        return self.photo_file.__str__()

#Определяю модель клиента
class Client(models.Model):
    #Имя клиента
    name = models.CharField(max_length=30)
    #Фамилия
    surname = models.CharField(max_length=40)
    #Дата рождения
    birthday = models.DateField()
    #Пол
    gender_choices = [('Мужчина', 'М'),
                      ('Женщина', 'Ж'),]
    gender = models.CharField(max_length=7, choices=gender_choices, default='Мужчина')

    #Связываем модели связью один к одному
    client_photo = models.OneToOneField(Photo, on_delete=models.CASCADE, primary_key=True)

    #Связываем модель с встроеной моделью User
    client_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    #Переопределяю метод str для более информативной работы в web-интерфейсе админки
    def __str__(self):
        return f"{self.name} {self.surname}"