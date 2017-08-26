# -*- coding: utf-8 -*-
import string
import random
from model.project import MantisProject


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(2, maxlen))])


def test_add_project(app):
    old_projects = app.manage_page.get_projects_list()
    project = MantisProject(name=random_string("Project ", 11))
    app.manage_page.add_new_project(project.name)
    old_projects.append(project)
    new_projects = app.manage_page.get_projects_list()
    assert sorted(old_projects, key=MantisProject.id_or_max) == sorted(new_projects, key=MantisProject.id_or_max)
