# -*- coding: utf-8 -*-


class SessionHelper():
    def __init__(self, app):
        self.app = app

    @property
    def logged_user_name(self):
        return self.app.wd.find_element_by_css_selector(".user-info")

    def open_homepage(self):
        wd = self.app.wd
        if wd.current_url.endswith("/mantisbt/my_view_page.php"):
            return
        wd.get(self.app.base_url)

    def login(self, username, password):
        self.open_homepage()
        self._type_and_submit_input("username", username)
        self._type_and_submit_input("password", password)

    def _type_and_submit_input(self, location, value):
        wd = self.app.wd
        wd.find_element_by_name(location).click()
        wd.find_element_by_name(location).clear()
        wd.find_element_by_name(location).send_keys(value)
        wd.find_element_by_css_selector("input[type='submit']").click()

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            self.logout()
        self.login(username, password)

    def logout(self):
        wd = self.app.wd
        logout_button = wd.find_element_by_css_selector("a[href*='logout_page.php']")
        if not logout_button.is_displayed():
            self.logged_user_name.click()
        logout_button.click()

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_css_selector("span.user-info")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return self.logged_user_name.text
