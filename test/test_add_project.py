# -*- coding: utf-8 -*-
import string
import random
from model.project import MantisProject


def random_project_name(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "
    return prefix + "".join([random.choice(symbols) for i in range(maxlen)])


def test_add_project_using_soap(app, admin):
    project = MantisProject(name=random_project_name("Project ", 10))
    old_projects = app.soap.get_project_list()
    app.manage_page.add_new_project(project.name)
    new_projects = app.soap.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=MantisProject.id_or_max) == sorted(new_projects, key=MantisProject.id_or_max)