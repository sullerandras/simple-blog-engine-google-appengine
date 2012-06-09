Feature: edit blog entry
    In order to fix typos
    an admin
    wants to be able to edit existing blog entries

    Scenario: Edit link for a blog entry
        Given there are no blog entries in the database
        And I am signed in as admin
        And I add a new blog entry "entry1"
        When I visit the home page
        Then I should see a "Edit" link

    Scenario: Edit blog entry page
        Given there are no blog entries in the database
        And I am signed in as admin
        And I add a new blog entry "entry1"
        And I visit the home page
        When I click on the "Edit" link
        Then I should see the "Edit blog entry" page
        And I should see an input for "title"
        And I should see an input for "text"
        And I should see a "Save" button

    Scenario: Edit a blog entry's title
        Given there are no blog entries in the database
        And I am signed in as admin
        And I add a new blog entry "entry1"
        And I visit the home page
        When I click on the "Edit" link
        And I fill out the "title" field with "new title"
        And I click on the "Save" button
        Then I should see the home page
        And I should see the blog entry with "title": "new title"
        And I should see the blog entry with "text": "entry1"

    Scenario: Edit a blog entry's text
        Given there are no blog entries in the database
        And I am signed in as admin
        And I add a new blog entry "entry1"
        And I visit the home page
        When I click on the "Edit" link
        And I fill out the "text" field with "new text"
        And I click on the "Save" button
        Then I should see the home page
        And I should see the blog entry with "title": "entry1"
        And I should see the blog entry with "text": "new text"

