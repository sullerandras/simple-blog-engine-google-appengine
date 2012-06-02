Feature: new blog entry link

    Scenario: admin user see the new blog entry link
        Given I am signed in as admin
        When I visit the home page
        Then I should see a "New blog entry" link

    Scenario: non admin users should not see the new blog entry link
        Given I am a signed in user
        When I visit the home page
        Then I should not see the "New blog entry" link

    Scenario: guest should not see the new blog entry link
        Given I am a guest user
        When I visit the home page
        Then I should not see the "New blog entry" link
