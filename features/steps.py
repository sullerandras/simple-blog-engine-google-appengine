# -*- coding: utf-8 -*-
from lettuce import step, world, before, after
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import random

BASE_URL = 'http://localhost:8080'

# ======================== HOOKS ==========================

@before.all
def before_all():
    world.browser = webdriver.Firefox() # Get local session of firefox

@after.all
def after_all(total):
    world.browser.close()

@before.each_scenario
def before_each_scenario(scenario):
    world.browser.delete_all_cookies()

# =========================================================

def load_page(page):
    world.browser.get("%s%s" % (BASE_URL, page))

def get_random_text(length, multiline):
    s = ''
    for i in xrange(length):
        if random.random() < 0.2 and s and s == s.strip():
            s += ' '
        elif multiline and random.random() < 0.05 and s and s == s.strip():
            s += '\n'
        else:
            s += chr(random.randrange(ord('a'), ord('z')))
    return s.strip()

# =========================================================

@step(u'Given there are no blog entries in the database')
def given_there_are_no_blog_entries_in_the_database(step):
    # hackish. we need to get the xsrf_token from a custom url
    load_page('/xsrf_token')
    body = world.browser.find_element_by_tag_name('body')

    import urllib
    import urllib2
    urllib2.urlopen('http://localhost:8080/_ah/admin/interactive/execute',
        data = urllib.urlencode({'code' : 'from google.appengine.ext import db\n' +
                                      'db.delete(db.Query())',
                                 'xsrf_token': body.text}))

@step(u'When I visit the home page')
def when_i_visit_the_home_page(step):
    load_page('/')

@step(u'Then I should see the message "([^"]*)"')
def then_i_should_see_the_message(step, msg):
    body = world.browser.find_element_by_tag_name('body')
    assert msg in body.text, "I should see '%s', but I see '%s'" % (msg, body.text)


@step(u'Given I am a guest user')
def given_i_am_a_guest_user(step):
    pass

@step(u'Then I should see a "([^"]*)" link')
def then_i_should_see_a_link(step, name):
    world.browser.find_element_by_link_text(name)


@step(u'Given I am a signed in user')
def given_i_am_a_signed_in_user(step):
    load_page('/')
    world.browser.find_element_by_link_text('Sign in').click()
    world.browser.find_element_by_id('submit-login').click()

@step(u'Then I should not see the "([^"]*)" link')
def then_i_should_not_see_the_link(step, name):
    try:
        world.browser.find_element_by_link_text(name)
        assert 0, "I should not see the link: %s" % name
    except NoSuchElementException:
        pass


@step(u'I am signed in as admin')
def given_i_am_signed_in_as_admin(step):
    load_page('/')
    world.browser.find_element_by_link_text('Sign in').click()
    world.browser.find_element_by_id('admin').click()
    world.browser.find_element_by_id('submit-login').click()


@step(u'And I click on the "([^"]*)" link')
def and_i_click_on_the_link(step, link):
    world.browser.find_element_by_link_text(link).click()

@step(u'Then I should see the "New blog entry" page')
def then_i_should_see_the_page(step):
    assert world.browser.current_url.endswith('/new'),\
        'The url should ends with "/new", but it is %s' % world.browser.current_url
    world.browser.find_element_by_xpath("//*[text() = 'New blog entry']")

@step(u'I should see an input for "([^"]*)"')
def i_should_see_an_input_for(step, name):
    world.browser.find_element_by_name(name)

@step(u'And I should see a "([^"]*)" button')
def and_i_should_see_a_button(step, name):
    world.browser.find_element_by_xpath("//button[contains(text(), '%s')]" % name)


@step(u'And I am on the "New blog entry" page')
def and_i_am_on_the_page(step):
    load_page('/new')

@step(u'When I fill out the details with random data')
def when_i_fill_out_the_details_with_random_data(step):
    title = world.browser.find_element_by_name('title')
    world.title = get_random_text(20, False)
    title.send_keys(world.title)
    text = world.browser.find_element_by_name('text')
    world.text = get_random_text(200, True)
    text.send_keys(world.text)

@step(u'And I click on the "([^"]*)" button')
def and_i_click_on_the_button(step, name):
    world.browser.find_element_by_xpath("//button[contains(text(), '%s')]" % name).click()

@step(u'Then I should see the home page')
def then_i_should_see_the_home_page(step):
    url = '%s/' % BASE_URL
    assert world.browser.current_url == url,\
        'The url should be %s, but it is %s' % (url, world.browser.current_url)

@step(u'And I should see the new blog entry with the entered random data')
def and_i_should_see_the_new_blog_entry_with_the_entered_random_data(step):
    body = world.browser.find_element_by_tag_name('body')
    assert world.title in body.text, 'I should see "%s" but only see "%s"' % (world.title, body.text)
    assert world.text in world.browser.page_source,\
        'I should see "%s" but only see "%s"' % (world.text, world.browser.page_source)
