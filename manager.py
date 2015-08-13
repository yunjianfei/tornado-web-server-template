#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
#
#   Author  :   jianfeiyun
#   E-mail  :   jianfeiyun@gmail.com
#   Date    :   2014/02/25 
#   Desc    :
#

""" 

Usecase:
    ./manager --port=8888

"""

import string,os,sys,logging,signal,time,threading,socket
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tor_manager.util.options import define,options
from tor_manager.util.config import Config
from tor_manager.service.main import MainHandler
from tor_manager.service.host import HostHandler

MODULE = "manager"
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
HTTP_SERVER = None
CONF_FILE = "./tor_manager/conf/svc.conf"

#Define command parameter
define("port", default=None, help="Run server on a specific port, mast input", type=int)
define("conf", default=None, help="Config file", type=str)

#The config file parser
def parse_config(conf_file):
    cf = conf_file
    #parse conf file
    if cf == None or cf == "":
        cf = CONF_FILE
    try:
        conf = Config(cf)
        ret = conf.load_conf()
        if ret == -1:
            print "Error: '%s' is not config file or not exist!" % (cf)
            quit()
    except Exception, ex:
        print "Excetion: %s" % (str(ex))
        quit()

#Init logging
def init_logging(port):
    hostname = socket.gethostname()
    log_file = MODULE + "." + hostname + ".log"
    logger = logging.getLogger()
    logger.setLevel(Config.VALUE['log_level'])

    #create log path
    log_path = Config.VALUE['log_path']
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    #fh = logging.FileHandler(os.path.join(log_path, log_file))
    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, log_file), when='D', backupCount=2)
    sh = logging.StreamHandler()

    ###########This set the logging level that show on the screen#############
    #sh.setLevel(logging.DEBUG)
    #sh.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    fh.setFormatter(formatter) 
    sh.setFormatter(formatter) 

    logger.addHandler(fh)
    logger.addHandler(sh)
    logging.info("Current log level is : %s",logging.getLevelName(logger.getEffectiveLevel()))


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    logging.info('Stopping http server')
    HTTP_SERVER.stop()

    logging.info('SVC Manager will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')

    stop_loop()


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "tor_manager/html"),
        )

        handlers = [
            (r"/", MainHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "tor_manager/static")}),
            (r"/host", HostHandler),
        ]

        super(Application,self).__init__(handlers,**settings)
    
def main():
    #################parse command#######################
    try:
        options.parse_command_line()
    except Exception, ex:
        logging.error("%s", str(ex))
        quit()


    if options.port == None:
        options.print_help()
        return

    ############parse and load config file###############
    parse_config(options.conf)

    ############init logging##############################
    init_logging(options.port)

    logging.info("Test info:SVC Manager start!")
    logging.error("Test error:SVC Manager start!")
    logging.debug("Test debug:SVC Manager start!")
    
    ############setting tornado server#####################
    global HTTP_SERVER

    try:
        HTTP_SERVER = tornado.httpserver.HTTPServer(Application())
        HTTP_SERVER.listen(options.port)
    except Exception, ex:
        logging.error("Create and listen http server failed! Exception: %s", str(ex))
        quit()
    logging.info("Begin listen to port: %s!", options.port)

    ##############set signal handler#######################
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)


    ############start tornado server#######################
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit SVC-Manager')

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()
