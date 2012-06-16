# -*- coding: utf-8 -*-
from lettuce import step, world, before, after
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import random, datetime

BASE_URL = 'http://localhost:8080/blog'

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

def assert_i_am_on_page(page):
    """ Asserts that the url is BASE_URLpage (excluding get parameters and hash). """
    assert page == '' or page[0] == '/', 'page should starts with "/"'
    url = world.browser.current_url
    expected = '%s%s' % (BASE_URL, page)
    assert url.startswith(expected), \
        'I should be on page %s, but the url is %s' % (page, url)
    assert len(url) == len(expected) or url[len(expected)] in ['?', '#'], \
        'I should be on page %s, but the url is %s' % (page, url)

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

@step(u'I visit the home page')
def i_visit_the_home_page(step):
    load_page('/')

@step(u'Then I should see the message "([^"]*)"')
def then_i_should_see_the_message(step, msg):
    body = world.browser.find_element_by_tag_name('body')
    assert msg in body.text, "I should see '%s', but I see '%s'" % (msg, body.text)

@step(u'And I add a new blog entry "([^"]*)"')
def and_i_add_a_new_blog_entry(step, title):
    step.behave_as("""
        Given I am on the "New blog entry" page
        And I fill out the details with "{title}"
        And I click on the "Post" button
    """.format(title = title))

@step(u'Then I should see these two blog entries in "([^"]*)", "([^"]*)" order')
def then_i_should_see_these_two_blog_entries_in_order(step, first, second):
    body = world.browser.find_element_by_tag_name('body')
    assert first in body.text, "I should see '%s', but I see '%s'" % (first, body.text)
    assert second in body.text, "I should see '%s', but I see '%s'" % (second, body.text)
    assert body.text.index(first) < body.text.index(second),\
        "'%s' should occur before '%s', but the result string is '%s'" % (first, second, body.text)


@step(u'Given I am a guest user')
def given_i_am_a_guest_user(step):
    pass

@step(u'Then I should see a "([^"]*)" link')
def then_i_should_see_a_link(step, name):
    world.browser.find_element_by_link_text(name)


@step(u'I am a signed in user')
def i_am_a_signed_in_user(step):
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


@step(u'I click on the "([^"]*)" link')
def i_click_on_the_link(step, link):
    world.browser.find_element_by_link_text(link).click()

@step(u'Then I should see the "New blog entry" page')
def then_i_should_see_the_page(step):
    assert_i_am_on_page('/new')
    world.browser.find_element_by_xpath("//*[text() = 'New blog entry']")

@step(u'I should see an input for "([^"]*)"')
def i_should_see_an_input_for(step, name):
    world.browser.find_element_by_name(name)

@step(u'I should see a "([^"]*)" button')
def i_should_see_a_button(step, name):
    world.browser.find_element_by_xpath("//button[contains(text(), '%s')]" % name)


@step(u'I am on the "New blog entry" page')
def i_am_on_the_new_blog_entry_page(step):
    load_page('/new')

@step(u'When I fill out the details with random data')
def when_i_fill_out_the_details_with_random_data(step):
    world.title = get_random_text(20, False)
    world.text = get_random_text(200, True)
    fill_out_the_details_with(step, world.title, world.text)

@step(u'And I fill out the details with "([^"]*)"')
def fill_out_the_details_with(step, title, text = None):
    world.browser.find_element_by_name('title').send_keys(title)
    world.browser.find_element_by_name('text').send_keys(text or title)

@step(u'And I click on the "([^"]*)" button')
def and_i_click_on_the_button(step, name):
    world.browser.find_element_by_xpath("//button[contains(text(), '%s')]" % name).click()

@step(u'Then I should see the home page')
def then_i_should_see_the_home_page(step):
    assert_i_am_on_page('/')

@step(u'And I should see the new blog entry with the entered random data')
def and_i_should_see_the_new_blog_entry_with_the_entered_random_data(step):
    body = world.browser.find_element_by_tag_name('body')
    assert world.title in body.text, 'I should see "%s" but only see "%s"' % (world.title, body.text)
    assert world.text in world.browser.page_source,\
        'I should see "%s" but only see "%s"' % (world.text, world.browser.page_source)

@step(u'And I should see that the blog entry created today')
def and_i_should_see_that_the_blog_entry_created_today(step):
    body = world.browser.find_element_by_tag_name('body')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    assert today in body.text, 'I should see the current date %s but only see %s' % (today, body.text)

@step(u'When I fill out the details with long random data')
def when_i_fill_out_the_details_with_long_random_data(step):
    world.title = get_random_text(20, False)
    world.text = get_random_text(600, True)
    fill_out_the_details_with(step, world.title, world.text)

@step(u'I fill out the "([^"]*)" field with "([^"]*)"')
def i_fill_out_the_field_with(step, field, text):
    elem = world.browser.find_element_by_name(field)
    elem.clear()
    elem.send_keys(text)

@step(u'And I fill out the "([^"]*)" field with:')
def and_i_fill_out_the_field_with(step, field):
    assert step.multiline
    elem = world.browser.find_element_by_name(field)
    elem.clear()
    elem.send_keys(step.multiline)

@step(u'And I should see the text in HTML')
def and_i_should_see_the_text_in_html(step):
    assert step.multiline in world.browser.page_source,\
        'I should see "%s" but only see "%s"' % (step.multiline, world.browser.page_source)


@step(u'Then I should see the "Edit blog entry" page')
def then_i_should_see_the_edit_blog_entry_page(step):
    assert_i_am_on_page('/edit')
    world.browser.find_element_by_xpath("//*[text() = 'Edit blog entry']")

@step(u'And I should see the blog entry with "([^"]*)": "([^"]*)"')
def and_i_should_see_the_blog_entry_with_field_value(step, field, value):
    assert field in ['title', 'text']
    elems = world.browser.find_elements_by_class_name(field)
    assert len(elems) == 1
    assert elems[0].text == value, \
        'The blog entry\'s %s should be %s, but it is %s' % (field, value, elems[0].text)
