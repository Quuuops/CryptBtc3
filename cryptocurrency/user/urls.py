from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import  LogoutView
from cryptocurrency import settings
from .views import *

urlpatterns = [
    path('registration', registr, name='registration'),
    path('authentication', user_login, name='authentication'),
    url(r'^Logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='Logout'),
    path('account/page/id=<int:id>', UserPage.as_view(), name='user_account'),
    path('account/change_password', password_change, name="change_password"),
    path('account/create_wallet', create_wallet, name="create_wallet"),
    path('account/buy_crypt', buy_crypt, name="buy_crypt"),
    path('account/sell_crypt', sell_crypt, name="sell_crypt"),
    path('account/wallet/transaction', wallet_transaction, name="wallet_transaction"),
    path('account/change_data', change_data, name="change_data"),
    path('account/transaction', UserTransaction.as_view(), name="transaction"),

]
