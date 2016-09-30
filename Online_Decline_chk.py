import datetime
import glob
import sys
#testlog = '/home/ck911c/Pam20160905.log'

def get_nos(file_log):
    mins = int(sys.argv[1])
    #mins = int(raw_input("Enter the time frame in minutes for which you need to check the transanctions: "))
    times_now  = datetime.datetime.now()
    times_b4 = times_now - datetime.timedelta(minutes=mins)
    print "Opened logfile - ", file_log
    for i, line in enumerate(file_log):
        if times_b4.strftime('%Y-%m-%dT%H:%M') in line:
            startline = i
            #print "Found Startline - ", startline
        elif times_now.strftime('%Y-%m-%dT%H:%M') in line:
            endline = i
            break
            #print "Found Endline - ", endline
    return startline, endline

def get_trx_id(strt, nd, file_log):
    trx_id = []
    chk_error = "Card Declined"
    while True:
        line = file_log.readlines()
        if chk_error in line:
            print line
            trx_id.append([line.split("|")[6]])
            print trx_id
    return trx_id

def reasons(trxs, file_log):
    resp_dm = {}
    for line in file_log.readlines():
        for trax in trxs:
            if str(trax) in line:
                if "GCSWebLogicEJBProxy" in line:
                    errline = line.split("|")[9]
                    print errline
                    response, detail_msg = errline.split(":")[4], errline.split(":")[6]
                    tmp_tupl = (response, detail_msg)
                    if tmp_tupl not in resp_dm.items():
                        resp_dm.update({tmp_tupl[0] : tmp_tupl[1]})
    return resp_dm


IDs = []

logdate = datetime.datetime.now().strftime('%Y%m%d')
logpath = glob.glob('/appl/capm/log/pam900*lpv*/')
logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
for log in logpath:
    with open(log) as logfile:
        Start, end = get_nos(logfile)
        print Start
        print end
        IDs = get_trx_id(Start, end, logfile)
        print IDs
        new_IDs = [''.join(id) for id in IDs]
        err_dict = reasons(new_IDs, logfile)

print 'Response', ' '*(50-len('Response')), '|', 'Detail Message', ' '*(50-len('Detail Message'))
print '-'*50, '+', '-'*50
for k in err_dict:
    print k, ' '*(50-len(k)), "|", err_dict[k], ' '*(50-len(err_dict[k]))
