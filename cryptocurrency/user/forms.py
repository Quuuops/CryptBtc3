from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

import user
from crypto_course.models import CryptoWallet, Crypt


class UserAuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=True, min_length=2, max_length=25,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', required=True, min_length=2, max_length=25,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class ChangePasswordUser(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    new_password = forms.CharField(label='Новый Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_repeat = forms.CharField(label='Повторите новый пароль',
                                          widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = 'password'

    def clean_password(self):
        valid = self.user.check_password(self.cleaned_data['new_password'])
        if not valid:
            raise forms.ValidationError("Password Incorrect")
        return valid

    class Meta:
        model = User
        fields = 'password'


class CreateCryptoWallet(forms.Form):
    crypt = forms.ChoiceField(label='Выберите валюту', widget=forms.RadioSelect)

    class Meta:
        model = CryptoWallet
        fields = 'wallet'


class BuyCrypt(forms.Form):
    crypt_adress = forms.CharField(label='Адрес валюты', required=True, min_length=2, max_length=50,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    money = forms.DecimalField(label='Сумма в $', required=True, widget=forms.NumberInput(
        attrs={'minlength': 10, 'maxlength': 15, 'required': True, 'type': 'number', }))


class Meta:
    model = CryptoWallet
    fields = ('wallet', 'value_crypt')


class SellCrypt(forms.Form):
    crypt_adress_sell = forms.CharField(label='Адрес валюты', required=True, min_length=2, max_length=50,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    crypt_value = forms.DecimalField(label='Сумма', required=True, widget=forms.NumberInput(
        attrs={'minlength': 10, 'maxlength': 15, 'required': True, 'type': 'number', }))
    user_nick = forms.CharField(label='Никнейм', help_text='Необязательно', required=False, min_length=2, max_length=50,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    check_user_self = forms.BooleanField(label='Себе на счет', required=False)


class WalletTransaction(forms.Form):
    crypt_adress_from = forms.CharField(label='Адрес валюты', required=True, min_length=2, max_length=50,
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    crypt_value_from = forms.DecimalField(label='Сумма', required=True, widget=forms.NumberInput(
        attrs={'minlength': 10, 'maxlength': 15, 'required': True, 'type': 'number', }))
    crypt_adress_to = forms.CharField(label='Адрес валюты', required=True, min_length=2, max_length=50,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))


