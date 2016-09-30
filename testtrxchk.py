import datetime
import glob
import sys
#testlog = '/home/ck911c/Pam20160905.log'

def get_nos():
    logdate = datetime.datetime.now().strftime('%Y%m%d')
    logpath = glob.glob('/appl/capm/log/pam900*lpv*/')
    logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
    mins = int(sys.argv[1])
    #mins = int(raw_input("Enter the time frame in minutes for which you need to check the transanctions: "))
    times_now  = datetime.datetime.now()
    times_b4 = times_now - datetime.timedelta(minutes=mins)
    for log in logpath:
        with open(log) as logfile:
            print "Opened logfile - ", logfile
            for i, line in enumerate(logfile):
                if times_b4.strftime('%Y-%m-%dT%H:%M') in line:
                    startline = i
                    #print "Found Startline - ", startline
                elif times_now.strftime('%Y-%m-%dT%H:%M') in line:
                    endline = i
                    break
                    #print "Found Endline - ", endline
    return startline, endline

def get_trx_id(strt, nd):
    logdate = datetime.datetime.now().strftime('%Y%m%d')
    logpath = glob.glob('/appl/capm/log/pam900*lpv*/')
    logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
    trx_id = []
    chk_error = "Card Declined"
    for log in logpath:
        with open(log) as logfile:
            for line in logfile.readlines()[strt:nd]:
                if chk_error in line:
                    trx_id.append([line.split("|")[6]])
    return trx_id

def reasons(trxs):
    resp_dm = {}
    logdate = datetime.datetime.now().strftime('%Y%m%d')
    logpath = glob.glob('/appl/capm/log/pam900*lpv*/')
    logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
    for log in logpath:
        with open(log) as logfile:
            for line in logfile.readlines():
                for trax in trxs:
                    if str(trax) in line:
                        if "GCSWebLogicEJBProxy" in line:
                            errline = line.split("|")[9]
                            response, detail_msg = errline.split(":")[4], errline.split(":")[6]
                            tmp_tupl = (response, detail_msg)
                            if tmp_tupl not in resp_dm.items():
                                resp_dm.update({tmp_tupl[0] : tmp_tupl[1]})
    return resp_dm


IDs = []

Start, end = get_nos()
IDs = get_trx_id(Start, end)
new_IDs = [''.join(id) for id in IDs]
err_dict = reasons(new_IDs)

print 'Response', ' '*(50-len('Response')), '|', 'Detail Message', ' '*(50-len('Detail Message'))
print '-'*50, '+', '-'*50
for k in err_dict:
    print k, ' '*(50-len(k)) "|", err_dict[k], ' '*(50-len(err_dict[k]))
