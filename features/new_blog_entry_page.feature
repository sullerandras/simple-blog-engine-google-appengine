Feature: new blog entry page

    Scenario: new blog entry page
        Given I am signed in as admin
        When I visit the home page
        And I click on the "New blog entry" link
        Then I should see the "New blog entry" page
        And I should see an input for "title"
        And I should see an input for "text"
        And I should see a "Post" button
