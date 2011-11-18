from .utils import memoized
from .classes import DB, Column

from .exceptions import (DriverNotFound,
                         DBNotConnected)

_connection = None


def get_driver(driver):
    driver_path = 'drivers.%s_driver' % (driver,)
    try:
        return memoized(__import__)(driver_path, globals(), locals(), -1)
    except ImportError:
        raise DriverNotFound(driver_path)


def create_schema():
    if not _connection:
        raise DBNotConnected()

    schema = get_driver(DB.driver).create_schema(
        'users',
        Column('email', ('varchar', 255), unique=True),
        Column('password', ('varchar', 255)),
        Column('activation_code', ('char', 40), unique=True),
        Column('status', ('char', 1), default='P'),  # Pending, Blocked, Active
        Column('login_attempts', ('int',), default='0'),
        Column('last_attempt', ('int',), default='0'),
    )

    execute(schema)


def execute(sql, values=None):
    return get_driver(DB.driver).execute(_connection, sql, values)


def create(sql, values=None):
    return get_driver(DB.driver).create(_connection, sql, values)
