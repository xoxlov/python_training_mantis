# -*- coding: utf-8 -*-
import pytest
import json
import os.path
import ftputil
from fixture.application import Application


fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_name) as config_file:
            target = json.load(config_file)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture()
def app(request, config):
    global fixture
    global target
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    return fixture


@pytest.fixture()
def admin(request, app):
    web_admin = app.config["webadmin"]
    fixture.session.ensure_login(username=web_admin["username"], password=web_admin["password"])


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    config_ftp = config["ftp"]
    install_server_configuration(config_ftp["host"], config_ftp["username"], config_ftp["password"])
    def fin():
        restore_server_configuration(config_ftp["host"], config_ftp["username"], config_ftp["password"])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config/config_inc.php.bak"):
            remote.remove("config/config_inc.php.bak")
        if remote.path.isfile("config/config_inc.php"):
            remote.rename("config/config_inc.php", "config/config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config/config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config/config_inc.php.bak"):
            if remote.path.isfile("config/config_inc.php"):
                remote.remove("config/config_inc.php")
            remote.rename("config/config_inc.php.bak", "config/config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
