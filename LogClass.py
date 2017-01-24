#!/usr/bin/python

class Logclass(object):
    "Define a generic logclass"
    
    def __init__(self, app, log):
        self.app = app
        self.log = log

    def getLogs(app, log):
        if lower(app) == 'capm':
            if lower(log) == 'pam':
                logpath = glob.glob('/appl/capm/log/pam900*lpv*/')
                logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
            elif lower(log) == 'rte':
                logpath = glob.glob('/appl/capm/log/rte*lpv*/')
                logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
        if lower(app) == 'gcs':
            if lower(log) == 'auth':
                logpath = glob.glob('/opt/app/p1*/newgcs/logs/')
                logpath = 

    def xtrctLog(logpath):
        for log in logpath:




