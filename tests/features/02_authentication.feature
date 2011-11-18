Feature: Authentication
    Scenario: Log In
        Given an user log in with "test@example.com" and "mypassword"
        Then the message "Welcome test@example.com" is displayed

    Scenario: Log In with incorrect password
        Given an user log in with "test@example.com" and "incorrectpassword"
        Then the message "Incorrect password" is displayed

    Scenario: Block user after "3" attempts
        Given an user log in with "test@example.com" and "incorrectpassword1"
        Given an user log in with "test@example.com" and "incorrectpassword2"
        Given an user log in with "test@example.com" and "incorrectpassword3"
        Given an user log in with "test@example.com" and "incorrectpassword4"
        Then the message "You are blocked" is displayed
        And after "5" seconds
        An user log in with "test@example.com" and "incorrectpassword5"
        Then the message "You are blocked" is displayed
        And after "10" seconds
        An user log in with "test@example.com" and "incorrectpassword6"
        Then the message "Incorrect password" is displayed
