# -*- coding: utf-8 -*-
from lettuce import step, world, before, after
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time, datetime

# ======================== HOOKS ==========================

@before.each_feature
def before_each_feature(feature):
    world.browser = webdriver.Firefox() # Get local session of firefox

@after.each_feature
def after_each_feature(feature):
    world.browser.close()

# =========================================================

@step(u'Given there are no blog entries in the database')
def given_there_are_no_blog_entries_in_the_database(step):
    pass

@step(u'When I visit the home page')
def when_i_visit_the_home_page(step):
    world.browser.get("http://localhost:8080") # Load page

@step(u'Then I should see the message "([^"]*)"')
def then_i_should_see_the_message(step, msg):
    body = world.browser.find_element_by_xpath("//body")
    assert msg in body.text, "I should see '%s', but I see '%s'" % (msg, body.text)


@step(u'Given I am a guest user')
def given_i_am_a_guest_user(step):
    pass

@step(u'Then I should see a "([^"]*)" link')
def then_i_should_see_a_link(step, name):
    world.browser.find_element_by_xpath("//a[contains(text(), '%s')]" % name)

