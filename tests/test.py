import unittest, datetime
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.ext import admin

from models import BlogEntry
from main import IndexHandler, NewBlogEntryHandler, XsrfTokenHandler, EditBlogEntryHandler

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def signInAsUser(self):
        self.testbed.setup_env(
            USER_EMAIL = 'user@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '0',
            overwrite = True)

    def signInAsAdmin(self):
        self.testbed.setup_env(
            USER_EMAIL = 'admin@example.com',
            USER_ID = '1',
            USER_IS_ADMIN = '1',
            overwrite = True)

class GuestVisitHomePageTestCase(BaseTestCase):
    def testWithNoBlogEntries(self):
        self.assertEqual(0, BlogEntry.all().count())
        result = IndexHandler().render()
        self.assertRegexpMatches(result, "No entries yet, please check back later!")

    def testWithTwoBlogEntries(self):
        BlogEntry(title = 'entry1', text = 'entry1').save()
        BlogEntry(title = 'entry2', text = 'entry2').save()
        result = IndexHandler().render()
        self.assertIn('entry2', result)
        self.assertIn('entry1', result)
        self.assertLess(result.index('entry2'), result.index('entry1'))


class SignInTestCase(BaseTestCase):
    def testGuest(self):
        result = IndexHandler().render()
        self.assertRegexpMatches(result, r"<a href=[^>]+>Sign in</a>")

    def testSignedIn(self):
        self.signInAsUser()
        result = IndexHandler().render()
        self.assertNotRegexpMatches(result, r"<a href=[^>]+>Sign in</a>")

class SignOutTestCase(BaseTestCase):
    def testGuest(self):
        result = IndexHandler().render()
        self.assertNotRegexpMatches(result, r"<a href=[^>]+>Sign out</a>")

    def testSignedIn(self):
        self.signInAsUser()
        result = IndexHandler().render()
        self.assertRegexpMatches(result, r"<a href=[^>]+>Sign out</a>")

class NewBlogEntryLinkTestCase(BaseTestCase):
    def testAdmin(self):
        self.signInAsAdmin()
        result = IndexHandler().render()
        self.assertRegexpMatches(result, r"<a href=[^>]+>New blog entry</a>")

    def testSignedIn(self):
        self.signInAsUser()
        result = IndexHandler().render()
        self.assertNotRegexpMatches(result, r"<a href=[^>]+>New blog entry</a>")

    def testGuest(self):
        result = IndexHandler().render()
        self.assertNotRegexpMatches(result, r"<a href=[^>]+>New blog entry</a>")

class NewBlogEntryPageTestCase(BaseTestCase):
    def testAdmin(self):
        self.signInAsAdmin()
        result = NewBlogEntryHandler().render()
        self.assertRegexpMatches(result, r'<[^>]+>New blog entry</[^>]+>')
        self.assertRegexpMatches(result, r'<[^>]+ name="title"[^>]*>')
        self.assertRegexpMatches(result, r'<[^>]+ name="text"[^>]*>')
        self.assertRegexpMatches(result, r'<button type="submit"[^>]*>Post</button>')

class PostNewBlogEntryTestCase(BaseTestCase):
    def createNewBlogEntryHandler(self, textLength = 200):
        class MockRequest(object):
            def __init__(self, textLength):
                self.uri = 'http://mockhost'
                # multiply a 10 character string to reach the expected length
                self.text = 'short\ntext' * (textLength / 10)
                self.POST = {'title': 'asdsad', 'text': self.text}

        class MockResponse(object):
            def __init__(self):
                self.status = 0
                self.headers = {}
            def set_status(self, status):
                self.status = status
            def clear(self):
                pass

        handler = NewBlogEntryHandler()
        handler.request = MockRequest(textLength)
        handler.response = MockResponse()
        return handler

    def testPostNewBlogEntry(self, textLength = 200):
        self.signInAsAdmin()

        self.assertEqual(0, BlogEntry.all().count())
        handler = self.createNewBlogEntryHandler(textLength = textLength)
        handler.post()
        self.assertEqual(1, BlogEntry.all().count())
        e = BlogEntry.all().get()
        self.assertEqual('asdsad', e.title)
        self.assertEqual(handler.request.text, e.text)

    def testPostNewBlogEntryWithLongText(self):
        self.testPostNewBlogEntry(textLength = 2000)

    def testRenderingBlogEntries(self):
        self.assertEqual(0, BlogEntry.all().count())
        BlogEntry(title = 'asdsad', text = 'my text').save()
        self.assertEqual(1, BlogEntry.all().count())
        result = IndexHandler().render()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertRegexpMatches(result, r'<[^>]+ class="title"[^>]*>asdsad</')
        self.assertRegexpMatches(result, r'<[^>]+ class="text"[^>]*><p>my text</p></')
        self.assertRegexpMatches(result, r'<[^>]+ class="date"[^>]*>%s</' % today)

