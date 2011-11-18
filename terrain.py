from lettuce import *

from simpleauth.db import create_schema

from simpleauth.setup import (setup_database,
                              setup_mail,
                              setup_dummy_mail)


@before.all
def before_all_setup_database():
   setup_database('sqlite3', ':memory:')
   #setup_mail('host', 'user', 'password', use_tls=False, port=587)
   setup_dummy_mail()

   create_schema()
