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
from tor_manager.util import tools

class HostHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.Resp = Resp()
        url = Config.VALUE['master_url'] + "/host"
        self.http_client = HttpClient(url)
    

    def get(self):
        """
            The GET method is used to get one profile by vid or Profile list
        """
        _method = tools.strip_string(self.get_argument('_method', None))

        if _method == 'delete':
            self.delete()
            return

        if _method == 'put':
            self.put()
            return

        hostname = tools.strip_string(self.get_argument('hostname', None))

        host = {}
        if hostname != None:
            host['hostname'] = hostname 

        resp = self.http_client.get(host)
        (code, body) = self.http_client.resp_handler(resp)
        if code != RespCode.SUCCESS and code != RespCode.NO_RECORD:
            failure_reason = resp.get('failure_reason', None)
            self.render("hostManage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
            return

        if code == RespCode.NO_RECORD:
            self.render("hostManage/viewHosts.html", hosts=None)
            return

        if hostname != None:
            self.render("hostManage/viewHost.html", host=body)
            return

        self.render("hostManage/viewHosts.html", hosts=body)
        return

    def post(self):
        logging.info("Received post body: %s", self.request.body)

        _method = tools.strip_string(self.get_argument('_method', None))
        if _method == 'delete':
            self.delete()
            return

        hostname = tools.strip_string(self.get_argument('hostname', None))
        ip = tools.strip_string(self.get_argument('ip', None))

        host = {}
        host['hostname'] = hostname
        host['ip'] = ip

        resp = self.http_client.post(host)
        logging.debug("Response : %s", str(resp))
        (code, file) = self.http_client.resp_handler(resp)
        if code == RespCode.SUCCESS:
            self.redirect("/host")
        else:
            failure_reason = resp.get('failure_reason', None)
            self.render("hostManage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
        return


    def put(self):
        """
            The put method is used to modify host
        """
        hostname = tools.strip_string(self.get_argument('hostname', None))
        worker_num = tools.to_int(self.get_argument('worker_num', None))

        host = {}
        if hostname != None:
            host['hostname'] = hostname
        if worker_num != None:
            host['worker_num'] = worker_num

        resp = self.http_client.put(host)
        (code, body) = self.http_client.resp_handler(resp)
        if code != RespCode.SUCCESS:
            failure_reason = resp.get('failure_reason', None)
            self.render("hostManage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
            return

        self.redirect("/host")
        return

    def delete(self):
        """
            The delete method is used to delete profile
        """
        hostname = tools.strip_string(self.get_argument('hostname', None))

        host = {}
        if hostname != None:
            host['hostname'] = hostname 

        resp = self.http_client.delete(host)
        (code, body) = self.http_client.resp_handler(resp)
        if code != RespCode.SUCCESS:
            failure_reason = resp.get('failure_reason', None)
            self.render("hostManage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
            return

        self.redirect("/host")
        return
