# -*- coding: utf-8 -*-
from lettuce import step, world, before, after
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

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
    world.browser.get("http://localhost:8080%s" % page)

# =========================================================

@step(u'Given there are no blog entries in the database')
def given_there_are_no_blog_entries_in_the_database(step):
    pass

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


@step(u'Given I am signed in as admin')
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
