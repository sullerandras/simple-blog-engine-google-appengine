import unittest, datetime
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.ext import admin

from models import BlogEntry
from main import IndexHandler, NewBlogEntryHandler, XsrfTokenHandler

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

class GuestVisitHomePageTestCase(BaseTestCase):
    def testWithNoBlogEntries(self):
        self.assertEqual(0, BlogEntry.all().count())
        handler = IndexHandler()
        s = handler.render()
        self.assertRegexpMatches(s, "No entries yet, please check back later!")

class SignInTestCase(BaseTestCase):
    def testGuest(self):
        handler = IndexHandler()
        s = handler.render()
        self.assertRegexpMatches(s, r"<a href=[^>]+>Sign in</a>")

    def testSignedIn(self):
        self.testbed.setup_env(
            USER_EMAIL = 'user@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '0',
            overwrite = True)
        handler = IndexHandler()
        s = handler.render()
        self.assertNotRegexpMatches(s, r"<a href=[^>]+>Sign in</a>")

class SignOutTestCase(BaseTestCase):
    def testGuest(self):
        handler = IndexHandler()
        s = handler.render()
        self.assertNotRegexpMatches(s, r"<a href=[^>]+>Sign out</a>")

    def testSignedIn(self):
        self.testbed.setup_env(
            USER_EMAIL = 'user@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '0',
            overwrite = True)
        handler = IndexHandler()
        s = handler.render()
        self.assertRegexpMatches(s, r"<a href=[^>]+>Sign out</a>")

class NewBlogEntryLinkTestCase(BaseTestCase):
    def testAdmin(self):
        self.testbed.setup_env(
            USER_EMAIL = 'admin@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '1',
            overwrite = True)
        handler = IndexHandler()
        s = handler.render()
        self.assertRegexpMatches(s, r"<a href=[^>]+>New blog entry</a>")

    def testSignedIn(self):
        self.testbed.setup_env(
            USER_EMAIL = 'user@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '0',
            overwrite = True)
        handler = IndexHandler()
        s = handler.render()
        self.assertNotRegexpMatches(s, r"<a href=[^>]+>New blog entry</a>")

    def testGuest(self):
        handler = IndexHandler()
        s = handler.render()
        self.assertNotRegexpMatches(s, r"<a href=[^>]+>New blog entry</a>")

class NewBlogEntryPageTestCase(BaseTestCase):
    def testAdmin(self):
        self.testbed.setup_env(
            USER_EMAIL = 'admin@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '1',
            overwrite = True)
        handler = NewBlogEntryHandler()
        s = handler.render()
        self.assertRegexpMatches(s, r'<[^>]+>New blog entry</[^>]+>')
        self.assertRegexpMatches(s, r'<[^>]+ name="title"[^>]*>')
        self.assertRegexpMatches(s, r'<[^>]+ name="text"[^>]*>')
        self.assertRegexpMatches(s, r'<button type="submit"[^>]*>Post</button>')

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
        self.testbed.setup_env(
            USER_EMAIL = 'admin@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '1',
            overwrite = True)

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
        handler = IndexHandler()
        s = handler.render()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.assertRegexpMatches(s, r'<[^>]+ class="title"[^>]*>asdsad</')
        self.assertRegexpMatches(s, r'<[^>]+ class="text"[^>]*>my text</')
        self.assertRegexpMatches(s, r'<[^>]+ class="date"[^>]*>%s</' % today)

class XsrfTokenTestCase(BaseTestCase):
    def testXsrfToken(self):
        class MockRequest(object):
            def __init__(self):
                self.host = 'localhost:8080'

        handler = XsrfTokenHandler()
        handler.request = MockRequest()
        s = handler.render()
        self.assertEqual(s, admin.get_xsrf_token())

if __name__ == '__main__':
    unittest.main()
