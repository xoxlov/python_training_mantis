# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pages.ManagePage import ManagePage
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.session import SessionHelper
from fixture.mail import MailHelper
from fixture.soap import SoapHelper


class Application:
    def __init__(self, browser, config):
        self.config = config
        if browser == "firefox":
            caps = DesiredCapabilities.FIREFOX
            caps['marionette'] = False
            self.wd = webdriver.Firefox(capabilities=caps)
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.james = JamesHelper(self)
        self.manage_page = ManagePage(self)
        self.base_url = config["web"]["baseUrl"]
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()
