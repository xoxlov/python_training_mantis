# -*- coding: utf-8 -*-


def test_login(app):
    # login is being made automatically in fixture
    assert app.session.is_logged_in_as("administrator")
    app.session.logout()
