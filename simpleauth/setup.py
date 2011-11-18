from . import db
from .classes import DB, Mail


def setup_database(driver, name, user='', password='', host='', port=''):
    if db._connection:
        return

    DB.driver = driver
    DB.name = name
    DB.user = user
    DB.password = password
    DB.host = host
    DB.port = port

    db._connection = db.get_driver(driver).connect(name, user, password, host, port)


def setup_mail(host, host_user, host_password, use_tls=False, port=587):
    Mail.host = host
    Mail.host_user = host_user
    Mail.host_password = host_password
    Mail.use_tls = use_tls
    Mail.port = port


def setup_dummy_mail():
    Mail.is_dummy = True
