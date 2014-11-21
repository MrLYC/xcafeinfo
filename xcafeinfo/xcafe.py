#!/usr/bin/env python
# encoding: utf-8

import argparse
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


def parse_args(args, conf, sections):
    parser = argparse.ArgumentParser(description="Get nodes info from xcafe")
    parser.add_argument("path")
    parser.add_argument(
        "-e", "--endpoint", default=conf.get(sections.DEFAULT, "endpoint"))
    parser.add_argument(
        "-u", "--user", default=conf.get(sections.DEFAULT, "user"))
    parser.add_argument(
        "-p", "--password", default=conf.get(sections.DEFAULT, "password"))

    conf_nodes = conf.get(sections.DEFAULT, "nodes")
    parser.add_argument(
        "-n", "--nodes", nargs='+', default=(i for i in conf_nodes if i))

    parser.add_argument(
        "--server_selector", default=conf.get(sections.SELECTOR, "server"))
    parser.add_argument(
        "--port_selector", default=conf.get(sections.SELECTOR, "port"))
    parser.add_argument(
        "--password_selector", default=conf.get(sections.SELECTOR, "password"))
    parser.add_argument(
        "--algorithm_selector", default=conf.get(sections.SELECTOR, "algorithm"))

    return parser.parse_args(args)


if __name__ == "__main__":
    from xcafeinfo.cfgmgr import CONF, Sections
    import sys

    args = parse_args(sys.argv, CONF, Sections)

    xcafe = XCafe(args.endpoint)
    xcafe.login(args.user, args.password)
    for node in args.nodes:
        print "node:", node
        nodeinfo = xcafe.node_info(
            node,
            s_server=args.server_selector,
            s_port=args.port_selector,
            s_pass=args.password_selector,
            s_alg=args.algorithm_selector)

        print "\tserver:", nodeinfo.server
        print "\tport:", nodeinfo.port
        print "\tpassword:", nodeinfo.password
        print "\talgorithm:", nodeinfo.algorithm
