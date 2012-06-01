import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

from models import BlogEntry
from main import IndexHandler

class GuestVisitHomePageTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def testWithNoBlogEntries(self):
        self.assertEqual(0, BlogEntry.all().count())
        handler = IndexHandler()
        s = handler.render()
        self.assertRegexpMatches("No entries yet, please check back later!", s)

if __name__ == '__main__':
    unittest.main()
