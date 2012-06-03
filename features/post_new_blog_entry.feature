Feature: post new blog entry

    Scenario: post new blog entry
        Given there are no blog entries in the database
        And I am signed in as admin
        And I am on the "New blog entry" page
        When I fill out the details with random data
        And I click on the "Post" button
        Then I should see the home page
        And I should see the new blog entry with the entered random data
        And I should see that the blog entry created today

    Scenario: post new blog entry with long text
        Given there are no blog entries in the database
        And I am signed in as admin
        And I am on the "New blog entry" page
        When I fill out the details with long random data
        And I click on the "Post" button
        Then I should see the home page
        And I should see the new blog entry with the entered random data
        And I should see that the blog entry created today
