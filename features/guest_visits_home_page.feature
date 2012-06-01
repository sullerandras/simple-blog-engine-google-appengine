Feature: guest visits home page
    As a guest
    I want to visit the home page
    So I can read blog entries

    Scenario: visit home page with no blog entries
        Given there are no blog entries in the database
        When I visit the home page
        Then I should see the message "No entries yet, please check back later!"

    Scenario: visit home page with blog entries
        Given there are several blog entries in the database:
            | title  | text             | date       |
            | first  | first blog entry | 2012-05-21 |
            | second | second entry     | 2012-06-01 |
        When I visit the home page
        Then I should see the following blog entries:
            | title  | text             | date       |
            | first  | first blog entry | 2012-05-21 |
            | second | second entry     | 2012-06-01 |
