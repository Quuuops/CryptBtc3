from django.shortcuts import render
from django.views.generic import ListView
from requests import Session
import json
from .models import Crypt
import datetime


class Crypt_values(ListView):
    model = Crypt
    context_object_name = 'crypt'
    template_name = 'crypto_course/crypto_value.html'
    context = {'crypt': 'crypt',
               }
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        return Crypt.objects.all()


class Crypto_api(ListView):
    template_name = 'crypto_course/api_crypt.html'
    model = Crypt
    extra_context = {'title': 'Курс валют'}
    context_object_name = 'crypt'

    def get_queryset(self):
        return Crypt.objects.all()