from django.urls import path
from .views import *
urlpatterns = [
    path('', Crypt_values.as_view(), name='home'),
    path('crypto_currency/api_crypt', Crypto_api.as_view(), name='api_crypt'),
]
