#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :
#   E-mail  :
#   Date    :   2014/02/25
#   Desc    :
#

"""

"""
import logging, urllib, os, sys, shutil
from datetime import date, datetime
import tornado.httpclient

def strip_string(ori):
    #if isinstance(ori, str):
    if ori == None or ori == "":
        return None

    ori = unicode(ori)
    #ori = str(ori).strip()
    ori = ori.strip("\'")
    ori = ori.strip("\"")
    #ori = ori.replace('\r','')
    #ori = ori.replace('\n','')
    return ori

def to_int(num):
    if num == None:
        return num

    try:
        num = strip_string(num)
        value = int(num)
        return value
    except Exception, ex:
        logging.error("Convert '%s' to Int Error: %s", num, str(ex))
        return None

def to_encode(ustr, encoding='utf-8'):  
    if ustr is None:  
        return ''  
    if isinstance(ustr, unicode):  
        return ustr.encode(encoding, 'ignore')  
    else:  
        return str(ustr) 

def json_date_default(obj):
    if isinstance(obj, datetime):
        #return obj.strftime('%Y-%m-%d %H:%M:%S')
        return str(obj)
    elif isinstance(obj, date):
        #return obj.strftime('%Y-%m-%d')
        return str(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)

def query_sql_generator(base, field, opt, value, if_str=True, if_time=False):
    sql = base
    if sql.find('WHERE') == -1 and sql.find('where') == -1:
        sql = sql + " WHERE "
    else:
        sql = sql + " AND " 

    if if_time:
        sql = sql + "%s %s '%s'" % (field, opt, value)
        return sql

    sql = sql + "%s %s " % (field, opt)

    if if_str:
        sql = sql + "'%s'" % value
    else:
        sql = sql + "%s" % value

    return sql

def update_sql_generator(tablename, rowdict, prefix=None):
    sql = "UPDATE %s Set " % tablename
    if prefix != None:
        sql = sql + " %s, " % prefix

    values = []
    vstr = ""
    for (k,v) in  rowdict.items():
        if v == None:
            continue

        if not isinstance(v, int):
            values.append("%s='%s' " % (k, v.replace("'", "\\\'")))
        else:
            values.append("%s=%s " % (k, v))

    #for item in values:
    vstr =  ", ".join(values)

    sql = sql + vstr
    return sql


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

def make_post_request(url, data={}, headers={}, connect_timeout=20, request_timeout=60):
    body = make_qs(data)
    content_type = 'application/x-www-form-urlencoded'

    headers.update({'Content-Type' : content_type,
               'Content-Length': str(len(body))})

    return tornado.httpclient.HTTPRequest(
                method='POST',
                headers=headers,
                url=url,
                body=body,
                connect_timeout=connect_timeout,
                request_timeout=request_timeout)

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def copy(src, dst):
    if os.path.islink(src):
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
    else:
        shutil.copy(src,dst)
