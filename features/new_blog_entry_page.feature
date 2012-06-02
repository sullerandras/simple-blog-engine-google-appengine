Feature: new blog entry page

    Scenario: new blog entry page
        Given I am signed in as admin
        When I visit the the new blog entry page
        Then I should see an input for "title"
        And I should see an input for "text"
        And I should see a "Post" button
