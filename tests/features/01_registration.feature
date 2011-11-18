Feature: Registration
    Scenario: Setting New User
        Given I register myself with "test@example.com" and "mypassword"
        Then I need to receive "1" e-mail containing "Your activation code is"
        And the user status is "pending"

    Scenario: New User Activation
        Given I activate user with the received activation code
        Then the user status is "active"
