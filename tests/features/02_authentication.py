# coding: utf-8
from time import sleep

from lettuce import step, world

from simpleauth.shortcuts import login
from simpleauth.exceptions import (UserIncorrectPassword,
                                   UserBlocked)


@step(u'user log in with "([^"]*)" and "([^"]*)"')
def given_an_user_log_in_with_email_and_password(step, email, password):
    try:
        world.user = login(email, password)
    except UserIncorrectPassword:
        world.message = 'Incorrect password'
    except UserBlocked:
        world.message = 'You are blocked'
    else:
        world.message = 'Welcome %s' % email


@step(u'Then the message "([^"]*)" is displayed')
def then_the_message_is_displayed(step, message):
    assert world.message == message, "Got %s" % world.message


@step(u'after "([^"]+)" seconds')
def and_after_seconds(step, seconds):
    seconds = int(seconds)
    sleep(seconds)