class MarkdownBlogEntryTestCase(BaseTestCase):
    def testRenderingBlogEntriesWithMarkdown(self):
        self.assertEqual(0, BlogEntry.all().count())
        BlogEntry(title = 'asdsad', text = 'Hello Markdown\n'+
            '==\n'+
            '\n'+
            'This is an example post using [Markdown](http://a.b).').save()
        self.assertEqual(1, BlogEntry.all().count())
        result = IndexHandler().render()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertRegexpMatches(result, r'<[^>]+ class="title"[^>]*>asdsad</')
        self.assertRegexpMatches(result, r'<[^>]+ class="text"[^>]*><h1>Hello Markdown</h1>'+
            '[^<]*'+
            '<p>This is an example post using <a href="http://a.b">Markdown</a>.</p></')
        self.assertRegexpMatches(result, r'<[^>]+ class="date"[^>]*>%s</' % today)

class EditBlogEntryTestCase(BaseTestCase):
    def testEditLinkForAdmin(self):
        # Given there are no blog entries in the database
        self.assertEqual(0, BlogEntry.all().count())
        # And I am signed in as admin
        self.signInAsAdmin()
        # And I add a new blog entry "entry1"
        BlogEntry(title = 'entry1', text = 'entry1').save()
        self.assertEqual(1, BlogEntry.all().count())
        # When I visit the home page
        result = IndexHandler().render()
        # Then I should see a "Edit" link
        self.assertRegexpMatches(result, r"<a href=[^>]+>Edit</a>")

    def testNoEditLinkForGuest(self):
        # Given there is a blog entry in the database
        BlogEntry(title = 'entry1', text = 'entry1').save()
        self.assertEqual(1, BlogEntry.all().count())
        # When I visit the home page
        result = IndexHandler().render()
        # Then I should not see the "Edit" link
        self.assertNotRegexpMatches(result, r"<a href=[^>]+>Edit</a>")

    def testNoEditLinkForUser(self):
        # Given there is a blog entry in the database
        BlogEntry(title = 'entry1', text = 'entry1').save()
        self.assertEqual(1, BlogEntry.all().count())
        # And I am a signed in user
        self.signInAsUser()
        # When I visit the home page
        result = IndexHandler().render()
        # Then I should not see the "Edit" link
        self.assertNotRegexpMatches(result, r"<a href=[^>]+>Edit</a>")

    def createEditBlogEntryHandler(self):
        class MockRequest(object):
            def __init__(self):
                self.uri = 'http://mockhost'
                self.host = 'mockhost'
                self.GET = {}
                self.POST = {'title': 'entry1', 'text': 'entry1'}

        class MockOut(object):
            def __init__(self):
                self.buffer = ''
            def write(self, data):
                self.buffer += str(data)
            def __str__(self):
                return self.buffer

        class MockResponse(object):
            def __init__(self):
                self.status = 0
                self.headers = {}
                self.out = MockOut()
            def set_status(self, status):
                self.status = status
            def clear(self):
                pass

        handler = EditBlogEntryHandler()
        handler.request = MockRequest()
        handler.response = MockResponse()
        return handler

    def testEditBlogEntry(self):
        # Given there is a blog entry in the database
        entry = BlogEntry(title = 'entry1', text = 'entry1')
        entry.save()
        self.assertEqual(1, BlogEntry.all().count())
        # And I am signed in as admin
        self.signInAsAdmin()
        # When I edit the blog entry
        handler = self.createEditBlogEntryHandler()
        handler.request.GET['id'] = entry.key().id()
        handler.get()
        result = str(handler.response.out)
        # And I should see an input for "title"
        self.assertRegexpMatches(result, r'<[^>]+ name="title"[^>]*>')
        self.assertRegexpMatches(result, r'<[^>]+ value="entry1"[^>]*>')
        # And I should see an input for "text"
        self.assertRegexpMatches(result, r'<[^>]+ name="text"[^>]*>')
        self.assertRegexpMatches(result, r'<textarea[^>]*>entry1<')
        # And I should see a "Save" button
        self.assertRegexpMatches(result, r'<button[^>]*>Save</')

        # And I fill out the "title" field with "new title"
        handler = self.createEditBlogEntryHandler()
        handler.request.POST['id'] = entry.key().id()
        handler.request.POST['title'] = 'new title'
        # And I fill out the "text" field with "new text"
        handler.request.POST['text'] = 'new text'
        # And I click on the "Save" button
        handler.post()
        # And I should see the blog entry with "title": "new title"
        self.assertEqual(1, BlogEntry.all().count())
        entry = BlogEntry.all().get()
        self.assertEqual('new title', entry.title)
        # And I should see the blog entry with "text": "new text"
        self.assertEqual('new text', entry.text)

class XsrfTokenTestCase(BaseTestCase):
    def testXsrfToken(self):
        class MockRequest(object):
            def __init__(self):
                self.host = 'localhost:8080'

        handler = XsrfTokenHandler()
        handler.request = MockRequest()
        result = handler.render()
        self.assertEqual(result, admin.get_xsrf_token())

if __name__ == '__main__':
    unittest.main()
