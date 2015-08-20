#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   
#   E-mail  :   
#   Date    :   2014/02/25 
#   Desc    :
#

import json
import urllib
import logging,time
from tornado.httpclient import HTTPClient
from tor_manager.util.httpresponse import ResponseCode

def make_qs(qdict):
    if qdict == None:
        return None 

    if isinstance(qdict, dict):
        return urllib.urlencode(qdict)
    else:
        return None

def make_url(base, query_args):
    qs = make_qs(query_args)
    if qs != None:
        return base + '?' + qs
    else:
        return base

class HttpClient:
    def __init__(self, url):
        self.url = url
        self.http_client = HTTPClient()

    def retry(func):
        def call(self, *args, **kwargs):
            attempts = 0
            ex = None
            while attempts < 10:
                try:
                    ret = func(self, *args, **kwargs)
                    return ret
                except Exception, ex:
                    logging.error("Exception : %s.  Retry!", str(ex))
                    time.sleep(2)
                    attempts += 1
            raise Exception, ex
        return call


    @retry
    def fetch(self, request, **kwargs):
        return self.http_client.fetch(request, **kwargs)

    def post(self, dict):
        try:
            resp = self.fetch(self.url, method='POST', body=json.dumps(dict))
            resp = json.loads(resp.body)
            return resp
        except Exception, ex:
            logging.error("In HttpClient post. Exception: %s" % (str(ex)))
            return None

    def get(self, dict=None):
        try:
            url = self.url
            if dict != None:
                url = make_url(url, dict)
            resp = self.fetch(url, method='GET')
            return json.loads(resp.body)
        except Exception, ex:
            logging.error("In HttpClient get. Exception: %s" % (str(ex)))
            return None

    def put(self, dict):
        try:
            resp = self.fetch(self.url, method='PUT', body=json.dumps(dict))
            return json.loads(resp.body)
        except Exception, ex:
            logging.error("In HttpClient put. Exception: %s" % (str(ex)))
            return None

    def delete(self, dict):
        try:
            get_url = make_url(self.url, dict)
            resp = self.fetch(get_url, method='DELETE')
            return json.loads(resp.body)
        except Exception, ex:
            logging.error("In HttpClient delete. Exception: %s" % (str(ex)))
            return None

    def resp_handler(self, resp):
        if resp == None:
            logging.error("Get response failed! Some error ocurred!")
            return (None, None)

        code = resp.get('response_code', None)
        if code != ResponseCode.SUCCESS:
            logging.error("Response is not 'Success'! ErrorCode: '%s'. Info: %s", resp['response_code_string'], resp['failure_reason'])

        content = resp.get("content", None)
        return (code, content)
