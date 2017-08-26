# -*- coding: utf-8 -*-
from model.project import MantisProject


class ManagePage(object):

    def __init__(self, app):
        self.app = app
        self.wd = self.app.wd

    @property
    def main_manage_page_button(self):
        return self.wd.find_element_by_css_selector("a[href*='manage_overview_page.php']")

    @property
    def manage_projects_button(self):
        # Ссылка "Управление проектами"
        return self.wd.find_element_by_css_selector("a[href*='/mantisbt/manage_proj_page.php']")

    @property
    def manage_projects_tab_selected(self):
        return self.wd.current_url.endswith("/manage_proj_page.php")

    @property
    def project_name(self):
        return self.wd.find_element_by_css_selector("#project-name")

    @property
    def create_new_project_button(self):
        return self.wd.find_element_by_css_selector(("form[action='manage_proj_create_page.php'] input.btn-primary"))

    @property
    def add_new_project_from_creation_form(self):
        return self.wd.find_element_by_css_selector("#manage-project-create-form input.btn-primary")

    @property
    def delete_project_button(self):
        return self.wd.find_element_by_css_selector("#project-delete-form input[type='submit']")

    @property
    def delete_confirmation_button(self):
        return self.wd.find_element_by_css_selector(".alert input[type='submit']")

    # method cannot be @property because has parameter
    def get_button_for_project(self, id):
        return self.wd.find_element_by_css_selector("a[href*='manage_proj_edit_page.php?project_id=%s']" % id)

    def open_main_manage_page(self):
        if not self.wd.current_url.endswith("manage_overview_page.php"):
            self.main_manage_page_button.click()

    def open_projects_manage_page(self):
        if not self.manage_projects_tab_selected:
            self.open_main_manage_page()
            self.manage_projects_button.click()

    def get_projects_list(self):
        self.open_projects_manage_page()
        pr_list = []
        for pr in self.wd.find_elements_by_css_selector(("a[href*='manage_proj_edit_page.php?project_id=']")):
            href = pr.get_property("attributes")[0]["nodeValue"]
            pr_id = int(href[href.find("=") + 1:])
            pr_list.append(MantisProject(id=pr_id, name=pr.text))
        return pr_list

    def add_new_project(self, name):
        self.open_projects_manage_page()
        self.create_new_project_button.click()
        self._type_data_to_field(self.project_name, name)
        self.add_new_project_from_creation_form.click()
        self.open_projects_manage_page()

    def delete_project(self, project_to_delete):
        self.open_projects_manage_page()
        self.get_button_for_project(id=project_to_delete.id).click()
        # FIXME: костыль! чтобы дополнительная кнопка навигации не перекрывала кнопку удаления
        self.wd.execute_script(("window.scrollTo(0, 250)"))
        self.delete_project_button.click()
        self.delete_confirmation_button.click()
        self.open_projects_manage_page()

    def _type_data_to_field(self, locator, data):
        locator.clear()
        locator.click()
        locator.send_keys(data)
