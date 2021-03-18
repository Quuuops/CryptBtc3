Description of the site

Languages

    PYTHON(DJANGO 3.1.7)
    HTML5/CSS/JAVASCRIPT(BOOTSTRAP)
Other
  
    User redis / celery to automatically update crypto_course database

Requirements



    amqp==5.0.5
    anyjson==0.3.3
    asgiref==3.3.1
    bcrypt==3.2.0
    beautifulsoup4==4.9.3
    billiard==3.6.3.0
    celery==5.0.5
    certifi==2020.12.5
    cffi==1.14.5
    chardet==4.0.0
    click==7.1.2
    click-didyoumean==0.0.3
    click-plugins==1.1.1
    click-repl==0.1.6
    cryptography==3.4.6
    defusedxml==0.6.0
    Django==3.1.7
    django-allauth==0.44.0
    django-bootstrap3==14.2.0
    django-bootstrap4==2.3.1
    django-celery==3.3.1
    django-celery-beat==2.0.0
    django-celery-results==2.0.1
    django-debug-toolbar==3.2
    django-kombu==0.9.4
    django-moneyfield==0.2.1
    django-results==0.5.1
    django-timezone-field==4.1.1
    django-widget-tweaks==1.4.8
    docopt==0.6.2
    idna==2.10
    kombu==5.0.2
    mysqlclient==2.0.3
    oauthlib==3.1.0
    Pillow==8.1.0
    pip-tools==5.5.0
    pipreqs==0.4.10
    pkg-resources==0.0.0
    prompt-toolkit==3.0.17
    pycparser==2.20
    pycryptodome==3.10.1
    PyJWT==2.0.1
    python-crontab==2.5.1
    python-dateutil==2.8.1
    python3-openid==3.2.0
    pytz==2021.1
    redis==3.5.3
    requests==2.25.1
    requests-oauthlib==1.3.0
    six==1.15.0
    soupsieve==2.2
    sqlparse==0.4.1
    urllib3==1.26.3
    vine==5.0.0
    wcwidth==0.2.5
    yarg==0.1.9


Database

    MySQL

Database model

    User
    Crypt
    UserWalletCrypt
    TransactionSell
    TransactionBuy
    TransctionWallet
    ProfileUser




Created 2 user applications and cryptocurrencies

In the cryptocurrency application, the output of the course is implemented, thanks to Redis and celery, the database is automatically updated, thanks to the execution of the tasks specified in the code with a timer, the course is constantly updated and rewritten into the database.
 the main page of the site
In the users app:
- User registration, recording the entire database, hashing passwords Sha256 unique login, password verification, in case of an error, a redirect to registration is carried out
- Autoraziation of users, sessions, checking for compliance of the user and their password, logging into a personal account
- Creation of a unique wallet attached to the user and cryptocurrency links in the database.
When the wallet is created, it is displayed in the user profile
- Purchase of cryptocurrency, selection of the desired cryptocurrency, introduction of a wallet, the amount of replenishment in dollars. The base records the amount of received cryptocurrency to the user's wallet, and the purchase transaction is also recorded when sending.
Checking for the existence of a wallet for a given cryptocurrency, whether the user has enough funds
-Sale cryptocurrency
The sale is carried out either to oneself to the user's wallet, or it can be sent from the cryptocurrency to the user's balance in dollars by nickname.
If the checkbox is active, then the user replenishes his balance, if not, he will ask for a unique username, it is still recorded in the database, and the transaction for this sale is recorded
- Transfer between wallets
The user can transfer from the wallet to another cryptocurrency wallet, Currencies can be different, a recalculation is performed between the exchange rates, it is checked whether the wallet is sent to the user, who performs the operation, whether the wallet is obtained, the entered amount does not exceed the user's wallet balance, changes in the database and adds to transactions between wallets,
-Change Password
Each user can change his password, checks are made to compare the current password, whether the 2 fields of repeated passwords match, if matching, the password is hashed using the cipher sha256
-Changing user data
Updating a user's first name, last name or email
-Transactions
Each user can see transactions for the sale of currencies 