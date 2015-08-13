#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   
#   E-mail  :   
#   Date    :   2014/02/25 
#   Desc    :
#

import tornado.web
import json,logging,types,time,urllib2
from tor_manager.util.config import Config
from tor_manager.util.httpclient import HttpClient
from tor_manager.util.httpresponse import Response as Resp, ResponseCode as RespCode

class MainHandler(tornado.web.RequestHandler):
    """docstring for MainHandler"""

    def initialize(self):
        self.Resp = Resp()

    def get(self):
        ori = self.get_argument("ori", None)
        if ori == None:
            self.render("index.html", title = "a", name = "b")
            return

        if ori == "host":
            self.render("hostManage/addHost.html")
            return

        if ori == "user":
            self.render("userManage/addUser.html")
            #self.render("userManage/selectUser.html")
            return

    def post(self):
        data = self.request.body
        logging.info("Received data: %s", data)
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        logging.info("User logging! username: %s, password: %s", username, password)

        self.render("tor_main.html", username=username)
