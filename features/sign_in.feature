Feature: sign in

    Scenario: guests should see a sign in link
        Given I am a guest user
        When I visit the home page
        Then I should see a "Sign in" link

    Scenario: signed in users should not see a sign in link
        Given I am a signed in user
        When I visit the home page
        Then I should not see the "Sign in" link
