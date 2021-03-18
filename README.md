Description of the site
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