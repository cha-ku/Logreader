## Author - Chaitanya Kukde

import datetime
import glob
import sys

chk_error = "Card Declined"
logdate = datetime.datetime.now().strftime('%Y%m%d')
logpath = glob.glob('/appl/capm/log/pam900*lpv*/')
logpath = [dir + "Pam" + logdate + ".log".format(dir) for dir in logpath]
mins = int(sys.argv[1])
times_now  = datetime.datetime.now()
times_b4 = times_now - datetime.timedelta(minutes=mins)
trx_id = []

def reasons(trxs, file_log):
    resp_dm = {}
    for line in file_log:
        for trax in trxs:
            if str(trax) in line:
                if "GCSWebLogicEJBProxy" in line:
                    errline = line.split("|")[9]
                    #print "errline - ", errline
                    response, detail_msg = errline.split(":")[4], errline.split(":")[6]
                    tmp_tupl = (response, detail_msg)
                    if tmp_tupl not in resp_dm.items():
                        resp_dm.update({tmp_tupl[0] : tmp_tupl[1]})
    return resp_dm


for log in logpath:
    with open(log) as logfile:
        print "Opened logfile - ", logfile
        startline = False
        for line in logfile:
            if times_b4.strftime('%Y-%m-%dT%H:%M') in line:
                startline = True
            if startline and chk_error in line:
                if line.split("|")[6] not in trx_id:
                    trx_id.append([line.split("|")[6]])
            if times_now.strftime('%Y-%m-%dT%H:%M') in line:
                print "Found Endline"
                break

for log in logpath:
    with open(log) as logfile:
        print "Opened logfile - ", logfile
        new_IDs = [''.join(id) for id in trx_id]
        err_dict = reasons(new_IDs, logfile)

print 'Response', ' '*(50-len('Response')), '|', 'Detail Message', ' '*(50-len('Detail Message'))
print '-'*50, '+', '+', '-'*50
for k in err_dict:
    print k, ' '*(50-len(k)), "|", err_dict[k], ' '*(50-len(err_dict[k]))
