Installation
============

    pip install -r requirements.txt


Run tests
=========

    lettuce tests/


Usage
=====

```python
from simpleauth.setup import *
from simpleauth.shortcuts import signup, activate, login
from simpleauth.exceptions import UserBlocked, UserIncorrectPassword


setup_database('sqlite3', 'dev.db')
setup_mail('mail.gmail.com', 'user@gmail.com', 'password', use_tls=True, port=587)


user = signup('test@example.com', 'password')

# ... You may receive an e-mail with your activation code
# but here we make this programatically

activate(user.pk, user.activation_code)

try:
    user = login('test@example.com', 'password')
except UserIncorrectPassword:
    print 'E-mail or password are invalid'
except UserBlocked:
    print 'You are blocked'
```
