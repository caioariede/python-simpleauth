# coding: utf-8
from re import findall
from lettuce import step, world

from simpleauth.shortcuts import (signup,
                                  activate,
                                  mail_dummy_box)


@step(u'Given I register myself with "([^"]*)" and "([^"]*)"')
def given_i_register_myself_with_email_and_password(step, email, password):
    world.user = signup(email, password)


@step(u'Then I need to receive "([^"]*)" e-mail containing "([^"]*)"')
def then_i_need_to_receive_num_e_mail_containing_message(step, num_emails, message):
    mail_box = mail_dummy_box()

    assert int(num_emails) == len(mail_box), 'Got %d' % len(mail_box)

    content = mail_box[0].as_string()

    world.activation_code = findall(message + ' (\S+)', content)[0]

    assert message in content, 'Got %s' % content


@step(u'the user status is "([^"]*)"')
def the_user_status_is(step, status):
    user_status = world.user.get_status_display()

    assert user_status == status, 'Got %s' % user_status


@step(u'I activate user with the received activation code')
def activate_user_with_received_activation_code(step):
    world.user = activate(world.user.pk, world.activation_code)
