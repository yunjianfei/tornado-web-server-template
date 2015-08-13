#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   
#   E-mail  :   
#   Date    :   2014/02/25 
#   Desc    :
#

import ConfigParser
import string,os,sys,logging

class Config:
    VALUE = {
        #####################master config######################
        'master_url' : None,
        #####################log config########################
        'log_level' : None,
        'log_path' : None,
        #################default value config##################
        'num_per_page' : None,
    }

    ###init func###
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.cf = None
        self.CONFS = [
          { 'item' : 'master_url', 'func' : self.get_master_url, 'required' : True, 'default' : None },
          { 'item' : 'log_level', 'func' : self.get_log_level, 'required' : False, 'default' : logging.INFO, },
          { 'item' : 'log_path', 'func' : self.get_log_path, 'required' : False, 'default' : '/var/svc/log', },
          { 'item' : 'num_per_page', 'func' : self.get_num_per_page, 'required' : False, 'default' : 10, },
        ]

    def get(self, type, item):
        try:
            return self.cf.get(type, item)
        except Exception, ex:
            #logging.error("Error ocurred when get '%s' '%s'! Exception: %s", type, item, str(ex))
            print "Error ocurred when get '%s' '%s'! Exception: %s" % (type, item, str(ex))
            return None

    def get_config_item(self, item):
        conf = item['item']
        func = item['func']
        ret = func()

        if ret == None and item['required'] == True:
            print "Error: The configure item '%s' is required!" % item['item']
            quit()

        if ret == None and item['default'] != None:
            Config.VALUE[conf] = item['default']
            return

        if ret != None:
            Config.VALUE[conf] = ret

        return
            
    ###load config###
    def load_conf(self):
        if os.path.isfile(self.conf_file):

            self.cf = ConfigParser.ConfigParser()
            self.cf.read(self.conf_file)

            for c in self.CONFS:
                self.get_config_item(c)

            return 0
        else:
            print "Error: '%s' is not exist or not file!" % (self.conf_file)
            quit()
            return -1
    
    def get_master_url(self):
        '''  get master url '''
        return self.get("master", "master_url") 

    def get_log_path(self):
        '''  get log path '''
        path = self.get("log", "log_path") 
        if path == "" or path == None:
            return None
        else:
            return path

    def get_log_level(self):
        '''  get log path '''
        level = self.get("log", "log_level")
        if level == "DEBUG":
            return logging.DEBUG
        elif level == "INFO":
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "ERROR":
            return logging.ERROR
        else:
            return None

    def get_num_per_page(self):
        '''  get default num per page for paging'''
        return int(self.get("default", "num_per_page"))
