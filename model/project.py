# -*- coding: utf-8 -*-
from sys import maxsize


class MantisProject(object):
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return "{a}: '{b}'".format(a=self.id, b=self.name)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        return int(self.id) if self.id else maxsize
