# -*- coding: utf-8 -*-
import random
import string
from model.project import MantisProject


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(2, maxlen))])


def test_delete_project(app):
    old_projects = app.manage_page.get_projects_list()
    if not old_projects:
        app.manage_page.add_new_project(MantisProject(name=random_string("Project ", 11)))
    project_to_delete = random.choice(old_projects)
    app.manage_page.delete_project(project_to_delete)
    old_projects.remove(project_to_delete)
    new_projects = app.manage_page.get_projects_list()
    assert sorted(old_projects, key=MantisProject.id_or_max) == sorted(new_projects, key=MantisProject.id_or_max)
