from drf_yasg import openapi
from rest_framework import status


daemon_GET_responce = {
    status.HTTP_200_OK: openapi.TYPE_ARRAY
}