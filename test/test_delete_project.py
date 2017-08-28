# -*- coding: utf-8 -*-
import random
from model.project import MantisProject


def test_delete_project(app, admin):
    old_projects = app.soap.get_project_list()
    if not old_projects:
        app.manage_page.add_new_project(MantisProject(name="Project to delete"))
    project_to_delete = random.choice(old_projects)
    app.manage_page.delete_project(project_to_delete)
    old_projects.remove(project_to_delete)
    new_projects = app.soap.get_project_list()
    assert sorted(old_projects, key=MantisProject.id_or_max) == sorted(new_projects, key=MantisProject.id_or_max)
