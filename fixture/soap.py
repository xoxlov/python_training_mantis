from suds.client import Client
from suds import WebFault
from model.project import MantisProject

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        username = self.app.config["webadmin"]["username"]
        password = self.app.config["webadmin"]["password"]
        client = Client("http://localhost/mantisbt/api/soap/mantisconnect.php?wsdl")
        try:
            all_projects = client.service.mc_projects_get_user_accessible(username, password)
            return [MantisProject(id=x.id, name=x.name) for x in all_projects]
        except WebFault as e:
            return False
