Feature: sign out

    Scenario: guests should not see a sign out link
        Given I am a guest user
        When I visit the home page
        Then I should not see the "Sign out" link

    Scenario: signed in users should see a sign out link
        Given I am a signed in user
        When I visit the home page
        Then I should see a "Sign out" link
