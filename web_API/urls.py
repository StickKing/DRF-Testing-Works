from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from client_API.views import *
from weather_API.views import *
from daemon_API.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Client Weather and other API",
      default_version='v1',
      description="Тестовое задание",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mainsample@yandex.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    
    path('api/client/', ClientView.as_view()),
    path('api/client/register/', ClientRegisterView.as_view()),
    path('api/weather/', WeatherView.as_view()),
    path('api/daemon/', DaemonView.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
