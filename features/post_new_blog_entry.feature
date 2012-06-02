Feature: post new blog entry

    Scenario: post new blog entry
        Given I am signed in as admin
        And I am on the "New blog entry" page
        When I fill out the details with random data
        And I click on the "Post" button
        Then I should see the home page
        And I should see the new blog entry with the entered random data
