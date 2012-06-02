import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from models import BlogEntry
from main import IndexHandler, NewBlogEntryHandler

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
    def testPostNewBlogEntry(self):
        class MockRequest(object):
            def __init__(self):
                self.uri = 'http://mockhost'
                self.POST = {'title': 'asdsad', 'text': 'my text'}

        class MockResponse(object):
            def __init__(self):
                self.status = 0
                self.headers = {}
            def set_status(self, status):
                self.status = status
            def clear(self):
                pass

        self.testbed.setup_env(
            USER_EMAIL = 'admin@example.com',
            USER_ID = '123',
            USER_IS_ADMIN = '1',
            overwrite = True)

        self.assertEqual(0, BlogEntry.all().count())
        handler = NewBlogEntryHandler()
        handler.request = MockRequest()
        handler.response = MockResponse()
        handler.post()
        self.assertEqual(1, BlogEntry.all().count())
        e = BlogEntry.all().get()
        self.assertEqual('asdsad', e.title)
        self.assertEqual('my text', e.text)

    def testRenderingBlogEntries(self):
        self.assertEqual(0, BlogEntry.all().count())
        BlogEntry(title = 'asdsad', text = 'my text').save()
        self.assertEqual(1, BlogEntry.all().count())
        handler = IndexHandler()
        s = handler.render()
        self.assertRegexpMatches(s, r'<[^>]+ class="title"[^>]*>asdsad</')
        self.assertRegexpMatches(s, r'<[^>]+ class="text"[^>]*>my text</')

if __name__ == '__main__':
    unittest.main()
