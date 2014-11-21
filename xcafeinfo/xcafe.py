#!/usr/bin/env python
# encoding: utf-8

from os import path
from collections import namedtuple

import requests
from pyquery import PyQuery

NodeInfo = namedtuple("NodeInfo", [
    "server", "port", "password", "algorithm"])


class XCafe(object):
    dashbord = "dashboard.php"
    nodeinfo = "nodeinfo.php?&sid=%s"
    loginaction = "config/userData.php"

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.session()

    def real_url(self, url):
        return path.join(self.endpoint, url)

    def login(self, user, password):
        self.session.post(self.real_url(self.loginaction), data={
            "email": user, "password": password, "op": "login"})
        self.session.get(self.endpoint)

    def node_info(self, node, s_server, s_port, s_pass, s_alg):
        response = self.session.get(self.real_url(self.nodeinfo % node))
        pquery = PyQuery(response.content)

        return NodeInfo(
            server=pquery(s_server).val(),
            port=pquery(s_port).val(),
            password=pquery(s_pass).val(),
            algorithm=pquery(s_alg).val())
