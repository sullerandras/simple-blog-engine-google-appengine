Feature: markdown syntax
    As an admin
    I want to type the blog entry text in Markdown format
    So I can easily display HTML content without writing any HTML code

    Scenario: write blog entry text in Markdown
        Given there are no blog entries in the database
        And I am signed in as admin
        And I am on the "New blog entry" page
        When I fill out the "title" field with "markdown test"
        And I fill out the "text" field with:
            """
            Hello Markdown
            ==

            This is an example post using [Markdown](http://daringfireball.net/projects/markdown/).
            """
        And I click on the "Post" button
        Then I should see the home page
        And I should see the blog entry with "title": "markdown test"
        And I should see the text in HTML:
            """
            <h1>Hello Markdown</h1>

            <p>This is an example post using <a href="http://daringfireball.net/projects/markdown/">Markdown</a>.</p>
            """
