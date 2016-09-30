with open('Pamlog.txt') as logfile:
    for line in logfile.readlines():
            if "GCSWebLogicEJBProxy" in line:
                    print "response - ", line.split("|")[9].split(":")[4]
                    print "detail message - ", line.split("|")[9].split((":")[6]
