Feature: guest visits home page
    As a guest
    I want to visit the home page
    So I can read blog entries

    Scenario: visit home page with no blog entries
        Given there are no blog entries in the database
        When I visit the home page
        Then I should see the message "No entries yet, please check back later!"

    Scenario: visit home page with two blog entries
        Given there are no blog entries in the database
        And I am signed in as admin
        And I add a new blog entry "entry1"
        And I add a new blog entry "entry2"
        When I visit the home page
        Then I should see these two blog entries in "entry2", "entry1" order
