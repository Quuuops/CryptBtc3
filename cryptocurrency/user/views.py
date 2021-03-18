from random import choice
from string import ascii_letters, digits
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserAuthForm, \
    ChangePasswordUser, CreateCryptoWallet, \
    BuyCrypt, SellCrypt, WalletTransaction
from crypto_course.models import Crypt, CryptoWallet
from .models import Profile, BuyTransactionCrypt, Sell_Transaction_Crypt, Wallet_Transaction_Crypt
from django.contrib.auth.hashers import make_password


def registr(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/registration.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserAuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = UserAuthForm()
    return render(request, 'user/auth.html', {"form": form})

class UserPage(ListView):
    model = User, Crypt, CryptoWallet
    template_name = 'user/account.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CryptoWallet.objects.all().filter(user_id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = User.objects.get(pk=self.kwargs['id'])
        return context


class UserTransaction(ListView):
    model = Sell_Transaction_Crypt, BuyTransactionCrypt, Wallet_Transaction_Crypt
    template_name = 'user/transaction.html'
    context_object_name = 'transaction'
    sale_transaction = Sell_Transaction_Crypt.objects.all()
    buy_transaction = BuyTransactionCrypt.objects.all()
    wallet_transaction = Wallet_Transaction_Crypt.objects.all()

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['id'] = User.objects.get(pk=self.kwargs['id'])
    #     return context

    def get_queryset(self):
        return Sell_Transaction_Crypt.objects.filter(from_user_id=self.request.user.id)


@login_required
def password_change(request):
    u = User.objects.get(username=request.user)
    user_password = User.objects.filter(id=request.user.id).values('password')
    if request.method == 'POST':
        form = ChangePasswordUser(data=request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_pass = request.POST.get("new_password")
            new_pass_rep = request.POST.get("new_password_repeat")
            if new_pass == new_pass_rep:
                if old_password != new_pass:
                    if check_password(old_password, user_password[0]['password']):
                        update_user = User.objects.filter(id=request.user.id).update(password=make_password(new_pass))
                        update_session_auth_hash(request, user=request.user.id)
                        return redirect('authentication')
                    else:
                        messages.error(request, 'Ваш нынешний пароль введен неверно!')
                        return redirect('change_password')
                else:
                    messages.error(request, 'Ваш старый и новый пароль должны отличаться!')
                    return redirect('change_password')

            else:
                messages.error(request, 'Повторный пароль отличается')
                return redirect('change_password')

    else:
        form = ChangePasswordUser()

    return render(request, 'user/change_password.html',
                  {'form': form, 'user': u})


@login_required
def create_wallet(request):
    objectlist = Crypt.objects.all().distinct().order_by('-price_crypt_dollar').select_related()
    if request.method == 'POST':
        crypt_id = request.POST['cryptocurrency']
        current_user = request.user

        new_wallet = CryptoWallet(crypt_id=crypt_id, wallet=''.join(choice(ascii_letters + digits) for i in range(33)),
                                  user_id=current_user.id)
        new_wallet.save()
        return redirect('page/id=%d' % request.user.id)
    else:
        form = CreateCryptoWallet()
        return render(request, 'user/create_wallet.html', {'form': form, 'objectlist': objectlist})


@login_required
def buy_crypt(request):
    objectlist = Crypt.objects.all().distinct().order_by('-price_crypt_dollar').select_related()
    if request.method == 'POST':
        form = BuyCrypt(data=request.POST)
        crypt_id = request.POST['crypt_id']
        pay_money = request.POST['money']
        wallet = request.POST['crypt_adress']
        profile_current_user_balance = Profile.objects.filter(user_id=request.user.id).values('user_balance')
        wallet_current_balance = CryptoWallet.objects.filter(wallet=wallet, crypt_id=crypt_id).values('value_crypt')
        current_course_crypt = Crypt.objects.filter(id=crypt_id).values('price_crypt_dollar')
        id_crypt_value = CryptoWallet.objects.filter(wallet=wallet).values('id')

        if form.is_valid():
            if (float(profile_current_user_balance[0]['user_balance']) - float(pay_money)) > 0:
                if len(wallet_current_balance) > 0:
                    user_transaction = BuyTransactionCrypt(from_user_value=pay_money,
                                                           to_crypt_value=float(pay_money) / float(
                                                               current_course_crypt[0]['price_crypt_dollar']),
                                                           from_user_id=request.user.id, to_crypt_id=crypt_id,
                                                           to_crypt_wallet_id=id_crypt_value[0]['id'])
                    user_transaction.save()
                    user_balance = Profile.objects.filter(user_id=request.user.id).update(
                        user_balance=float(profile_current_user_balance[0]['user_balance']) - float(pay_money))
                    wallet_balance = CryptoWallet.objects.filter(wallet=wallet, crypt_id=crypt_id).update(
                        value_crypt=float(wallet_current_balance[0]['value_crypt']) + (
                                float(pay_money) / float(current_course_crypt[0]['price_crypt_dollar'])))
                    messages.success(request, 'Заявка успешно оплачена')
                    return redirect('page/id=%d' % request.user.id)
                else:
                    messages.error(request, 'Кошелек не найден')
                return redirect('buy_crypt')
            else:
                messages.error(request, 'Недостаточно средств')
            return redirect('buy_crypt')

    else:
        form = BuyCrypt()
        return render(request, 'user/buy_crypt.html', {'form': form, 'objectlist': objectlist})


@login_required
def sell_crypt(request):
    objectlist = Crypt.objects.all().distinct().order_by('-price_crypt_dollar').select_related()
    if request.method == 'POST':
        form = SellCrypt(data=request.POST)
        crypt_id = request.POST['crypt_id']
        crypt_money = request.POST['crypt_value']
        wallet_address = request.POST['crypt_adress_sell']
        user_nick = request.POST['user_nick']
        self_user = request.POST.get('check_user_self', False)

        user_wallet_values = CryptoWallet.objects.filter(user_id=request.user.id, wallet=wallet_address,
                                                         crypt_id=crypt_id).values('value_crypt')
        current_crypt_course = Crypt.objects.filter(id=crypt_id).values('price_crypt_dollar')
        self_user_id_balance = Profile.objects.filter(user_id=request.user.id).values('user_balance')
        user_name = User.objects.filter(username=user_nick).values('id')
        user_seller_name = User.objects.get(id=request.user.id)
        crypt_id_trans = Crypt.objects.get(id=crypt_id)
        wallet_address_trans = CryptoWallet.objects.get(wallet=wallet_address)

        if form.is_valid():
            if len(user_wallet_values) > 0:
                if (float(user_wallet_values[0]['value_crypt']) - float(crypt_money)) > 0:
                    if self_user == 'on':
                        sell_transaction = Sell_Transaction_Crypt(from_user=user_seller_name, from_crypt=crypt_id_trans,
                                                                  from_crypt_wallet=wallet_address_trans,
                                                                  from_crypt_value=crypt_money,
                                                                  to_user=user_seller_name,
                                                                  to_value=float(crypt_money) * float(
                                                                      current_crypt_course[0]['price_crypt_dollar']))
                        sell_transaction.save()
                        update_value_crypt_money = CryptoWallet.objects.filter(wallet=wallet_address).update(
                            value_crypt=float(user_wallet_values[0]['value_crypt']) - float(crypt_money))
                        update_money_self_user_dollar = Profile.objects.filter(user_id=request.user.id).update(
                            user_balance=float(self_user_id_balance[0]['user_balance']) + (
                                    float(crypt_money) * float(current_crypt_course[0]['price_crypt_dollar'])))
                        messages.success(request, 'Заявка успешно оплачена')
                        return redirect('page/id=%d' % request.user.id)
                    elif self_user == False:
                        if len(user_name) > 0:
                            user_take_id = User.objects.get(id=user_name[0]['id'])

                            to_user = User.objects.filter(username=user_nick).values('id')
                            sell_transaction = Sell_Transaction_Crypt(from_user=user_seller_name,
                                                                      from_crypt=crypt_id_trans,
                                                                      from_crypt_wallet=wallet_address_trans,
                                                                      from_crypt_value=crypt_money,
                                                                      to_user=user_take_id,
                                                                      to_value=float(crypt_money) * float(
                                                                          current_crypt_course[0][
                                                                              'price_crypt_dollar']))
                            sell_transaction.save()
                            money_by_nickname_user = Profile.objects.filter(user_id=user_name[0]['id']).values(
                                'user_balance')
                            update_user_value_balance = CryptoWallet.objects.filter(wallet=wallet_address).update(
                                value_crypt=float(user_wallet_values[0]['value_crypt']) - float(crypt_money))
                            update_money_user_id_dollar = Profile.objects.filter(user_id=user_name[0]['id']).update(
                                user_balance=float(money_by_nickname_user[0]['user_balance']) + (
                                        float(crypt_money) * float(current_crypt_course[0]['price_crypt_dollar'])))
                            messages.success(request, 'Заявка успешно оплачена')
                            return redirect('page/id=%d' % request.user.id)
                        else:
                            messages.error(request, 'Неверный логин пользователя')
                            return redirect('sell_crypt')
                else:
                    messages.error(request, 'Недостаточно средств')
                    return redirect('sell_crypt')
            else:
                messages.error(request, 'Укажите ваш верный кошелек')
                return redirect('sell_crypt')
    else:
        form = SellCrypt
        return render(request, 'user/sell_crypt.html', {'form': form, 'objectlist': objectlist})


@login_required
def wallet_transaction(request):
    objectlist = Crypt.objects.all().distinct().order_by('-price_crypt_dollar')
    if request.method == 'POST':
        form = WalletTransaction(data=request.POST)
        wallet_transction_from_id = request.POST['crypt_from']
        crypt_adress_from = request.POST['crypt_adress_from']
        crypt_value_from = request.POST['crypt_value_from']
        crypt_adress_to = request.POST['crypt_adress_to']
        wallet_transction_to_id = request.POST['crypt_to']

        get_from_user_id = User.objects.get(id=request.user.id)
        get_from_crypt_id = Crypt.objects.get(id=wallet_transction_to_id)
        get_from_wallet = CryptoWallet.objects.filter(wallet=crypt_adress_from).values('id')
        get_from_wallet_id = CryptoWallet.objects.get(id=get_from_wallet[0]['id'])
        get_to_crypt_address = CryptoWallet.objects.filter(wallet=crypt_adress_to).values('user_id', 'crypt_id', 'id')
        get_user_to_id = User.objects.get(id=get_to_crypt_address[0]['user_id'])
        get_crypt_to_id = Crypt.objects.get(id=get_to_crypt_address[0]['crypt_id'])
        get_wallet_to_id = CryptoWallet.objects.get(id=get_to_crypt_address[0]['id'])

        get_wallet_current_value_from = CryptoWallet.objects.filter(wallet=crypt_adress_from,
                                                                    crypt_id=wallet_transction_from_id,
                                                                    user_id=request.user.id).values('value_crypt',
                                                                                                    'wallet')
        get_wallet_current_value_to = CryptoWallet.objects.filter(wallet=crypt_adress_to,
                                                                  crypt_id=wallet_transction_to_id).values(
            'value_crypt', 'wallet')
        get_crypto_course_from = Crypt.objects.filter(id=wallet_transction_from_id).values('price_crypt_dollar')
        get_crypto_course_to = Crypt.objects.filter(id=wallet_transction_to_id).values('price_crypt_dollar')

        if form.is_valid():
            if len(get_wallet_current_value_from) > 0:
                if len(get_wallet_current_value_to) > 0:
                    if float(get_wallet_current_value_from[0]['value_crypt']) - float(crypt_value_from) > 0:

                        add_transactions_wallet = Wallet_Transaction_Crypt(from_user=get_from_user_id,
                                                                           from_crypt=get_from_crypt_id,
                                                                           from_crypt_wallet=get_from_wallet_id,
                                                                           from_crypt_value=crypt_value_from,
                                                                           to_user=get_user_to_id,
                                                                           to_crypt=get_crypt_to_id,
                                                                           to_crypt_wallet=get_wallet_to_id,
                                                                           to_crypt_value=((float(
                                                                               crypt_value_from) * float(
                                                                               get_crypto_course_from[0][
                                                                                   'price_crypt_dollar'])) / float(
                                                                               get_crypto_course_to[0][
                                                                                   'price_crypt_dollar'])))
                        add_transactions_wallet.save()
                        update_value_transaction_wallet_from = CryptoWallet.objects.filter(wallet=crypt_adress_from,
                                                                                           crypt_id=wallet_transction_from_id).update(
                            value_crypt=float(get_wallet_current_value_from[0]['value_crypt']) - float(
                                crypt_value_from))
                        update_value_transaction_to_wallet = CryptoWallet.objects.filter(wallet=crypt_adress_to,
                                                                                         crypt_id=wallet_transction_to_id).update(
                            value_crypt=float(get_wallet_current_value_to[0]['value_crypt']) + ((float(
                                crypt_value_from) * float(get_crypto_course_from[0]['price_crypt_dollar'])) / float(
                                get_crypto_course_to[0]['price_crypt_dollar'])))
                        messages.success(request, 'Заявка успешно оплачена')
                        return redirect('/user/account/page/id=%d' % request.user.id)
                    else:
                        messages.error(request, 'Недостаточного стредств')
                        return redirect('wallet_transaction')
                else:
                    messages.error(request, 'Кошелек получателя не найден!')
                    return redirect('wallet_transaction')
            else:
                messages.error(request, 'Ваш кошелек не валиден!')
                return redirect('wallet_transaction')
    else:
        form = WalletTransaction
        return render(request, 'user/wallet_transaction.html', {'form': form, 'objectlist': objectlist})


@login_required
def change_data(request):
    if request.method == 'POST':
        if True:
            change_name = request.POST['name']
            change_lastname = request.POST['surname']
            change_email = request.POST['email']
            User.objects.filter(id=request.user.id).update(first_name=change_name, last_name=change_lastname,
                                                           email=change_email)
            messages.error(request, 'Данные успешно обновились!')
            return redirect('/user/account/page/id=%d' % request.user.id)

    else:
        return render(request, 'user/change_user_data.html')
