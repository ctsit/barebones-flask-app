from selenium import webdriver


def get_browser():
    # @see http://selenium-python.readthedocs.org/en/latest/api.html
    return webdriver.Firefox()
    # desired_capabilities = {'ignore-certificate-errors': True}
    # return webdriver.PhantomJS(desired_capabilities=desired_capabilities)
    # return webdriver.Chrome(desired_capabilities=desired_capabilities)


def before_all(context):
    context.browser = get_browser()
    context.browser.set_window_size(1024, 768)
    context.browser.implicitly_wait(3)


def after_all(context):
    context.browser.quit()
