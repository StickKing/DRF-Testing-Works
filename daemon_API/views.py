from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from multiprocessing.pool import ThreadPool
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from psutil import virtual_memory, disk_usage
from datetime import date
from .swagger_schema import *
import json

#Представление API демона
class DaemonView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_description="Данный запрос возвращет данные об использовании RAM и дискового пространства",
                         responses=daemon_GET_responce)
    def get(self, request):
        #Функция собирающая информацию об использрвании RAM и дисков
        def MemoryJSONDaemon():
            disk_memory = [i / 1048576 for i in disk_usage('/')]
            RAM_memory = [i / 1048576 for i in virtual_memory()]
            #Преобразовываем данные в более читаемый вид
            json_items = [f"Total RAM = {RAM_memory[0]} Mb", f"Free RAM = {RAM_memory[1]} Mb",
                          f"Used RAM = {RAM_memory[3]} Mb", f"Total disk memory = {disk_memory[0]} Mb",
                          f"Used disk memory = {disk_memory[1]} Mb", f"Free disk memory = {disk_memory[2]} Mb",
                          f"Date of Verification {date.today()}"]
            #Преобразуем данные в JSON массив
            return json.dumps(json_items)
        pool = ThreadPool(processes=1)
        #Запускаем код в отдельном потоке
        result = pool.apply_async(MemoryJSONDaemon)
        #Возвращаем результат обратно 
        return Response(result.get())
    