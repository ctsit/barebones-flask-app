from nose.tools import assert_equals
import time

@when('we visit index')
def step(context):
    context.browser.get('https://127.0.0.1:5000/')
    time.sleep(1)

@then('it should have a title "Barebones Web Application"')
def step(context):
    assert_equals(context.browser.title, "Barebones Web Application")
