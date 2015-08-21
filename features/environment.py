from selenium import webdriver

def get_browser():
    # return webdriver.PhantomJS()
    return webdriver.Firefox()


def before_all(context):
    context.browser = get_browser()

def after_all(context):
    context.browser.quit()
