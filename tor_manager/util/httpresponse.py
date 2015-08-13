#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :
#   E-mail  :
#   Date    :   2014/02/25
#   Desc    :
#
import json
from svc_lib import tools

class ResponseCode:
    SUCCESS = 0
    NO_PARAMETER = 1
    INVALID_PARAMETER = 2
    HAS_EXISTED = 3
    DB_ERROR = 4
    NO_RECORD = 5
    STATUS_ERROR = 6
    LOCK_ERROR = 7
    LOGIC_ERROR = 8
    VRS_ERROR = 9
    CONFIG_ERROR = 10

    code_string_EN = {
        SUCCESS : "SUCCESS",
        NO_PARAMETER : "NO_PARAMETER",
        INVALID_PARAMETER : "INVALID_PARAMETER",
        HAS_EXISTED : "HAS_EXISTED",
        DB_ERROR : "DB_ERROR",
        NO_RECORD : "NO_RECORD",
        STATUS_ERROR : "STATUS_ERROR",
        LOCK_ERROR : "LOCK_ERROR",
        LOGIC_ERROR : "LOGIC_ERROR",
        VRS_ERROR : "VRS_ERROR",
        CONFIG_ERROR : "CONFIG_ERROR",
    }

    failure_reason_EN = {
        SUCCESS : "",
        NO_PARAMETER : "There is no parameter '%s'!",
        INVALID_PARAMETER : "The value of parameter '%s' is invalid!",
        HAS_EXISTED : "This object has existed in the table '%s'!",
        DB_ERROR : "Database error when execute '%s'!",
        NO_RECORD : "No record when query '%s'!",
        STATUS_ERROR : "Can't do the operation in status '%s'",
    }

class Response:
    def make_response(self, code, para=None, content=None, err_str=None):
        response = {}
        response['response_code'] = code
        response['response_code_string'] = ResponseCode.code_string_EN[code]

        failure_reason = ""
        if code != ResponseCode.SUCCESS:
            if para != None:
                failure_reason = ResponseCode.failure_reason_EN[code] % para

            if err_str != None:
                failure_reason = failure_reason + err_str

            response['failure_reason'] = failure_reason

        if content != None:
            response['content'] = content

        return json.dumps(response, default=tools.json_date_default)
