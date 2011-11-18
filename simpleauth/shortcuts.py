from .db import create, execute
from .classes import User, Mail
from .exceptions import UserBlocked, UserIncorrectPassword


def send_mail(subject, content, to):
    """
    Send e-mail to with HTML format.

    """
    return Mail.send_mail(subject, content, to)


def mail_dummy_box():
    """
    Return a fake mail inbox for testing purposes

    """
    return Mail.dummy_box


def signup(email, password):
    """
    User signup.

    Send e-mail with activation code to the user.

    """
    password = User.hash_password(password)
    activation_code = User.generate_activation_code()

    user = User(None, email, password, activation_code, 'P')
    user.pk = create('insert into users (email, password, activation_code, status)'
                     ' values (?, ?, ?, ?)', (user.email,
                                              user.password,
                                              user.activation_code,
                                              user.status))

    send_mail('Welcome!', 'Your activation code is %s' % activation_code, email)

    return user


def activate(user_pk, activation_code):
    """
    Activate user by a given activation code

    """
    rows = execute('select * from users where id=? and activation_code=? limit 1',
                        (user_pk, activation_code))

    for row in rows:
        user = User(*row)
        user.status = 'A'

        execute('update users set status=? where id=?', (user.status, user.pk))

        return user


def login(email, password):
    """
    Log in the user.

    The user accounts is blocked after 3 attempts and remains
    blocked for about 10 seconds.

    """
    rows = execute('select * from users where email=? and status!=? limit 1',
                        (email, 'P'))

    for row in rows:
        user = User(*row)

        if user.status == 'B':
            seconds = user.seconds_from_last_attempt()
            if seconds < 10:
                user.increase_attempt()
                raise UserBlocked

            user.status = 'A'
            user.login_attempts = 0
            user.last_attempt = 0

        if user.password == User.hash_password(password):
            user.login_attempts = 0
            user.last_attempt = 0

            execute('update users set login_attempts=?, last_attempt=? where id=?',
                        (user.login_attempts, user.last_attempt, user.pk,))

            return user

        else:
            user.increase_attempt()

            execute('update users set status=?, login_attempts=?, last_attempt=? where id=?',
                        (user.status, user.login_attempts, user.last_attempt, user.pk,))

    raise UserIncorrectPassword
