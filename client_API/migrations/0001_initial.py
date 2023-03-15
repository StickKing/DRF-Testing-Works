# Generated by Django 4.1.7 on 2023-03-10 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_file', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=40)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(choices=[('Мужчина', 'М'), ('Женщина', 'Ж')], default='Мужчина', max_length=7)),
                ('client_photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='client_API.photo')),
            ],
        ),
    ]
