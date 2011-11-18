from hashlib import sha1
from uuid import uuid1

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .utils import current_timestamp


class DB(object):
    """
    Store database information and credentials.

    """
    driver = ''
    name = ''
    user = ''
    password = ''
    host = ''
    port = ''

    _connection = None


class Column(object):
    """
    Database column.

    """
    def __init__(self, name, type, null=False, unique=False, default=None):
        self.name = name
        self.type = type
        self.null = null
        self.unique = unique
        self.default = default


class User(object):
    """
    User object.

    """
    def __init__(self, pk, email, password, activation_code, status, login_attempts=0, last_attempt=0):
        self.pk = pk
        self.email = email
        self.password = password
        self.activation_code = activation_code
        self.status = status
        self.login_attempts = login_attempts
        self.last_attempt = last_attempt

    def get_status_display(self):
        return {'P': 'pending',
                'B': 'blocked',
                'A': 'active'}[self.status]

    def seconds_from_last_attempt(self):
        return current_timestamp() - self.last_attempt

    def increase_attempt(self):
        self.login_attempts += 1
        self.last_attempt = current_timestamp()

        if self.login_attempts >= 3:
            self.status = 'B'

    def is_active(self):
        return self.status == 'A'

    @classmethod
    def generate_activation_code(cls):
        return sha1(str(uuid1())).hexdigest()

    @classmethod
    def hash_password(cls, password):
        # TODO: Use salt before password
        return sha1(password).hexdigest()


class Mail(object):
    """
    Store mail credentials and send_mail method.

    When is_dummy is set the emails are appended
    to dummy_box instead of being sent.

    """
    is_dummy = False

    host = ''
    host_user = ''
    host_password = ''

    use_tls = ''
    port = ''

    dummy_box = []

    @classmethod
    def send_mail(cls, subject, content, to):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = cls.host_user
        msg['To'] = to

        part2 = MIMEText(content, 'html')

        msg.attach(part2)

        if not cls.is_dummy:
            s = smtplib.SMTP(cls.host, cls.port)
            s.ehlo()

            if cls.use_tls:
                s.starttls()

            s.login(cls.host_user, cls.host_password)
            s.sendmail(cls.host_user, to, msg.as_string())
            s.quit()

        else:
            cls.dummy_box.append(msg)
